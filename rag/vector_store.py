from langchain_community.vectorstores import FAISS

def create_vector_store(documents, embeddings):
    """
    Creates a FAISS vector store from documents and embeddings.
    """
    return FAISS.from_documents(documents, embeddings)
