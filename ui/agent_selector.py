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


# ------------------ SESSION STATE ------------------
if "active_agent" not in st.session_state:
    st.session_state.active_agent = None


# ------------------ GLOBAL CSS ------------------
st.markdown("""
<style>
.main { background-color: #fafafa; }

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 25px 0 15px 0;
    color: #1f2937;
}

.card {
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 20px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
}

.student {
    background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
    border-left: 6px solid #22c55e;
}

.professional {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
    border-left: 6px solid #6366f1;
}

.agent-title {
    font-size: 18px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 6px;
}

.agent-desc {
    font-size: 14px;
    color: #4b5563;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ------------------ CARD ------------------
def agent_card(title, description, agent_name, css_class):
    st.markdown(
        f"""
        <div class="card {css_class}">
            <div class="agent-title">{title}</div>
            <div class="agent-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Open", key=agent_name):
        st.session_state.active_agent = agent_name


# ------------------ AGENT RENDER ------------------
def render_agent(agent_name):
    if agent_name == "exam_planner":
        exam_planner_run()
    elif agent_name == "resource_collector":
        resource_collector_run()
    elif agent_name == "doubt_solver":
        doubt_solver_run()
    elif agent_name == "mentor_agent":
        mentor_agent_run()
    elif agent_name == "email_writer":
        email_writer_run()
    elif agent_name == "task_decomposer":
        task_decomposer_run()
    elif agent_name == "meeting_scheduler":
        meeting_scheduler_run()
    elif agent_name == "insight_agent":
        insight_agent_run()


# ------------------ MAIN UI ------------------
def run():
    st.title("Flow Bridge")

    st.markdown(
        """
        Flow Bridge is an intelligent, multi-agent platform designed to support
        students and professionals through structured planning, guidance,
        and actionable insights.
        """
    )

    # -------- BACK BUTTON --------
    if st.session_state.active_agent:
        if st.button("⬅ Back to Dashboard"):
            st.session_state.active_agent = None
            st.rerun()

        st.divider()
        render_agent(st.session_state.active_agent)
        return

    # -------- DASHBOARD --------
    st.divider()
    st.markdown('<div class="section-title">Student Agents</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        agent_card(
            "Exam Planner",
            "Create syllabus-based study plans.",
            "exam_planner",
            "student"
        )
        agent_card(
            "Doubt Solver",
            "Clear doubts using syllabus context.",
            "doubt_solver",
            "student"
        )

    with col2:
        agent_card(
            "Resource Collector",
            "Find learning resources for topics.",
            "resource_collector",
            "student"
        )
        agent_card(
            "Mentor Agent",
            "Motivation and progress tracking.",
            "mentor_agent",
            "student"
        )

    st.divider()
    st.markdown('<div class="section-title">Professional Agents</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        agent_card(
            "Email Writer",
            "Draft professional emails.",
            "email_writer",
            "professional"
        )
        agent_card(
            "Meeting Scheduler",
            "Schedule and manage meetings.",
            "meeting_scheduler",
            "professional"
        )

    with col4:
        agent_card(
            "Task Decomposer",
            "Break work into tasks.",
            "task_decomposer",
            "professional"
        )
        agent_card(
            "Insight Agent",
            "Analyze productivity.",
            "insight_agent",
            "professional"
        )
