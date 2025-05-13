import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress, get_level_image
)

st.set_page_config(page_title="100-Level Image Game", layout="centered")

st.title("🎮 100-Level Image Game")

# Login or register
if "user_id" not in st.session_state:
    auth_mode = st.selectbox("Login or Sign up", ["Login", "Sign up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(auth_mode):
        if auth_mode == "Sign up":
            user_id = register_user(username, password)
        else:
            user_id = login_user(username, password)

        if user_id:
            st.session_state.user_id = user_id
            progress = get_user_progress(user_id)
            if not progress:
                init_user_progress(user_id)
                st.session_state.level = 1
                st.session_state.score = 0
            else:
                st.session_state.level = progress["current_level"]
                st.session_state.score = progress["score"]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# Load game
level = st.session_state.level
score = st.session_state.score
user_id = st.session_state.user_id

st.subheader(f"Level {level}")
st.image(get_level_image(level), caption=f"Level {level} Image", use_column_width=True)

# Simulated correct answer check (you should replace this)
answer = st.text_input("Your Answer").lower()

if st.button("Submit"):
    if answer == "correct":  # Replace with your logic
        st.success("Correct! Moving to next level.")
        st.session_state.level += 1
        st.session_state.score += 10
        update_user_progress(user_id, st.session_state.level, st.session_state.score)
    else:
        st.warning("Wrong answer. Try again!")

if level >= 100:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")

st.sidebar.write(f"Current Score: {score}")
st.sidebar.write(f"Current Level: {level}")
