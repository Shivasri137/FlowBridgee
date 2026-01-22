import streamlit as st
import requests
from utils.db import add_task, fetch_all_tasks, complete_task

def decompose_task_with_phi3(task_name):
    url = "http://localhost:11434/api/generate"
    prompt = f"Decompose this task into a concise numbered list of sub-tasks: {task_name}"
    
    payload = {"model": "phi3", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json().get("response", "Decomposition failed.")
    except:
        return "Error: Ensure Ollama is running."

def run():
    st.subheader(" Task Decomposer Agent")

    # --- INPUT SECTION ---
    task_input = st.text_input("What project do you want to break down?")
    if st.button("Decompose & Add"):
        if task_input.strip():
            with st.spinner("Phi-3 is thinking..."):
                decomposition = decompose_task_with_phi3(task_input)
                # Save the first line as title, rest as sub-tasks
                formatted_task = f"### {task_input}\n{decomposition}"
                add_task(formatted_task)
                st.success("Added to-do list!")
                st.rerun()

    st.divider()

    # --- DYNAMIC LIST SECTION ---
    st.subheader("Current Projects")
    tasks = fetch_all_tasks()

    if not tasks:
        st.info("No active tasks.")
        return

    for task in tasks:
        # Unpack based on your DB structure (id, content, status, ...)
        task_id, content, status, created_at, completed_at = task

        # Dynamic Styling based on Status
        is_completed = (status == "Completed")
        status_color = "green" if is_completed else "orange"
        
        with st.expander(f"{'Done' if is_completed else 'Pending'} {content.splitlines()[0][:50]}...", expanded=not is_completed):
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(content)
                # Visual Dynamic Status Tag
                st.markdown(f"**Status:** :{status_color}[{status}]")

            with col2:
                if not is_completed:
                    if st.button("Finish", key=f"btn_{task_id}"):
                        complete_task(task_id) # Updates status to 'Completed' in DB
                        st.rerun() # Forces UI to refresh and show new status
                else:
                    st.button("Done", key=f"btn_{task_id}", disabled=True)