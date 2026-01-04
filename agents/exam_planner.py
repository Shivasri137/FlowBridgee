import streamlit as st
import pandas as pd
import json
import os
from datetime import date, timedelta

SCHEDULES_PATH = "data/user_data/schedules.json"
PROGRESS_PATH = "data/user_data/progress.json"


def extract_topics(syllabus_text):
    """
    Converts full syllabus text into individual topics.
    Each non-empty line is treated as a study unit.
    """
    lines = syllabus_text.split("\n")
    topics = [line.strip() for line in lines if line.strip()]
    return topics


def save_schedule(schedule):
    os.makedirs("data/user_data", exist_ok=True)
    with open(SCHEDULES_PATH, "w") as f:
        json.dump(schedule, f, indent=2, default=str)


def initialize_progress(subject, topics):
    """
    Initializes progress.json with all topics marked as Pending.
    """
    os.makedirs("data/user_data", exist_ok=True)

    progress = {}
    if os.path.exists(PROGRESS_PATH):
        try:
            with open(PROGRESS_PATH, "r") as f:
                progress = json.load(f)
        except json.JSONDecodeError:
            progress = {}

    progress[subject] = {}
    for topic in topics:
        progress[subject][topic] = "Pending"

    with open(PROGRESS_PATH, "w") as f:
        json.dump(progress, f, indent=2)


def run():
    st.subheader("Exam Planner Agent (Whole Syllabus Based)")

    subject = st.text_input("Subject Name")

    syllabus_text = st.text_area(
        "Paste Full Syllabus",
        placeholder=(
            "Unit 1: Algebra\n"
            "Linear Equations\n"
            "Quadratic Equations\n"
            "Unit 2: Trigonometry\n"
            "Basic Identities\n"
            "Heights and Distances\n"
            "Unit 3: Calculus\n"
            "Limits\n"
            "Derivatives"
        ),
        height=250
    )

    exam_date = st.date_input("Exam Date", min_value=date.today())
    hours_per_day = st.number_input(
        "Study hours per day",
        min_value=1,
        max_value=8,
        value=2
    )

    if st.button("Generate Study Plan"):
        if not subject.strip():
            st.error("Please enter subject name.")
            return

        topics = extract_topics(syllabus_text)
        days_left = (exam_date - date.today()).days

        if not topics:
            st.error("Please paste the syllabus.")
            return

        if days_left <= 0:
            st.error("Exam date must be in the future.")
            return

        plan = []
        schedule_json = []
        current_date = date.today()
        topic_index = 0

        for day in range(days_left):
            if topic_index < len(topics):
                topic = topics[topic_index]
                task_type = "Concept Learning"
                topic_index += 1
            else:
                topic = "Revision / Practice"
                task_type = "Revision"

            entry = {
                "Date": str(current_date),
                "Subject": subject,
                "Topic": topic,
                "Task Type": task_type,
                "Duration (hrs)": hours_per_day,
                "Status": "Pending"
            }

            plan.append(entry)
            schedule_json.append(entry)
            current_date += timedelta(days=1)

        # Save schedule
        save_schedule(schedule_json)

        # Initialize progress tracking
        initialize_progress(subject, topics)

        df = pd.DataFrame(plan)

        st.success("Whole Syllabus Study Plan Generated and Linked to Mentor Agent")
        st.dataframe(df, use_container_width=True)
