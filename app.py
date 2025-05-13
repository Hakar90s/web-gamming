import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress
)
from ui import login_or_signup_form, display_game, display_score, logout_button

st.set_page_config(page_title="100-Level Image Game", layout="centered")

# Login or register
if "user_id" not in st.session_state:
    # Display login or sign up form
    auth_mode, username, password = login_or_signup_form()

    # Handle login or registration
    if st.button(auth_mode):
        if auth_mode == "Sign up":
            user_id = register_user(username, password)
        else:
            user_id = login_user(username, password)

        if user_id:
            # Store user ID in session and fetch user progress
            st.session_state.user_id = user_id
            progress = get_user_progress(user_id)
            if not progress:
                # Initialize user progress if not found
                init_user_progress(user_id)
                st.session_state.level = 1
                st.session_state.score = 0
            else:
                # Set the user's progress
                st.session_state.level = progress["current_level"]
                st.session_state.score = progress["score"]
            st.rerun()  # Refreshes the page after login
        else:
            st.error("Invalid credentials.")
    st.stop()  # Stop here if no user is logged in

# Log-out functionality
logout_button()

# Game view
level = st.session_state.level
score = st.session_state.score
user_id = st.session_state.user_id

# Display current game level and image
display_game(level, score)

# Simulated correct answer check (replace with actual game logic)
answer = st.text_input("Your Answer").lower()

if st.button("Submit"):
    if answer == "correct":  # Replace with actual answer-checking logic
        st.success("Correct! Moving to next level.")
        st.session_state.level += 1
        st.session_state.score += 10
        update_user_progress(user_id, st.session_state.level, st.session_state.score)
    else:
        st.warning("Wrong answer. Try again!")

# Celebrate when user reaches level 100
if level >= 100:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")

# Display score and level in the sidebar
display_score(level, score)
