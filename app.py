import streamlit as st
from handle import get_user_progress, update_user_progress, init_user_progress

USER_ID = 1  # Placeholder for single-user app (can be replaced with login)

st.set_page_config(page_title="100-Level Image Game", layout="centered")

# Initialize session state
if 'level' not in st.session_state:
    progress = get_user_progress(USER_ID)
    if progress:
        st.session_state.level = progress['current_level']
        st.session_state.score = progress['score']
    else:
        st.session_state.level = 1
        st.session_state.score = 0
        init_user_progress(USER_ID)

# Dummy content for level (replace with image-based logic)
st.title(f"Level {st.session_state.level}")
st.image("https://via.placeholder.com/300x200.png?text=Level+" + str(st.session_state.level))

# Game interaction
user_input = st.text_input("Enter the answer:")

# Example condition
if st.button("Submit"):
    if user_input.lower() == "pass":  # Replace with real validation
        st.success("Correct!")
        st.session_state.score += 10
        st.session_state.level += 1
        update_user_progress(USER_ID, st.session_state.level, st.session_state.score)
        st.experimental_rerun()
    else:
        st.error("Try again!")

st.markdown(f"**Score:** {st.session_state.score}")
