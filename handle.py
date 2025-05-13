import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(st.secrets["postgres"]["connection_string"])

def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT current_level, score FROM user_progress WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"current_level": row[0], "score": row[1]}
    return None

def update_user_progress(user_id, level, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_progress
        SET current_level = %s, score = %s, last_updated = NOW()
        WHERE user_id = %s
    """, (level, score, user_id))
    conn.commit()
    conn.close()

def init_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_progress (user_id, current_level, score, last_updated)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (user_id) DO NOTHING
    """, (user_id, 1, 0))
    conn.commit()
    conn.close()
