import streamlit as st
from ui.agent_selector import run
from utils.db import init_db

st.set_page_config(
    page_title="Flow Bridge",
    layout="wide"
)

if __name__ == "__main__":
    init_db()   # <-- runs once, safe every time
    run()
