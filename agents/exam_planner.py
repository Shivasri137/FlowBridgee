import streamlit as st
import pandas as pd
import json
import os
import requests
import re # Added for robust parsing
from datetime import date, timedelta

# File Paths
SCHEDULES_PATH = "data/user_data/schedules.json"

def call_phi3(prompt, is_json=False):
    """Calls Ollama Phi-3 with robust JSON extraction for both Lists and Objects."""
    url = "http://localhost:11434/api/generate"
    payload = {"model": "phi3", "prompt": prompt, "stream": False}
    if is_json:
        payload["format"] = "json"
    
    try:
        response = requests.post(url, json=payload, timeout=120) 
        response.raise_for_status()
        raw_text = response.json().get("response", "")
        
        if is_json:
            # Finds either [...] or {...} to handle both list and object responses
            match = re.search(r'(\[.*\]|\{.*\})', raw_text, re.DOTALL)
            if match:
                clean_json = match.group(0)
                # Fix common AI formatting errors
                clean_json = re.sub(r',\s*\]', ']', clean_json)
                clean_json = re.sub(r',\s*\}', '}', clean_json)
                return json.loads(clean_json)
            else:
                return json.loads(raw_text)
        return raw_text
    except Exception as e:
        st.error(f"Ollama/Parsing Error: {e}")
        return None

def run():
    st.title(" Smart AI Exam Planner")

    tab1, tab2 = st.tabs([" Active Plan & Tracker", " Create New Plan"])

    # --- TAB 2: CREATE NEW PLAN ---
    with tab2:
        st.subheader("Generate AI Study Schedule")
        with st.form("generation_form"):
            subject = st.text_input("Subject Name", placeholder="e.g., Business Intelligence")
            exam_date = st.date_input("Exam Date", min_value=date.today() + timedelta(days=1))
            syllabus_text = st.text_area("Paste Syllabus (Units & Topics)", height=200)
            generate_btn = st.form_submit_button("Generate Smart Plan")

            if generate_btn and subject and syllabus_text:
                days_left = (exam_date - date.today()).days
                with st.spinner("Agent is processing your syllabus..."):
                    prompt = f"""
                    Create a {days_left}-day study plan for {subject}.
                    Syllabus: {syllabus_text}
                    Assign each day a specific practical time slot (e.g. 10 AM - 12 PM).
                    Return ONLY a JSON list of objects: 
                    [{{"day": 1, "time": "09:00 AM - 11:00 AM", "topic": "Topic Name", "focus": "key concept"}}]
                    """
                    ai_plan = call_phi3(prompt, is_json=True)

                if ai_plan and isinstance(ai_plan, list):
                    schedule_data = []
                    for entry in ai_plan:
                        if isinstance(entry, dict):
                            day_num = int(entry.get("day", 1)) - 1
                            plan_date = date.today() + timedelta(days=day_num)
                            
                            schedule_data.append({
                                "Date": str(plan_date),
                                "Time": entry.get("time", "TBD"),
                                "Topic": entry.get("topic", "Revision"),
                                "Focus": entry.get("focus", "General Study"),
                                "Status": "Pending"
                            })
                    
                    os.makedirs(os.path.dirname(SCHEDULES_PATH), exist_ok=True)
                    with open(SCHEDULES_PATH, "w") as f:
                        json.dump(schedule_data, f, indent=2)
                    st.success("Plan generated successfully!")
                    st.rerun()

    # --- TAB 1: ACTIVE PLAN & TRACKER ---
    with tab1:
        if not os.path.exists(SCHEDULES_PATH):
            st.info("No active plan. Create one in the next tab!")
            return

        with open(SCHEDULES_PATH, "r") as f:
            full_schedule = json.load(f)
        
        df = pd.DataFrame(full_schedule)
        
        if "Status" in df.columns:
            c1, c2, c3 = st.columns(3)
            c1.metric("Completed", len(df[df['Status'] == 'Completed']))
            c2.metric("Incomplete", len(df[df['Status'] == 'Incomplete']))
            c3.metric("Pending", len(df[df['Status'] == 'Pending']))

        st.table(df[["Date", "Time", "Topic", "Focus", "Status"]])
        st.divider()

        # --- MCQ QUIZ LOGIC ---
        st.subheader(" Topic Validation (MCQ)")
        target_topics = [t["Topic"] for t in full_schedule if t.get("Status") != "Completed"]

        if target_topics:
            selected_topic = st.selectbox("Validate mastery for:", target_topics)
            
            if st.button("Generate Quiz"):
                with st.spinner("Generating MCQ..."):
                    mcq_prompt = f"""
                    Generate one technical MCQ for: {selected_topic}.
                    Return ONLY JSON: {{"question": "...", "options": ["A", "B", "C", "D"], "answer": "exact_text"}}
                    The "answer" must match one of the options exactly.
                    """
                    st.session_state.quiz_data = call_phi3(mcq_prompt, is_json=True)
                    st.session_state.quiz_active_topic = selected_topic

            if "quiz_data" in st.session_state and st.session_state.quiz_active_topic == selected_topic:
                q = st.session_state.quiz_data
                if q and isinstance(q, dict):
                    st.write(f"**Question:** {q.get('question')}")
                    
                    # --- FIX: ROBUST OPTION SPLITTING ---
                    raw_options = q.get('options', [])
                    if len(raw_options) == 1:
                        processed_options = re.split(r'\s(?=[A-D][\.\)])', raw_options[0])
                    else:
                        processed_options = raw_options

                    choice = st.radio("Select Answer:", processed_options, index=None, key="mcq_radio")
                    
                    if st.button("Check Answer"):
                        if choice:
                            # --- DYNAMIC MATCHING LOGIC ---
                            user_choice = str(choice).strip().lower()
                            correct_answer = str(q.get('answer')).strip().lower()

                            # Matches if equal, if choice is in answer, or if answer is in choice
                            is_correct = (
                                user_choice == correct_answer or 
                                user_choice in correct_answer or 
                                correct_answer in user_choice
                            )

                            if is_correct:
                                st.success(" Correct! Status updated.")
                                for item in full_schedule:
                                    if item["Topic"] == selected_topic: 
                                        item["Status"] = "Completed"
                                
                                with open(SCHEDULES_PATH, "w") as f: 
                                    json.dump(full_schedule, f, indent=2)
                                
                                if "quiz_data" in st.session_state:
                                    del st.session_state.quiz_data
                                st.rerun()
                            else:
                                st.error(f" Wrong. Correct answer: {q.get('answer')}")
                                for item in full_schedule:
                                    if item["Topic"] == selected_topic: 
                                        item["Status"] = "Incomplete"
                                
                                with open(SCHEDULES_PATH, "w") as f: 
                                    json.dump(full_schedule, f, indent=2)
                                st.rerun()
                        else:
                            st.warning("Please select an option first!")
        else:
            st.balloons()
            st.success("Syllabus Completed!")

        if st.button("Reset Plan"):
            if os.path.exists(SCHEDULES_PATH): os.remove(SCHEDULES_PATH)
            st.rerun()

if __name__ == "__main__":
    run()