import streamlit as st

# ------------------ IMPORT AGENTS ------------------
from agents.exam_planner import run as exam_planner_run
from agents.resource_collector import run as resource_collector_run
from agents.doubt_solver import run as doubt_solver_run
from agents.mentor_agent import run as mentor_agent_run

from agents.email_writer import run as email_writer_run
from agents.task_decomposer import run as task_decomposer_run
from agents.meeting_scheduler import run as meeting_scheduler_run
from agents.insight_agent import run as insight_agent_run


# ------------------ GLOBAL CSS ------------------
st.markdown("""
<style>

/* App background */
.main {
    background-color: #fafafa;
}

/* Section titles */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 25px 0 15px 0;
    color: #1f2937;
}

/* Card base */
.card {
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 20px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    transition: transform 0.15s ease-in-out;
}

/* Student cards */
.student {
    background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
    border-left: 6px solid #22c55e;
}

/* Professional cards */
.professional {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
    border-left: 6px solid #6366f1;
}

/* Hover effect */
.card:hover {
    transform: translateY(-2px);
}

/* Agent title */
.agent-title {
    font-size: 18px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 6px;
}

/* Agent description */
.agent-desc {
    font-size: 14px;
    line-height: 1.5;
    color: #4b5563;
    margin-bottom: 12px;
}

/* Button polish */
button[kind="primary"] {
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: 500;
}

/* Divider spacing */
hr {
    margin: 30px 0;
}

</style>
""", unsafe_allow_html=True)


# ------------------ CARD COMPONENT ------------------
def agent_card(title, description, run_fn, css_class, key):
    st.markdown(
        f"""
        <div class="card {css_class}">
            <div class="agent-title">{title}</div>
            <div class="agent-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Open", key=key):
        run_fn()


# ------------------ MAIN UI ------------------
def run():
    st.title("Flow Bridge")

    # -------- LANDING INTRO --------
    st.markdown(
        """
        Flow Bridge is an intelligent, multi-agent platform designed to support both students
        and professionals through structured planning, personalized guidance, and actionable insights.
        The system bridges academic learning and professional productivity by integrating specialized
        AI agents into a unified, role-based workflow.
        """
    )

    st.divider()

    # -------- STUDENT AGENTS --------
    st.markdown('<div class="section-title">Student Agents</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        agent_card(
            "Exam Planner",
            "Create a full syllabus-based personalized study plan.",
            exam_planner_run,
            "student",
            "exam_planner"
        )

        agent_card(
            "Doubt Solver",
            "Clear subject doubts using syllabus-grounded intelligence.",
            doubt_solver_run,
            "student",
            "doubt_solver"
        )

    with col2:
        agent_card(
            "Resource Collector",
            "Discover videos, blogs, and PDFs for pending topics.",
            resource_collector_run,
            "student",
            "resource_collector"
        )

        agent_card(
            "Mentor Agent",
            "Get motivation, reminders, and visual progress tracking.",
            mentor_agent_run,
            "student",
            "mentor_agent"
        )

    st.divider()

    # -------- PROFESSIONAL AGENTS --------
    st.markdown('<div class="section-title">Professional Agents</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        agent_card(
            "Email Writer",
            "Draft professional emails with appropriate tone.",
            email_writer_run,
            "professional",
            "email_writer"
        )

        agent_card(
            "Meeting Scheduler",
            "Schedule meetings and analyze meeting load.",
            meeting_scheduler_run,
            "professional",
            "meeting_scheduler"
        )

    with col4:
        agent_card(
            "Task Decomposer",
            "Break complex work into manageable tasks.",
            task_decomposer_run,
            "professional",
            "task_decomposer"
        )

        agent_card(
            "Insight Agent",
            "Analyze productivity and task performance.",
            insight_agent_run,
            "professional",
            "insight_agent"
        )
