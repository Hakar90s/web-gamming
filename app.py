import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress
)
from level_data import level_data

# — Page config —
st.set_page_config(page_title="🎮 100-Level Image Game", layout="centered")
st.title("🎮 100-Level Image Game")

# — Auth helpers —
def logout_button():
    if st.sidebar.button("🚪 Log out"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# — Authentication flow —
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
            # init per-level flags
            st.session_state.correct_answer       = False
            st.session_state.show_answer_now      = False
            st.session_state.scored_current_level = False
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# — Game state & UI —
user_id = st.session_state.user_id
username = st.session_state.username
level    = st.session_state.level
score    = st.session_state.score

logout_button()

info = level_data.get(level)
if not info:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")
    st.stop()

st.subheader(f"Level {level}")

# ensure flags exist
for flag in ("correct_answer","show_answer_now","scored_current_level"):
    if flag not in st.session_state:
        st.session_state[flag] = False

# choose image
img = info["answer_image_url"] if (st.session_state.correct_answer or st.session_state.show_answer_now) else info["image_url"]
st.image(img, use_container_width=True)

# — Answer form (one click only) —
with st.form("answer_form"):
    st.write(info["question"])
    st.text_input("Your Answer", key="answer_input")
    submit_clicked = st.form_submit_button("Submit Answer")
    show_clicked   = st.form_submit_button("Show Answer")

# process form actions
if submit_clicked:
    ans = st.session_state.answer_input.strip().lower()
    if ans == info["answer"]:
        st.session_state.correct_answer = True
        st.success("✅ Correct! Answer image shown.")
        if not st.session_state.scored_current_level:
            st.session_state.score += 10
            update_user_progress(user_id, level, st.session_state.score)
            st.session_state.scored_current_level = True
    else:
        st.warning("❌ Wrong answer, try again.")

if show_clicked:
    st.session_state.show_answer_now = True

# — Navigation buttons —
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.session_state.correct_answer or st.session_state.show_answer_now:
        if st.button("Continue to Next Level"):
            st.session_state.level += 1
            # reset level flags
            st.session_state.correct_answer       = False
            st.session_state.show_answer_now      = False
            st.session_state.scored_current_level = False
            update_user_progress(user_id, st.session_state.level, st.session_state.score)
            st.rerun()
with col2:
    if st.button("⬅️ Previous Level"):
        if level > 1:
            st.session_state.level -= 1
            st.session_state.correct_answer       = False
            st.session_state.show_answer_now      = False
            st.session_state.scored_current_level = False
            st.rerun()
        else:
            st.warning("You're already at level 1.")
with col3:
    # placeholder for any future button
    pass

# — Sidebar info —
st.sidebar.write(f"👤 Username: {username}")
st.sidebar.write(f"⭐ Score: {score}")
st.sidebar.write(f"🏁 Level: {level}")
