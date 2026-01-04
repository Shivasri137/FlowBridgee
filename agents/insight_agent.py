import streamlit as st
import pandas as pd
from utils.db import fetch_all_tasks

def run():
    st.subheader("Insight Agent (Professional Productivity)")

    tasks = fetch_all_tasks()

    if not tasks:
        st.info("No task data available yet.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(
        tasks,
        columns=["ID", "Task Name", "Status", "Created At", "Completed At"]
    )

    total_tasks = len(df)
    completed_tasks = len(df[df["Status"] == "Completed"])
    pending_tasks = len(df[df["Status"] == "Pending"])

    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks else 0

    # KPI Section
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed", completed_tasks)
    col3.metric("Pending", pending_tasks)
    col4.metric("Completion Rate (%)", f"{completion_rate:.1f}")

    st.divider()

    # Chart
    chart_data = pd.DataFrame({
        "Status": ["Completed", "Pending"],
        "Count": [completed_tasks, pending_tasks]
    })

    st.subheader("Task Status Overview")
    st.bar_chart(chart_data.set_index("Status"))

    st.divider()

    # Insights (Rule-based)
    st.subheader("Insights & Recommendations")

    if completion_rate < 40:
        st.warning(
            "Your task completion rate is low. Consider reducing task load or improving prioritization."
        )
    elif completion_rate < 70:
        st.info(
            "You are making steady progress. Try focusing on completing pending tasks consistently."
        )
    else:
        st.success(
            "Great job! You are completing most of your tasks on time. Maintain this consistency."
        )
