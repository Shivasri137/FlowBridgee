import streamlit as st
import json
from datetime import date
import matplotlib.pyplot as plt

PROGRESS_PATH = "data/user_data/progress.json"


def load_progress():
    try:
        with open(PROGRESS_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def run():
    st.subheader("Mentor Agent (Guidance, Reminders & Progress Tracking)")

    st.write(
        "This mentor guides your preparation, reminds pending syllabus topics, "
        "and visually tracks your progress."
    )

    exam_date = st.date_input("Exam Date", min_value=date.today())

    confidence = st.selectbox(
        "How confident do you feel?",
        ["Very low", "Low", "Moderate", "High"]
    )

    if st.button("Get Mentor Advice"):
        days_left = (exam_date - date.today()).days

        # ---------------- Motivation ----------------
        st.subheader("Mentor Feedback")

        if days_left > 30:
            st.info("You have enough time. Focus on consistency and concept clarity.")
        elif 10 < days_left <= 30:
            st.warning("Time is limited. Prioritize pending topics and revision.")
        else:
            st.error("Exam is very near. Focus on revision and weak areas only.")

        if confidence in ["Very low", "Low"]:
            st.info("Low confidence is normal. Progress comes from completing pending topics.")
        else:
            st.success("Your confidence level is good. Maintain momentum.")

        # ---------------- Progress Analysis ----------------
        st.divider()
        st.subheader("Syllabus Progress Overview")

        progress = load_progress()

        completed = 0
        pending = 0
        pending_topics = []

        for subject, topics in progress.items():
            for topic, status in topics.items():
                if str(status).lower() == "completed":
                    completed += 1
                else:
                    pending += 1
                    pending_topics.append((subject, topic))

        total = completed + pending

        if total == 0:
            st.info("No syllabus progress found yet. Generate a study plan first.")
            return

        # ---------------- Line Graph ----------------
        fig, ax = plt.subplots()

        ax.plot(
            ["Start", "Current"],
            [total, pending],
            marker="o",
            label="Pending Topics"
        )

        ax.plot(
            ["Start", "Current"],
            [0, completed],
            marker="o",
            label="Completed Topics"
        )

        ax.set_title("Syllabus Progress Trend")
        ax.set_ylabel("Number of Topics")
        ax.legend()

        st.pyplot(fig)

        # ---------------- Pending Topics ----------------
        st.divider()
        st.subheader("Pending Syllabus Topics")

        if not pending_topics:
            st.success("Excellent! All syllabus topics are completed.")
        else:
            st.warning(f"{pending} topics are still pending:")

            for subject, topic in pending_topics[:5]:
                st.write(f"- **{subject}** → {topic}")

            if pending > 5:
                st.caption("Focus on completing these before starting new topics.")

        # ---------------- Final Message ----------------
        st.divider()
        st.subheader("Mentor Message")

        st.write(
            "Progress is not about speed, it is about direction. "
            "Complete pending topics step by step — confidence will follow."
        )
