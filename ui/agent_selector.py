import streamlit as st

# ------------------ IMPORT AGENTS ------------------
try:
    from agents.exam_planner import run as exam_planner_run
    from agents.resource_collector import run as resource_collector_run
    from agents.doubt_solver import run as doubt_solver_run
    from agents.mentor_agent import run as mentor_agent_run
    from agents.email_writer import run as email_writer_run
    from agents.task_decomposer import run as task_decomposer_run
    from agents.meeting_scheduler import run as meeting_scheduler_run
    from agents.insight_agent import run as insight_agent_run
except ImportError as e:
    st.error(f"Import Error: {e}. Check if agent files exist in 'agents/' folder.")

# ------------------ SESSION STATE ------------------
if "active_agent" not in st.session_state:
    st.session_state.active_agent = None

# ------------------ UI STYLING ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background: #f8fafc; }
    .main-header { font-size: 40px; font-weight: 800; color: #1e293b; margin-bottom: 5px; }
    .section-title { font-size: 22px; font-weight: 700; margin-top: 25px; color: #334155; border-bottom: 2px solid #e2e8f0; }
    .agent-card {
        border-radius: 12px; padding: 20px; background: white; 
        border: 1px solid #e2e8f0; height: 150px; 
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .agent-title { font-size: 18px; font-weight: 700; color: #1e293b; }
    .agent-desc { font-size: 13px; color: #64748b; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

def agent_card(title, desc, key, category):
    # Category color coding
    border_color = "#22c55e" if category == "student" else "#6366f1"
    st.markdown(f"""<div class="agent-card" style="border-left: 6px solid {border_color};">
        <div class="agent-title">{title}</div>
        <div class="agent-desc">{desc}</div>
    </div>""", unsafe_allow_html=True)
    if st.button(f"Launch {title}", key=f"btn_{key}"):
        st.session_state.active_agent = key
        st.rerun()

def render_agent(agent_name):
    # DYNAMIC ROUTING - ENSURE ALL STRINGS MATCH CARD KEYS
    if agent_name == "exam_planner": exam_planner_run()
    elif agent_name == "resource_collector": resource_collector_run()
    elif agent_name == "doubt_solver": doubt_solver_run()
    elif agent_name == "mentor_agent": mentor_agent_run()
    elif agent_name == "email_writer": email_writer_run()
    elif agent_name == "task_decomposer": task_decomposer_run()
    elif agent_name == "meeting_scheduler": meeting_scheduler_run()
    elif agent_name == "insight_agent": insight_agent_run()

def run():
    if st.session_state.active_agent:
        with st.sidebar:
            if st.button("⬅ Home Dashboard"):
                st.session_state.active_agent = None
                st.rerun()
            st.divider()
            st.info(f"Agent: {st.session_state.active_agent.upper()}")
        
        render_agent(st.session_state.active_agent)
        return

    st.markdown('<div class="main-header">Flow Bridge</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🎓 Student Workspace</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        agent_card("Exam Planner", "Syllabus tracking & AI Quizzes.", "exam_planner", "student")
        agent_card("Doubt Solver", "Conceptual clarity.", "doubt_solver", "student")
    with c2:
        agent_card("Resource Collector", "Learning materials.", "resource_collector", "student")
        agent_card("Mentor Agent", "Motivation & Progress.", "mentor_agent", "student")

    st.markdown('<div class="section-title">💼 Professional Suite</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        agent_card("Email Writer", "Professional drafting.", "email_writer", "professional")
        agent_card("Meeting Scheduler", "Calendar management.", "meeting_scheduler", "professional")
    with c4:
        agent_card("Task Decomposer", "Break goals into tasks.", "task_decomposer", "professional")
        agent_card("Insight Agent", "Productivity analysis.", "insight_agent", "professional")

if __name__ == "__main__":
    run()