import streamlit as st
from handle import update_user_progress
from level_data import level_data

def init_flags():
    for flag in ("correct_answer", "show_answer_now", "scored_current_level"):
        if flag not in st.session_state:
            st.session_state[flag] = False

def handle_answer_submission():
    info = level_data[st.session_state.level]
    ans  = st.session_state.user_answer.strip().lower()
    if ans == info["answer"]:
        st.session_state.correct_answer = True
        # award points once
        if not st.session_state.scored_current_level:
            st.session_state.score += 10
            update_user_progress(
                st.session_state.user_id,
                st.session_state.level,
                st.session_state.score
            )
            st.session_state.scored_current_level = True
    else:
        st.warning("❌ Wrong answer. Try again!")

def show_answer_callback():
    st.session_state.show_answer_now = True

def continue_to_next_level():
    st.session_state.level += 1
    # reset flags for new level
    st.session_state.correct_answer       = False
    st.session_state.show_answer_now      = False
    st.session_state.scored_current_level = False
    update_user_progress(
        st.session_state.user_id,
        st.session_state.level,
        st.session_state.score
    )

def go_back_to_previous_level():
    lvl = st.session_state.level
    if lvl > 1:
        st.session_state.level -= 1
        st.session_state.correct_answer       = False
        st.session_state.show_answer_now      = False
        st.session_state.scored_current_level = False
    else:
        st.warning("You're already at the first level!")

def render_level():
    init_flags()
    lvl  = st.session_state.level
    info = level_data.get(lvl)

    if not info:
        st.balloons()
        st.success("🎉 You've completed all 100 levels!")
        st.stop()

    st.subheader(f"Level {lvl}")

    # pick which image to show
    if st.session_state.correct_answer or st.session_state.show_answer_now:
        img = info.get("answer_image_url", "")
    else:
        img = info.get("image_url", "")

    if img:
        try:
            st.image(img, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.warning("⚠️ No image URL provided for this level.")

    st.write(info["question"])

    # store the user's answer in session state
    st.text_input("Your Answer", key="user_answer")

    # these callbacks now fire instantly
    st.button("Submit Answer", on_click=handle_answer_submission)
    st.button("Show Answer",   on_click=show_answer_callback)

    # navigation
    c1, c2 = st.columns(2)
    with c1:
        if (st.session_state.correct_answer or st.session_state.show_answer_now):
            st.button("Continue to Next Level", on_click=continue_to_next_level)
    with c2:
        st.button("⬅️ Previous Level", on_click=go_back_to_previous_level)
