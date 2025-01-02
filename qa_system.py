import chromadb
from chromadb.utils import embedding_functions


def get_answer(question: str, k: int = 3) -> str:
    """
    Get answer for a given question using ChromaDB

    Args:
        question: The question to answer
        k: Number of relevant chunks to retrieve

    Returns:
        str: The answer based on the most relevant chunks
    """
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path="./chroma_db")
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Get collection
    collection = client.get_collection(
        name="turkish_criminal_law",
        embedding_function=embedding_function
    )

    # Query the collection
    results = collection.query(
        query_texts=[question],
        n_results=k
    )

    # Combine the relevant chunks into an answer
    relevant_chunks = results['documents'][0]
    combined_answer = "\n".join(relevant_chunks)

    return combined_answer
