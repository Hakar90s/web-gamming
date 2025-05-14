st.subheader(f"Level {level}")

level_info = level_data.get(level)

# State flag to show answer image
if "show_answer_image" not in st.session_state:
    st.session_state.show_answer_image = False

# Show either question image or answer image
if st.session_state.show_answer_image:
    st.image(level_info["answer_image_url"], caption="Answer Image", use_container_width=True)
else:
    st.image(level_info["image_url"], caption="Question Image", use_container_width=True)

st.write(level_info["question"])
user_answer = st.text_input("Your Answer").strip().lower()

def handle_answer_submission():
    """Handle the submission of the user's answer."""
    if user_answer == level_info["answer"]:
        st.success("✅ Correct!")
        st.session_state.show_answer_image = True  # Show answer image
    else:
        st.warning("❌ Wrong answer. Try again!")

def show_answer():
    """Show answer image."""
    st.session_state.show_answer_image = True

def continue_to_next_level():
    """Go to next level and reset answer image flag."""
    st.session_state.level += 1
    st.session_state.score += 10
    st.session_state.show_answer_image = False
    update_user_progress(user_id, st.session_state.level, st.session_state.score)
    st.rerun()

def go_back_to_previous_level():
    if level > 1:
        st.session_state.level -= 1
        st.session_state.show_answer_image = False
        st.rerun()
    else:
        st.warning("You're already at level 1.")

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Submit Answer"):
        handle_answer_submission()

with col2:
    if st.button("Show Answer"):
        show_answer()

with col3:
    if st.button("Continue to Next Level"):
        continue_to_next_level()

if st.button("Go Back to Previous Level"):
    go_back_to_previous_level()
