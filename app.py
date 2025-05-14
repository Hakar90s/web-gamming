import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress
)
from level_data import level_data

# -------------------- Page Configuration -------------------- #
st.set_page_config(page_title="🎮 100-Level Image Game", layout="centered")
st.title("🎮 100-Level Image Game")

# -------------------- Auth Section -------------------- #
def logout_button():
    if st.sidebar.button("🚪 Log out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

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

            # Reset game flags
            st.session_state.correct_answer = False
            st.session_state.show_answer_now = False
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# -------------------- Game State -------------------- #
user_id = st.session_state.user_id
username = st.session_state.username
level = st.session_state.level
score = st.session_state.score

# -------------------- Load Level -------------------- #
level_info = level_data.get(level)

if not level_info:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")
    st.stop()

# Initialize session flags if not set
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = False
if "show_answer_now" not in st.session_state:
    st.session_state.show_answer_now = False

st.subheader(f"Level {level}")

# Determine which image to show
image_url = (
    level_info["answer_image_url"]
    if st.session_state.correct_answer or st.session_state.show_answer_now
    else level_info["image_url"]
)

st.image(image_url, caption=f"Level {level}", use_container_width=True)
st.write(level_info["question"])

# -------------------- Input & Buttons -------------------- #
user_answer = st.text_input("Your Answer").strip().lower()

def handle_answer_submission():
    if user_answer == level_info["answer"]:
        st.session_state.correct_answer = True
        st.success("✅ Correct! See the answer image above.")
        st.session_state.score += 10
        update_user_progress(user_id, level, st.session_state.score)
    else:
        st.warning("❌ Wrong answer. Try again!")

def show_answer():
    st.session_state.show_answer_now = True

def continue_to_next_level():
    st.session_state.level += 1
    st.session_state.correct_answer = False
    st.session_state.show_answer_now = False
    update_user_progress(user_id, st.session_state.level, st.session_state.score)
    st.rerun()

def go_back_to_previous_level():
    if level > 1:
        st.session_state.level -= 1
        st.session_state.correct_answer = False
        st.session_state.show_answer_now = False
        st.rerun()
    else:
        st.warning("You're already at the first level!")

# Buttons
if st.button("Submit Answer"):
    handle_answer_submission()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Show Answer"):
        show_answer()
with col2:
    if st.button("Continue to Next Level"):
        continue_to_next_level()
with col3:
    if st.button("⬅️ Previous Level"):
        go_back_to_previous_level()

# -------------------- Sidebar -------------------- #
st.sidebar.write(f"👤 Username: {username}")
st.sidebar.write(f"⭐ Score: {score}")
st.sidebar.write(f"🏁 Level: {level}")

logout_button()
