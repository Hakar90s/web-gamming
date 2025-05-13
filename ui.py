import streamlit as st
from handle import get_level_image

# Login or Sign Up form
def login_or_signup_form():
    auth_mode = st.selectbox("Login or Sign up", ["Login", "Sign up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    return auth_mode, username, password

# Display the current level and the associated image
def display_game(level, score):
    st.subheader(f"Level {level}")
    st.image(get_level_image(level), caption=f"Level {level} Image", use_container_width=True)

# Display score and level in the sidebar
def display_score(level, score):
    st.sidebar.write(f"Current Score: {score}")
    st.sidebar.write(f"Current Level: {level}")

# Log-out button functionality
def logout_button():
    if st.button("Log Out"):
        del st.session_state['user_id']
        st.session_state.level = 1
        st.session_state.score = 0
        st.rerun()  # Replaces experimental_rerun with st.rerun()
