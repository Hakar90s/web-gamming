import streamlit as st
from handle import login_user, register_user, init_user_progress, get_user_progress, update_user_progress
from PIL import Image

st.set_page_config(page_title="Image Quest Game", layout="centered")

st.title("🧠 Image Quest Game")

# Session states
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.level = None
    st.session_state.score = None

# Authentication
if st.session_state.user_id is None:
    auth_option = st.radio("Login or Sign up", ["Login", "Sign up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_option == "Login":
        if st.button("Login"):
            user_id = login_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                progress = get_user_progress(user_id)
                if progress:
                    st.session_state.level = progress["current_level"]
                    st.session_state.score = progress["score"]
                else:
                    st.session_state.level = 1
                    st.session_state.score = 0
                    init_user_progress(user_id)
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")

    elif auth_option == "Sign up":
        if st.button("Sign up"):
            success = register_user(username, password)
            if success:
                st.success("User registered. Please log in.")
            else:
                st.error("Username already exists.")
    st.stop()

# Game interface
st.subheader(f"Welcome, Level {st.session_state.level} | Score: {st.session_state.score}")

# Show image for current level
def get_level_image(level):
    try:
        return Image.open(f"images/level_{level}.png")
    except:
        return None

img = get_level_image(st.session_state.level)
if img:
    st.image(img, caption=f"Level {st.session_state.level}", use_column_width=True)
else:
    st.warning("Level image not found.")

# Game input (change logic as needed)
user_answer = st.text_input("Enter the secret word to proceed:")
if st.button("Submit Answer"):
    if user_answer.strip().lower() == "next":
        st.session_state.level += 1
        st.session_state.score += 10
        update_user_progress(st.session_state.user_id, st.session_state.level, st.session_state.score)
        st.success("Correct! Advancing to next level...")
        st.experimental_rerun()
    else:
        st.error("Incorrect. Try again!")

# Logout
if st.button("Logout"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
