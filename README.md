# Flow Bridge 🌉  
### A Multi-Agent AI Platform for Students and Professionals

Flow Bridge is an intelligent, role-based, multi-agent platform designed to bridge the gap between **academic learning** and **professional productivity**.  
The system integrates specialized AI agents into a unified workflow to support planning, guidance, analysis, and decision-making for different user roles.

---

## 🚀 Key Objectives

- Provide **personalized academic support** for students  
- Enable **structured productivity tools** for professionals  
- Demonstrate a **multi-agent system architecture**  
- Maintain an **offline-first, cost-free AI approach**

---

## 🧠 System Architecture Overview

Flow Bridge is built using a **modular multi-agent architecture**, where each agent performs a specific responsibility and can operate independently or as part of a workflow.

The platform is divided into **two domains**:

---

## 🎓 Student Agents

These agents focus on academic planning, learning support, and progress tracking.

### 1. Exam Planner Agent
- Generates syllabus-based study plans
- Breaks full syllabus into daily study units
- Considers exam date and daily availability
- Initializes progress tracking

### 2. Resource Collector Agent
- Collects relevant online learning resources
- Supports YouTube videos, blogs, and PDFs
- Suggests resources based on pending topics

### 3. Doubt Solver Agent
- Acts as an interactive tutor
- Provides simple explanations and step-by-step answers
- Uses syllabus-grounded context (RAG-based)
- Supports follow-up questions

### 4. Mentor Agent
- Monitors syllabus completion status
- Motivates students based on progress and time left
- Reminds pending topics
- Visualizes progress using line graphs

---

## 💼 Professional Agents

These agents support productivity, communication, and performance analysis.

### 5. Email Writer Agent
- Drafts professional and student-friendly emails
- Supports multiple tones (formal, friendly, urgent)
- Editable before final use

### 6. Task Decomposer Agent
- Breaks complex work into smaller actionable tasks
- Generates timelines and checklists
- Tracks task completion

### 7. Meeting Scheduler Agent
- Schedules meetings with date, time, and duration
- Displays upcoming and past meetings
- Provides meeting load insights

### 8. Insight Agent
- Analyzes task completion and productivity
- Generates performance summaries
- Provides actionable insights using charts

---

## 🖥️ User Interface Design

- Clean **card-based UI**
- Clear separation between **Student** and **Professional** modes
- Designed using Streamlit with custom CSS enhancements
- Focused on clarity, usability, and presentation quality

---

## 🛠️ Tech Stack

- **Frontend / UI**: Streamlit  
- **Backend Logic**: Python  
- **Data Storage**: JSON (local, lightweight)  
- **AI Models**: Local LLMs (via Ollama)  
- **Visualization**: Matplotlib  
- **Version Control**: Git & GitHub  

---

## 📂 Project Structure
FlowBridge/
│
├── agents/ # All AI agent modules
├── ui/ # UI components (agent selector)
├── data/ # Local JSON storage
├── rag/ # RAG-related utilities
├── utils/ # Helper functions
├── app.py # Main application entry point
├── requirements.txt # Dependencies
└── README.md # Project documentation


---

## ▶️ How to Run the Project

1. Clone the repository:
git clone https://github.com/Shivasri137/FlowBridgee.git
2. Navigate to the project directory:
cd FlowBridgee
3. Install dependencies:
pip install -r requirements.txt
4. Run the application:
streamlit run app.py

---

## 🎯 Key Highlights

- Fully offline & cost-free AI approach  
- Modular and extensible agent design  
- Real-time progress tracking and visualization  
- Suitable for academic evaluation and research papers  

---

## 📌 Future Enhancements

- Calendar integration
- User authentication
- Cloud deployment
- Advanced analytics and recommendations

---

## 👩‍💻 Author

**Shivasri**  
Department of AI & ML  
Nalla Malla Reddy Engineering College  

---

## 📄 License

This project is developed for academic and research purposes.




