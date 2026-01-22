import streamlit as st
import json
import os
import re
import urllib.parse
from duckduckgo_search import DDGS

# Path must match your Exam Planner's data storage
SCHEDULES_PATH = "data/user_data/schedules.json"

def load_pending_topics():
    """Extracts pending topics from the exam planner for searching."""
    if not os.path.exists(SCHEDULES_PATH):
        return []
    try:
        with open(SCHEDULES_PATH, "r") as f:
            data = json.load(f)
            # Clean topic names (removing parentheses and unit numbers)
            topics = [re.sub(r'\(.*?\)|Unit\s?\d+', '', t["Topic"]).strip() 
                      for t in data if t.get("Status") != "Completed"]
            return list(set(filter(None, topics)))
    except Exception:
        return []

def get_links(query, platform="blog"):
    """Fetches direct links with timeout protection and specific site targeting."""
    if platform == "youtube":
        final_query = f"{query} site:youtube.com"
    elif platform == "pdf":
        final_query = f"{query} filetype:pdf study notes"
    else:
        # Targets specific high-quality educational sites
        final_query = f"{query} tutorial (site:geeksforgeeks.org OR site:w3schools.com OR site:tutorialspoint.com)"

    results = []
    try:
        # 'lite' backend is stable and fast
        with DDGS(timeout=15) as ddgs:
            resp = ddgs.text(final_query, backend="lite", max_results=5)
            for r in resp:
                results.append({
                    "title": r.get("title"),
                    "link": r.get("href"),
                    "snippet": r.get("body")
                })
    except Exception:
        return []
    return results

def run():
    """The main entry point called by the Dashboard."""
    st.subheader("Resource Collector Agent")

    # 1. Topic Syncing
    pending = load_pending_topics()
    selected = st.selectbox("Select Topic from Syllabus:", pending) if pending else ""
    query = st.text_input("Confirm Topic:", value=selected)

    if st.button("Find Resources"):
        if not query:
            st.warning("Please select a topic.")
            return

        # Prepare encoded URL for the fallback buttons
        encoded_query = urllib.parse.quote(query)

        # 2. Results Tabs
        t_blog, t_yt, t_pdf = st.tabs([" Articles", " Videos", " PDFs"])

        with t_blog:
            items = get_links(query, "blog")
            if items:
                display_items(items)
            else:
                st.info("No direct articles found.")
                st.link_button(" Search Articles on Google", f"https://www.google.com/search?q={encoded_query}+tutorial")

        with t_yt:
            items = get_links(query, "youtube")
            if items:
                display_items(items)
            else:
                st.info("No direct videos found.")
                st.link_button(" Search on YouTube", f"https://www.youtube.com/results?search_query={encoded_query}")

        with t_pdf:
            # PDFs are working well, but added a fallback just in case
            items = get_links(query, "pdf")
            display_items(items)

def display_items(items):
    """Helper to display results neatly."""
    if not items:
        st.info("No direct links found.")
        return
    for item in items:
        st.markdown(f"#### [{item['title']}]({item['link']})")
        st.write(item['snippet'])
        st.caption(f"Direct Link: {item['link']}")
        st.divider()