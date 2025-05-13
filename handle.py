import psycopg2
import hashlib
import os
import streamlit as st

# Connect using secrets
def get_connection():
    return psycopg2.connect(st.secrets["postgres"]["connection_string"])

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (username, hash_password(password)))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        st.error("Username already exists.")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()
    return get_user_id(username)

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM users WHERE username=%s AND password=%s
    """, (username, hash_password(password)))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user[0] if user else None

def get_user_id(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    user_id = cur.fetchone()
    cur.close()
    conn.close()
    return user_id[0] if user_id else None

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

def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT current_level, score FROM user_progress WHERE user_id=%s
    """, (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'current_level': result[0], 'score': result[1]}
    return None

def update_user_progress(user_id, level, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_progress
        SET current_level = %s, score = %s, last_played = NOW()
        WHERE user_id = %s
    """, (level, score, user_id))
    conn.commit()
    cur.close()
    conn.close()

def get_level_image(level):
    return f"https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/images/level_{level}.png"
