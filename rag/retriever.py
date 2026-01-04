def get_relevant_chunks(vector_store, query, k=4):
    """
    Retrieves top-k relevant document chunks from the vector store.
    """
    return vector_store.similarity_search(query, k=k)
