import streamlit as st
from handle import update_user_progress
from level_data import level_data

TOTAL_LEVELS = len(level_data)  # should be 15

def init_flags():
    """Initialize per‐level flags in session state."""
    for flag in ("correct_answer", "show_answer_now", "scored_current_level"):
        if flag not in st.session_state:
            st.session_state[flag] = False

def handle_answer_submission():
    """Check the user's answer against one or more valid answers."""
    lvl = st.session_state.level
    info = level_data[lvl]
    user_ans = st.session_state.user_answer.strip().lower()

    # Normalize valid answers to a list
    valid = info["answer"]
    if isinstance(valid, str):
        valid = [valid]
    valid = [v.strip().lower() for v in valid]

    if user_ans in valid:
        st.session_state.correct_answer = True
        # Award points only once per level
        if lvl not in st.session_state.scored_levels:
            st.session_state.score += 10
            st.session_state.scored_levels.add(lvl)
            update_user_progress(
                st.session_state.user_id,
                lvl,
                st.session_state.score
            )
        # Unlock next level if this was the max reached
        if lvl == st.session_state.max_unlocked_level and lvl < TOTAL_LEVELS:
            st.session_state.max_unlocked_level += 1
    else:
        st.warning("❌ Wrong answer. Try again!")

def show_answer_callback():
    """Reveal the answer image, consuming one of the three uses."""
    if st.session_state.show_answer_remaining > 0:
        st.session_state.show_answer_now      = True
        st.session_state.show_answer_remaining -= 1
    else:
        st.warning("🚫 No show-answer attempts left!")

def continue_next():
    """Advance to the next level."""
    st.session_state.level += 1
    # Unlock if needed
    if st.session_state.level > st.session_state.max_unlocked_level:
        st.session_state.max_unlocked_level = st.session_state.level
    # Reset flags
    st.session_state.correct_answer  = False
    st.session_state.show_answer_now = False

def prev_level():
    """Go back to the previous level."""
    if st.session_state.level > 1:
        st.session_state.level -= 1
        st.session_state.correct_answer  = False
        st.session_state.show_answer_now = False
    else:
        st.warning("🚫 You're already at level 1.")

def render_level():
    """Render either the current level or the end‐of‐game message."""
    init_flags()
    lvl = st.session_state.level

    # End‐of‐game: if level beyond last, congratulate
    if lvl > TOTAL_LEVELS or lvl not in level_data:
        st.balloons()
        st.success(
            f"🎉 Congratulations, {st.session_state.username}!  \n\n"
            f"You’ve completed all {TOTAL_LEVELS} levels  \n\n"
            f"Your final score is **{st.session_state.score}**!"
        )
        return

    info = level_data[lvl]
    st.subheader(f"Level {lvl}")

    # Pick which image to show
    if st.session_state.correct_answer or st.session_state.show_answer_now:
        img_url = info["answer_image_url"].strip()
    else:
        img_url = info["image_url"].strip()

    if img_url:
        try:
            st.image(img_url, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

    st.write(info["question"])
    st.text_input("Your Answer", key="user_answer")

    # Buttons
    st.button("Submit Answer", on_click=handle_answer_submission)
    st.button(
        "Show Answer",
        on_click=show_answer_callback,
        disabled=(st.session_state.show_answer_remaining == 0)
    )

    # Navigation
    c1, c2 = st.columns(2)
    with c1:
        if st.session_state.correct_answer or st.session_state.show_answer_now:
            st.button("Continue to Next Level", on_click=continue_next)
    with c2:
        st.button("⬅️ Previous Level", on_click=prev_level)
