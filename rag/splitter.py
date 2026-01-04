from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    """
    Splits documents into chunks for embedding.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)