import streamlit as st
from handle import (
    login_user, register_user,
    get_user_progress, update_user_progress,
    get_level_image
)

# --- SESSION ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- AUTHENTICATION ---
st.title("🎮 100-Level Image Challenge Game")

auth_choice = st.sidebar.radio("Login / Sign up", ["Login", "Sign up"])

with st.sidebar.form(key="auth_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Submit")

if submit:
    if auth_choice == "Login":
        user_id = login_user(username, password)
        if user_id:
            st.session_state.user_id = user_id
            user_data = get_user_progress(user_id)
            st.session_state.level = user_data['current_level']
            st.session_state.score = user_data['score']
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Login failed. Please check credentials.")
    else:
        success = register_user(username, password)
        if success:
            st.success("Sign up successful. Please log in.")
        else:
            st.error("Username already exists.")

# --- GAME ---
if st.session_state.user_id:
    st.subheader(f"🧠 Level {st.session_state.level}")
    st.write(f"Score: {st.session_state.score}")

    image_url = get_level_image(st.session_state.level)
    st.image(image_url, use_column_width=True)

    user_answer = st.text_input("Your answer:")

    if st.button("Submit Answer"):
        correct_answer = f"answer{st.session_state.level}"  # Replace with real logic

        if user_answer.lower().strip() == correct_answer:
            st.success("✅ Correct!")
            st.session_state.level += 1
            st.session_state.score += 10
            update_user_progress(
                st.session_state.user_id,
                st.session_state.level,
                st.session_state.score
            )
        else:
            st.warning("❌ Incorrect. Try again.")
