import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import warnings

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain_core.language_models import BaseLanguageModel
from sentence_transformers import SentenceTransformer
import openai
from .legal_terms import LegalTerminology
from .qa_chain import LegalQAChain

# Load environment variables
load_dotenv(override=True)

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Set Hugging Face token if available
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if hf_token:
    os.environ["HUGGINGFACE_TOKEN"] = hf_token

# Set tokenizers parallelism to avoid warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Create persistent storage directory if it doesn't exist
CHROMA_DB_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "chroma_db")
os.makedirs(CHROMA_DB_DIR, exist_ok=True)


class TurkishLegalRAG:
    """A flexible RAG system for Turkish legal text that can work with different LLMs."""

    def __init__(
        self,
        law_json_path: str,
        terms_json_path: Optional[str] = None,
        collection_name: str = "turkish_criminal_law",
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    ):
        """Initialize the RAG system with configurable components."""
        self.law_data = self._load_law_data(law_json_path)

        # Initialize embedding function with optional token
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model,
            token=hf_token
        )

        # Initialize Chroma client with persistent storage
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            print(f"Using existing collection: {collection_name}")
        except (ValueError, chromadb.errors.InvalidCollectionException):
            print(f"Creating new collection: {collection_name}")
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Turkish Legal Text Embeddings"}
            )
            self._initialize_vector_store()

        # Initialize legal terminology if path provided
        self.legal_terms = None
        if terms_json_path:
            self.legal_terms = LegalTerminology(
                terms_json_path=terms_json_path,
                embedding_model=embedding_model,
                hf_token=hf_token
            )

    def _load_law_data(self, json_path: str) -> Dict[str, Any]:
        """Load the processed law data from JSON."""
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Law data file not found: {json_path}")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid law data format")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in law data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading law data: {str(e)}")

    def _initialize_vector_store(self):
        """Initialize the vector store with articles and provisions."""
        documents = []
        ids = []
        metadatas = []

        # Process each article (same as before)
        for book in self.law_data['books']:
            for part in book['parts']:
                for chapter in part['chapters']:
                    for article in chapter['articles']:
                        # Create a document for the full article
                        article_text = f"Article {article['number']}: {article['content']}"
                        article_id = f"article_{article['number']}"

                        documents.append(article_text)
                        ids.append(article_id)
                        metadatas.append({
                            'type': 'article',
                            'number': article['number'],
                            'book': book['title'],
                            'part': part['title'],
                            'chapter': chapter['title']
                        })

                        # Create documents for key provisions
                        if 'key_provisions' in article:
                            for idx, provision in enumerate(article['key_provisions']):
                                provision_id = f"provision_{article['number']}_{idx}"
                                documents.append(provision)
                                ids.append(provision_id)
                                metadatas.append({
                                    'type': 'provision',
                                    'article_number': article['number'],
                                    'provision_index': idx,
                                    'book': book['title'],
                                    'part': part['title'],
                                    'chapter': chapter['title']
                                })

        # Add documents to the collection
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        metadata_filter: Optional[Dict[str, str]] = None
    ) -> List[Dict]:
        """
        Retrieve relevant documents and legal terms for the given query.

        Args:
            query: The search query
            n_results: Number of results to retrieve
            metadata_filter: Optional metadata filters

        Returns:
            List of relevant documents and terms
        """
        # Get relevant law articles
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=metadata_filter
        )

        documents = []
        for idx, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][idx]
            documents.append({
                "id": results['ids'][0][idx],
                "content": doc,
                "metadata": metadata,
                "distance": results['distances'][0][idx] if 'distances' in results else None
            })

        # Get relevant legal terms if available
        if self.legal_terms:
            # Get terms based on both query and retrieved articles
            term_contexts = [query] + [doc["content"] for doc in documents]
            all_terms = []
            for context in term_contexts:
                terms = self.legal_terms.get_relevant_terms(
                    context, n_results=3)
                all_terms.extend(terms)

            # Remove duplicates and sort by relevance
            seen_terms = set()
            unique_terms = []
            for term in all_terms:
                if term["term"] not in seen_terms:
                    seen_terms.add(term["term"])
                    unique_terms.append({
                        "id": f"term_{len(unique_terms)}",
                        "content": f"[TERM] {term['term']}\n[DEFINITION] {term['definition']}",
                        "metadata": {"type": "legal_term", "term": term["term"]},
                        "distance": term.get("distance")
                    })

            # Add most relevant terms to the results
            documents.extend(unique_terms[:n_results])

        return documents

    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into a context string."""
        context_parts = []

        for doc in retrieved_docs:
            doc_type = doc['metadata'].get('type', 'unknown')

            if doc_type == 'article':
                context_parts.append(
                    f"Madde {doc['metadata']['number']}: {doc['content']}")
            elif doc_type == 'provision':
                context_parts.append(
                    f"Madde {doc['metadata']['article_number']} - {doc['content']}")
            elif doc_type == 'legal_term':
                context_parts.append(doc['content'])
            else:
                context_parts.append(doc['content'])

        return "\n\n".join(context_parts)


# Example usage
if __name__ == "__main__":
    # Initialize the base RAG system
    rag_system = TurkishLegalRAG("processed_law.json")

    # Initialize LLM (using GPT-3.5-turbo)
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=openai_api_key
    )

    # Create the QA chain
    qa_chain = LegalQAChain(rag_system, llm)

    print("\nTurkish Criminal Law QA System")
    print("=" * 50)

    # Test questions
    questions = [
        "Ceza kanununun temel amacı nedir?",
        "Türk Ceza Kanunu hangi durumlarda yabancı ülkelerde işlenen suçlara uygulanır?",
        "Ceza sorumluluğunun esasları nelerdir?"
    ]

    for question in questions:
        print(f"\nQ: {question}")
        print("\nA:", qa_chain.run(question))
        print("-" * 50)

    # Example with metadata filtering
    print("\nExample with metadata filtering (questions about Book 2):")
    filtered_response = qa_chain.run(
        "Cezaların türleri nelerdir?",
        metadata_filter={"book": "İKİNCİ KİTAP"}
    )
    print("\nA:", filtered_response)
