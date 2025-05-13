import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress
)
from level_data import level_data

st.set_page_config(page_title="🎮 100-Level Image Game", layout="centered")
st.title("🎮 100-Level Image Game")

# ------------------ Authentication ------------------ #
def logout_button():
    if st.sidebar.button("🚪 Log out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Check if the user is logged in or not
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
            st.session_state.username = username  # Store username in session state
            st.rerun()  # Rerun the app to reload with user data
        else:
            st.error("Invalid credentials.")
    st.stop()  # Stop execution if user is not logged in yet

# ------------------ Game State ------------------ #
# Retrieve user data from session state
user_id = st.session_state.user_id
level = st.session_state.level
score = st.session_state.score
username = st.session_state.username  # Fetch username from session state

logout_button()  # Render log-out button in the sidebar

level_info = level_data.get(level)

if not level_info:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")
    st.stop()

# ------------------ Game UI ------------------ #
st.subheader(f"Level {level}")
st.image(level_info["image_url"], caption=f"Level {level}", use_container_width=True)
st.write(level_info["question"])

user_answer = st.text_input("Your Answer").strip().lower()

def handle_answer_submission():
    """Handle the submission of the user's answer."""
    if user_answer == level_info["answer"]:
        st.success("Correct! Moving to the next level.")
        st.session_state.level += 1
        st.session_state.score += 10
        update_user_progress(user_id, st.session_state.level, st.session_state.score)
        st.rerun()  # Rerun the app to reflect new level and score
    else:
        st.warning("Wrong answer. Try again!")

def show_answer():
    """Display the correct answer and give the user the option to proceed to the next level."""
    st.write(f"The correct answer is: **{level_info['answer']}**")
    st.write("Click the button below to proceed to the next level.")
    if st.button("Continue to Next Level"):
        st.session_state.level += 1
        st.session_state.score += 10
        update_user_progress(user_id, st.session_state.level, st.session_state.score)
        st.rerun()  # Rerun the app to reflect new level and score

# ------------------ Buttons ------------------ #
if st.button("Submit Answer"):
    handle_answer_submission()

if st.button("Show Answer"):
    show_answer()

# ------------------ Sidebar ------------------ #
# Display username, score, and current level in the sidebar
st.sidebar.write(f"👤 Username: {st.session_state.get('username', 'Guest')}")
st.sidebar.write(f"⭐ Score: {score}")
st.sidebar.write(f"🏁 Level: {level}")
