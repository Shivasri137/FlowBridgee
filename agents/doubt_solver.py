import streamlit as st
import os
import subprocess
from PyPDF2 import PdfReader

# ---------------- CONFIG ----------------
UPLOAD_DIR = "data/knowledge_base/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

OLLAMA_MODEL = "phi3"


# ---------------- OLLAMA CALL ----------------
def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True
        )
        return result.stdout.strip()
    except Exception:
        return "Error: Unable to reach local AI model."


# ---------------- PDF TEXT EXTRACTION ----------------
def read_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception:
        pass
    return text


# ---------------- SIMPLE RAG ----------------
def retrieve_relevant_text(question, text):
    question_words = question.lower().split()
    lines = text.split("\n")

    relevant = []
    for line in lines:
        for word in question_words:
            if word in line.lower():
                relevant.append(line)
                break

    return "\n".join(relevant[:20])


# ---------------- MAIN AGENT ----------------
def run():
    st.subheader("Doubt Solver Agent")

    tabs = st.tabs(["Normal Doubt Solver", "RAG-Enabled Doubt Solver"])

    # ================= NORMAL =================
    with tabs[0]:
        st.markdown("### Normal Doubt Solver")
        st.caption("General AI tutor (no syllabus restriction)")

        question = st.text_area("Enter your doubt")

        if st.button("Solve Doubt"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking..."):
                    answer = ask_ollama(
                        f"Explain clearly with examples:\n{question}"
                    )
                st.markdown("#### Answer")
                st.write(answer)

    # ================= RAG =================
    with tabs[1]:
        st.markdown("### RAG-Enabled Doubt Solver")
        st.caption("Answers strictly from uploaded PDF")

        uploaded_file = st.file_uploader(
            "Upload study material (PDF only)",
            type=["pdf"]
        )

        extracted_text = ""

        if uploaded_file:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            st.success("PDF uploaded successfully")

            extracted_text = read_pdf(file_path)

            if extracted_text.strip():
                st.info("PDF text extracted successfully")
            else:
                st.error("PDF text could not be extracted (scanned PDF)")

        question = st.text_area("Ask a question from the uploaded document")

        if st.button("Solve Using Knowledge Base"):
            if not extracted_text.strip():
                st.warning("Please upload a readable PDF first.")
                return

            if not question.strip():
                st.warning("Please enter a question.")
                return

            context = retrieve_relevant_text(question, extracted_text)

            if not context.strip():
                st.warning("No relevant content found in the document.")
                return

            prompt = f"""
Answer ONLY from the context below.
If not found, say: "Answer not found in the document."

Context:
{context}

Question:
{question}
"""

            with st.spinner("Answering from document..."):
                answer = ask_ollama(prompt)

            st.markdown("#### Answer (From PDF)")
            st.write(answer)
