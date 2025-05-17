import streamlit as st
from auth import login_flow, logout_button
from game import init_flags, render_level
from ui import show_sidebar

# page config
st.set_page_config(page_title="🎮 100-Level Image Game", layout="centered")
st.title("🎮 100-Level Image Game")

# Authentication
login_flow()
logout_button()

# Game
init_flags()
render_level()

# Sidebar
show_sidebar()
