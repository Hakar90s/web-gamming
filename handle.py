import psycopg2
import streamlit as st
import hashlib
from datetime import datetime
import os

# Get connection from secrets
def get_connection():
    return psycopg2.connect(st.secrets["postgres"]["connection_string"])

# Hash passwords (very basic, use bcrypt in production)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign up a new user
def signup_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
        conn.commit()
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = cur.fetchone()[0]
        init_user_progress(user_id)
        cur.close()
        conn.close()
        return user_id
    except psycopg2.Error as e:
        conn.rollback()
        st.error("Username already exists or another error occurred.")
        return None

# Log in user
def login_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, hash_password(password)))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except psycopg2.Error as e:
        st.error("Login failed due to a database error.")
        return None

# Initialize progress if new
def init_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_progress (user_id, current_level, score, last_played)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id, 1, 0))
    conn.commit()
    cur.close()
    conn.close()

# Get current progress
def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT current_level, score FROM user_progress WHERE user_id=%s", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {"current_level": result[0], "score": result[1]}
    else:
        return {"current_level": 1, "score": 0}

# Update progress
def update_user_progress(user_id, level, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_progress
        SET current_level=%s, score=%s, last_played=NOW()
        WHERE user_id=%s
    """, (level, score, user_id))
    conn.commit()
    cur.close()
    conn.close()

def register_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password) VALUES (%s, %s)
            ON CONFLICT (username) DO NOTHING;
        """, (username, hash_password(password)))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Error in register_user:", e)
        return False

