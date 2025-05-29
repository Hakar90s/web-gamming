import streamlit as st
from handle import update_user_progress
from level_data import level_data

def init_flags():
    for flag in ("correct_answer","show_answer_now","scored_current_level"):
        if flag not in st.session_state:
            st.session_state[flag] = False

def handle_answer_submission():
    info = level_data[st.session_state.level]
    ans  = st.session_state.user_answer.strip().lower()
    valid = info["answer"]
    if isinstance(valid, str):
        valid = [valid]
    valid = [v.strip().lower() for v in valid]

    if ans in valid:
        st.session_state.correct_answer = True
        if st.session_state.level not in st.session_state.scored_levels:
            st.session_state.score += 10
            st.session_state.scored_levels.add(st.session_state.level)
            update_user_progress(
                st.session_state.user_id,
                st.session_state.level,
                st.session_state.score
            )
        # unlock next level immediately
        if (st.session_state.level == st.session_state.max_unlocked_level
            and st.session_state.level < len(level_data)):
            st.session_state.max_unlocked_level += 1
    else:
        st.warning("❌ Wrong answer. Try again!")

def show_answer_callback():
    if st.session_state.show_answer_remaining > 0:
        st.session_state.show_answer_now       = True
        st.session_state.show_answer_remaining -= 1
    else:
        st.warning("🚫 No show-answer attempts left!")

def continue_next():
    st.session_state.level += 1
    # unlock if needed
    if st.session_state.level > st.session_state.max_unlocked_level:
        st.session_state.max_unlocked_level = st.session_state.level
    st.session_state.correct_answer  = False
    st.session_state.show_answer_now = False

def prev_level():
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.session_state.correct_answer  = False
        st.session_state.show_answer_now = False
    else:
        st.warning("🚫 Already at level 1.")

def render_level():
    init_flags()
    lvl  = st.session_state.level
    info = level_data.get(lvl)

    # — end-of-game —
    if not info:
        st.balloons()
        st.success(
            f"🎉 Congratulations {st.session_state.username}!  "
            f"You’ve completed all {len(level_data)} levels  "
            f"with a score of {st.session_state.score}!"
        )
        st.stop()

    # — normal level render —
    st.subheader(f"Level {lvl}")

    # choose image
    img = (info["answer_image_url"] 
           if (st.session_state.correct_answer or st.session_state.show_answer_now)
           else info["image_url"])
    if img.strip():
        st.image(img.strip(), use_container_width=True)

    st.write(info["question"])
    st.text_input("Your Answer", key="user_answer")

    st.button("Submit Answer", on_click=handle_answer_submission)
    st.button("Show Answer",    on_click=show_answer_callback,
                               disabled=(st.session_state.show_answer_remaining==0))

    c1, c2 = st.columns(2)
    with c1:
        if (st.session_state.correct_answer or st.session_state.show_answer_now):
            st.button("Continue to Next Level", on_click=continue_next)
    with c2:
        st.button("⬅️ Previous Level", on_click=prev_level)
