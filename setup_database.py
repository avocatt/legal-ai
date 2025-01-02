import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2
import os


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def setup_chroma_db():
    """Setup ChromaDB with the Turkish Criminal Law text"""
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")

    # Use default embedding function (all-MiniLM-L6-v2)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Create or get collection
    collection = client.get_or_create_collection(
        name="turkish_criminal_law",
        embedding_function=embedding_function
    )

    # Extract text from PDF
    pdf_path = "türk-ceza-kanunu.pdf"
    text = extract_text_from_pdf(pdf_path)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Add documents to collection
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )

    print(f"Database setup complete. Added {len(chunks)} chunks to ChromaDB.")
    return collection


if __name__ == "__main__":
    setup_chroma_db()
