import psycopg2
import streamlit as st
import hashlib
import datetime

# Get connection
@st.cache_resource
def get_connection():
    conn = psycopg2.connect(st.secrets["postgres"]["connection_string"])
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, hash_password(password)))
    user = cur.fetchone()
    return user[0] if user else None

def init_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_progress (user_id, current_level, score, last_updated)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (user_id) DO NOTHING;
    """, (user_id, 1, 0))
    conn.commit()

def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT current_level, score FROM user_progress WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    return {"current_level": result[0], "score": result[1]} if result else None

def update_user_progress(user_id, level, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_progress SET current_level = %s, score = %s, last_updated = NOW()
        WHERE user_id = %s
    """, (level, score, user_id))
    conn.commit()
