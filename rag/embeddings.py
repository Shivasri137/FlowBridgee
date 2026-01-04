from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    """
    Returns a sentence-transformer embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
