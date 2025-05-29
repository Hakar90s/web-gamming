import streamlit as st
from handle import (
    register_user, login_user, get_user_progress,
    init_user_progress, update_user_progress
)
from level_data import level_data

# — Page setup —
st.set_page_config(page_title="🎮 100-Level Image Game", layout="centered")
st.title("🎮 100-Level Image Game")

# — Auth helpers —
def logout():
    if st.sidebar.button("🚪 Log out"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

def restart_game():
    if st.sidebar.button("🔄 Restart Game"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.scored_levels = set()
        st.session_state.show_answer_remaining = 3
        st.session_state.correct_answer = False
        st.session_state.show_answer_now = False
        st.session_state.max_unlocked_level = 1
        update_user_progress(st.session_state.user_id, 1, 0)
        st.rerun()

def jump_to_level():
    target = st.session_state.jump_level
    if 1 <= target <= st.session_state.max_unlocked_level:
        st.session_state.level = target
        st.session_state.correct_answer = False
        st.session_state.show_answer_now = False
        st.rerun()

# — Login / Signup —
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
            # initialize game state
            st.session_state.scored_levels         = set()
            st.session_state.show_answer_remaining = 3
            st.session_state.correct_answer        = False
            st.session_state.show_answer_now       = False
            st.session_state.max_unlocked_level    = st.session_state.level
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# — Game state —
uid   = st.session_state.user_id
user  = st.session_state.username
lvl   = st.session_state.level
score = st.session_state.score

# ensure max_unlocked_level is always set
if "max_unlocked_level" not in st.session_state:
    st.session_state.max_unlocked_level = lvl

# — Sidebar controls —
logout()
restart_game()

st.sidebar.markdown("### Jump to Level")
st.sidebar.selectbox(
    "Select level:",
    options=list(range(1, st.session_state.max_unlocked_level + 1)),
    key="jump_level",
    on_change=jump_to_level
)

st.sidebar.markdown(f"👤 **{user}**")
st.sidebar.markdown(f"⭐ **Score:** {score}")
st.sidebar.markdown(f"🏁 **Current:** Level {lvl}")
st.sidebar.markdown(f"🔍 **Show‐Answer Left:** {st.session_state.show_answer_remaining}")

# — Load level data —
info = level_data.get(lvl)
if not info:
    st.balloons()
    st.success("🎉 You've completed all 100 levels!")
    st.stop()

# — Display image —
if st.session_state.correct_answer or st.session_state.show_answer_now:
    img_url = info.get("answer_image_url", "").strip()
else:
    img_url = info.get("image_url", "").strip()

if img_url:
    try:
        st.image(img_url, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

st.subheader(f"Level {lvl}")
st.write(info["question"])

# — Capture user answer —
st.text_input("Your Answer", key="user_answer")

# — Handlers —
def submit_answer():
    ans = st.session_state.user_answer.strip().lower()
    valid = info["answer"]
    if isinstance(valid, str):
        valid = [valid]
    valid = [v.strip().lower() for v in valid]
    if ans in valid:
        st.session_state.correct_answer = True
        if lvl not in st.session_state.scored_levels:
            st.session_state.score += 10
            st.session_state.scored_levels.add(lvl)
            update_user_progress(uid, lvl, st.session_state.score)
        # unlock next level
        if lvl == st.session_state.max_unlocked_level and lvl < 100:
            st.session_state.max_unlocked_level += 1
    else:
        st.warning("❌ Wrong answer. Try again!")

def show_answer():
    if st.session_state.show_answer_remaining > 0:
        st.session_state.show_answer_now = True
        st.session_state.show_answer_remaining -= 1
    else:
        st.warning("🚫 No show-answer attempts left!")

def continue_next():
    st.session_state.level += 1
    st.session_state.correct_answer  = False
    st.session_state.show_answer_now = False

def prev_level():
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.session_state.correct_answer  = False
        st.session_state.show_answer_now = False
    else:
        st.warning("You're already at level 1.")

# — Buttons —
st.button("Submit Answer", on_click=submit_answer)
st.button("Show Answer", on_click=show_answer, disabled=(st.session_state.show_answer_remaining==0))

c1, c2 = st.columns(2)
with c1:
    if st.session_state.correct_answer or st.session_state.show_answer_now:
        st.button("Continue to Next Level", on_click=continue_next)
with c2:
    st.button("⬅️ Previous Level", on_click=prev_level)
