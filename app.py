# app.py
import streamlit as st
from handle import get_level, save_user_answer, update_user_progress, get_user_progress

st.set_page_config(page_title="Puzzle Realm", layout="centered")

# Simulate user_id for now
USER_ID = 1

# Initialize session state
if 'level' not in st.session_state:
    progress = get_user_progress(USER_ID)
    st.session_state.level = progress['current_level']
    st.session_state.score = progress['score']

# Load level
level_data = get_level(st.session_state.level)

st.title(f"🧩 Puzzle Realm - Level {level_data['level_number']}")
st.image(level_data['image_url'], use_column_width=True)
st.write(level_data['question'])

# Answer input
answer = st.text_input("Your Answer:")
if st.button("Submit"):
    is_correct = answer.strip().lower() == level_data['answer'].strip().lower()
    save_user_answer(USER_ID, level_data['id'], answer, is_correct)

    if is_correct:
        st.success("✅ Correct! Moving to next level.")
        st.session_state.score += level_data['difficulty']
        st.session_state.level += 1
        update_user_progress(USER_ID, st.session_state.level, st.session_state.score)
        st.experimental_rerun()
    else:
        st.error("❌ Incorrect. Try again or use a hint.")
        if level_data['hint']:
            st.info(f"Hint: {level_data['hint']}")
