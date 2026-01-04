import streamlit as st
from utils.db import add_task, fetch_all_tasks, complete_task

def run():
    st.subheader("Task Decomposer Agent (Professional)")

    task_name = st.text_input("Enter a new task")

    if st.button("Add Task"):
        if task_name.strip():
            add_task(task_name)
            st.success("Task added successfully")
        else:
            st.warning("Task name cannot be empty")

    st.divider()
    st.subheader("Your Tasks")

    tasks = fetch_all_tasks()

    if not tasks:
        st.info("No tasks found.")
        return

    for task in tasks:
        task_id, name, status, created_at, completed_at = task

        col1, col2, col3 = st.columns([4, 2, 2])

        col1.write(name)
        col2.write(status)

        if status == "Pending":
            if col3.button("Mark Completed", key=f"complete_{task_id}"):
                complete_task(task_id)
                st.experimental_rerun()
        else:
            col3.write("Done")
