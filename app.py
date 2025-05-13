import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress
)
from level_data import level_data

# --- Setup ---
st.set_page_config(page_title="🎮 100-Level Image Game", layout="centered")
st.title("🎮 100-Level Image Game")

# --- Logout Button ---
def logout_button():
    if st.sidebar.button("🚪 Log out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Authentication ---
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
            st.session_state.username = username
            progress = get_user_progress(user_id)
            if not progress:
                init_user_progress(user_id)
                st.session_state.level = 1
                st.session_state.score = 0
            else:
                st.session_state.level = progress["current_level"]
                st.session_state.score = progress["score"]
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# --- Game State ---
user_id = st.session_state.user_id
username = st.session_state.username
level = st.session_state.level
score = st.session_state.score

logout_button()

level_info = level_data.get(level)
if not level_info:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")
    st.stop()

# --- Game UI ---
st.subheader(f"Level {level}")
st.image(level_info["image_url"], caption=f"Level {level}", use_container_width=True)
st.write(level_info["question"])

# User answer input
user_answer = st.text_input("Your Answer").strip().lower()

# --- Button Actions ---
if st.button("Submit Answer"):
    if user_answer == level_info["answer"]:
        st.success("✅ Correct!")
        st.session_state.level += 1
        st.session_state.score += 10
        update_user_progress(user_id, st.session_state.level, st.session_state.score)
        st.rerun()
    else:
        st.warning("❌ Wrong answer. Try again.")

if st.button("Show Correct Answer"):
    st.info(f"✅ The correct answer is: **{level_info['answer']}**")

if st.button("Continue to Next Level"):
    st.session_state.level += 1
    st.session_state.score += 0  # No score if skipped
    update_user_progress(user_id, st.session_state.level, st.session_state.score)
    st.rerun()

if st.button("⬅ Go Back to Previous Level"):
    if level > 1:
        st.session_state.level -= 1
        st.rerun()
    else:
        st.warning("You are already at the first level!")

# --- Sidebar ---
st.sidebar.write(f"👤 Username: {st.session_state.get('username', 'Guest')}")
st.sidebar.write(f"⭐ Score: {score}")
st.sidebar.write(f"🏁 Level: {level}")
