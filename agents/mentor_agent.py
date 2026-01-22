import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import date

# File Paths
SCHEDULES_PATH = "data/user_data/schedules.json"
PROGRESS_PATH = "data/user_data/progress.json"

def get_phi3_guidance(completed, pending, days_left):
    url = "http://localhost:11434/api/generate"
    prompt = f"Student progress: {completed} done, {pending} left, {days_left} days to exam. Give 2 lines of strategy."
    try:
        response = requests.post(url, json={"model": "phi3", "prompt": prompt, "stream": False}, timeout=5)
        return response.json().get("response", "Stay focused!")
    except:
        return "Keep consistent! Every topic completed is a step toward success."

def load_data(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def run():
    st.subheader(" AI Mentor & Progress Insight")

    schedule = load_data(SCHEDULES_PATH)
    if not schedule:
        st.info("No study data found. Please generate a plan in the **Exam Planner** first.")
        return

    # --- 1. CALCULATE STATS ---
    total_topics = len(schedule)
    completed_topics = sum(1 for t in schedule if t.get("Status") == "Completed")
    pending_topics = total_topics - completed_topics
    
    # Get exam date safely
    try:
        exam_date = date.fromisoformat(schedule[-1]["Date"])
        days_to_exam = (exam_date - date.today()).days
    except:
        days_to_exam = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Done", f"{completed_topics}")
    col2.metric("Pending", f"{pending_topics}")
    col3.metric("Days Left", f"{max(0, days_to_exam)}")

    # --- 2. AI ADVICE ---
    st.divider()
    with st.chat_message("assistant"):
        advice = get_phi3_guidance(completed_topics, pending_topics, days_to_exam)
        st.write(advice)

    # --- 3. VISUAL INSIGHTS ---
    
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    
    # Pie Chart
    ax[0].pie([completed_topics, max(0.1, pending_topics)], 
              labels=['Done', 'Pending'], 
              autopct='%1.1f%%', 
              colors=['#2ecc71', '#e74c3c'])
    ax[0].set_title("Completion Rate")

    # Bar Chart
    ax[1].bar(["Total", "Pending"], [total_topics, pending_topics], color=['#3498db', '#f1c40f'])
    ax[1].set_title("Workload Volume")
    st.pyplot(fig)

    # --- 4. FIXED PENDING TOPICS TABLE ---
    st.divider()
    st.subheader(" Upcoming Tasks")
    
    pending_list = [t for t in schedule if t.get("Status") == "Pending"]
    
    if pending_list:
        df_pending = pd.DataFrame(pending_list)
        
        # --- FIX: Only show columns that actually exist ---
        available_cols = ["Date", "Topic", "Focus"]
        existing_cols = [c for c in available_cols if c in df_pending.columns]
        
        st.table(df_pending[existing_cols].head(5))
    else:
        st.success("All tasks completed! Time for revision.")