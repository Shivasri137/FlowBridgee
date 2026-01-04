import streamlit as st
import json
import os
from datetime import date, datetime

MEETINGS_PATH = "data/user_data/meetings.json"


def load_meetings():
    try:
        with open(MEETINGS_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_meetings(meetings):
    os.makedirs("data/user_data", exist_ok=True)
    with open(MEETINGS_PATH, "w") as f:
        json.dump(meetings, f, indent=2)


def run():
    st.subheader("Meeting Scheduler Agent (Professional)")

    st.write(
        "Schedule meetings, track upcoming sessions, and avoid meeting overload."
    )

    # -------- Schedule Meeting --------
    st.subheader("Schedule a New Meeting")

    title = st.text_input("Meeting Title")
    meeting_date = st.date_input("Meeting Date", min_value=date.today())
    meeting_time = st.time_input("Meeting Time")
    duration = st.number_input(
        "Duration (minutes)", min_value=15, max_value=240, step=15
    )

    if st.button("Schedule Meeting"):
        if not title.strip():
            st.warning("Please enter meeting title.")
            return

        meetings = load_meetings()

        meetings.append({
            "title": title,
            "date": str(meeting_date),
            "time": meeting_time.strftime("%H:%M"),
            "duration": duration
        })

        save_meetings(meetings)
        st.success("Meeting scheduled successfully.")

    # -------- View Meetings --------
    st.divider()
    st.subheader("Your Meetings")

    meetings = load_meetings()

    if not meetings:
        st.info("No meetings scheduled yet.")
        return

    today = date.today()
    upcoming = []
    past = []

    for m in meetings:
        m_date = datetime.strptime(m["date"], "%Y-%m-%d").date()
        if m_date >= today:
            upcoming.append(m)
        else:
            past.append(m)

    # Upcoming Meetings
    st.markdown("### Upcoming Meetings")
    for m in sorted(upcoming, key=lambda x: (x["date"], x["time"])):
        st.write(
            f"**{m['title']}** — {m['date']} at {m['time']} "
            f"({m['duration']} mins)"
        )

    # Past Meetings
    if past:
        st.divider()
        st.markdown("### Past Meetings")
        for m in sorted(past, key=lambda x: (x["date"], x["time"]), reverse=True):
            st.write(
                f"{m['title']} — {m['date']} at {m['time']}"
            )

    # -------- Simple Insights --------
    st.divider()
    st.subheader("Meeting Insights")

    today_meetings = [
        m for m in meetings
        if m["date"] == str(today)
    ]

    total_duration_today = sum(m["duration"] for m in today_meetings)

    st.write(f"Meetings today: {len(today_meetings)}")
    st.write(f"Total meeting time today: {total_duration_today} minutes")

    if total_duration_today > 180:
        st.warning(
            "You have heavy meeting load today. Consider protecting focus time."
        )
    elif total_duration_today == 0:
        st.success(
            "No meetings today. Good opportunity for deep work."
        )
    else:
        st.info(
            "Meeting load today looks manageable."
        )
