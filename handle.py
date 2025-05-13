# handle.py
import psycopg2
from psycopg2.extras import RealDictCursor

# Neon DB connection string
DB_URL = "postgresql://neondb_owner:npg_lNW8tqmcJ0XD@ep-soft-sunset-a2320sps-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require"

def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def get_level(level_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM levels WHERE level_number = %s", (level_number,))
    result = cur.fetchone()
    conn.close()
    return result

def save_user_answer(user_id, level_id, user_answer, is_correct):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_answers (user_id, level_id, user_answer, is_correct)
        VALUES (%s, %s, %s, %s)
    """, (user_id, level_id, user_answer, is_correct))
    conn.commit()
    conn.close()

def update_user_progress(user_id, new_level, new_score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_progress
        SET current_level = %s, score = %s, last_updated = NOW()
        WHERE user_id = %s
    """, (new_level, new_score, user_id))
    conn.commit()
    conn.close()

def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT current_level, score FROM user_progress WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result
