import streamlit as st
from handle import register_user, login_user, get_user_progress, init_user_progress

def logout_button():
    if st.sidebar.button("🚪 Log out"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

def login_flow():
    if "user_id" not in st.session_state:
        mode = st.selectbox("Login or Sign up", ["Login", "Sign up"])
        user = st.text_input("Username")
        pwd  = st.text_input("Password", type="password")
        if st.button(mode):
            if mode == "Sign up":
                uid = register_user(user, pwd)
            else:
                uid = login_user(user, pwd)
            if uid:
                st.session_state.user_id = uid
                st.session_state.username = user
                prog = get_user_progress(uid)
                if not prog:
                    init_user_progress(uid)
                    st.session_state.level = 1
                    st.session_state.score = 0
                else:
                    st.session_state.level = prog["current_level"]
                    st.session_state.score = prog["score"]
                # per‐level flags
                st.session_state.correct_answer       = False
                st.session_state.show_answer_now      = False
                st.session_state.scored_current_level = False
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.stop()
