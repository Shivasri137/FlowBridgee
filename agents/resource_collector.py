import streamlit as st
import json
from duckduckgo_search import DDGS

PROGRESS_PATH = "data/user_data/progress.json"


def load_pending_topics():
    try:
        with open(PROGRESS_PATH, "r") as f:
            progress = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    pending = []
    for subject, topics in progress.items():
        for topic, status in topics.items():
            if status.lower() != "completed":
                pending.append(f"{topic} {subject}")

    return pending


def search_resources(query, max_results=5):
    results = {"Blogs": [], "YouTube": [], "PDFs": []}

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=20):
            link = r.get("href", "").lower()
            title = r.get("title", "")
            desc = r.get("body", "")

            if "youtube.com" in link or "youtu.be" in link:
                results["YouTube"].append((title, r["href"], desc))
            elif link.endswith(".pdf"):
                results["PDFs"].append((title, r["href"], desc))
            else:
                results["Blogs"].append((title, r["href"], desc))

            if all(len(v) >= max_results for v in results.values()):
                break

    return results


def run():
    st.subheader("Resource Collector Agent")

    pending_topics = load_pending_topics()

    if pending_topics:
        selected_topic = st.selectbox(
            "Your Pending Topics (from Mentor Agent)",
            pending_topics
        )
    else:
        selected_topic = ""

    topic = st.text_input("Search Topic", value=selected_topic)

    if st.button("Find Resources"):
        if not topic.strip():
            st.warning("Please enter a topic.")
            return

        with st.spinner("Searching resources..."):
            results = search_resources(topic)

        for category, items in results.items():
            st.subheader(category)
            if not items:
                st.info("No results found.")
            for title, link, desc in items:
                st.markdown(f"**{title}**")
                st.markdown(f"[Open]({link})")
                if desc:
                    st.caption(desc)
                st.markdown("---")
