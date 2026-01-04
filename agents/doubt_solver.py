import streamlit as st
import os
import requests

from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import get_relevant_chunks


# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"


@st.cache_resource
def initialize_rag():
    """
    Loads math syllabus + notes PDFs, creates embeddings,
    and returns a FAISS vector store.
    """
    base_path = "data/knowledge_base"
    documents = []

    syllabus_path = os.path.join(base_path, "Syllabus")
    notes_path = os.path.join(base_path, "notes")

    if os.path.exists(syllabus_path):
        documents.extend(load_documents(syllabus_path))

    if os.path.exists(notes_path):
        documents.extend(load_documents(notes_path))

    if not documents:
        raise ValueError("No syllabus or notes PDFs found.")

    chunks = split_documents(documents)
    embeddings = get_embeddings()
    vector_store = create_vector_store(chunks, embeddings)

    return vector_store


def call_phi3(prompt: str) -> str:
    """
    Sends prompt to local phi-3 model via Ollama HTTP API.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json().get("response", "No response generated.")


def run():
    st.subheader("Doubt Solver Agent (Math – RAG Enabled)")

    try:
        vector_store = initialize_rag()
    except Exception as e:
        st.error(str(e))
        return

    question = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        # Retrieve relevant syllabus/notes chunks
        retrieved_docs = get_relevant_chunks(vector_store, question)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

        final_prompt = f"""
You are an exam-oriented mathematics tutor.

Answer the question using ONLY the context provided below.
If the answer is not present in the context, clearly say that the information is not available.

Context:
{context}

Question:
{question}
"""

        with st.spinner("Generating answer..."):
            try:
                answer = call_phi3(final_prompt)
                st.write(answer)
            except Exception as e:
                st.error(f"Error generating answer: {e}")
