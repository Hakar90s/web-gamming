import streamlit as st

def show_sidebar():
    user = st.session_state.get("username", "Guest")
    score = st.session_state.get("score", 0)
    lvl = st.session_state.get("level", 1)
    st.sidebar.write(f"👤 Username: {user}")
    st.sidebar.write(f"⭐ Score: {score}")
    st.sidebar.write(f"🏁 Level: {lvl}")
