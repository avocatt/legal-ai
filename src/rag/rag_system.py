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
from langchain.chains import LLMChain
from langchain_core.callbacks import BaseCallbackHandler
from sentence_transformers import SentenceTransformer
import openai

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


class TurkishLegalRAG:
    """A flexible RAG system for Turkish legal text that can work with different LLMs."""

    def __init__(self,
                 law_json_path: str,
                 collection_name: str = "turkish_criminal_law",
                 embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"):
        """Initialize the RAG system with configurable components."""
        self.law_data = self._load_law_data(law_json_path)

        # Initialize embedding function with optional token
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model,
            token=hf_token
        )

        # Initialize Chroma client and collection
        self.chroma_client = chromadb.Client()
        try:
            # Try to get existing collection
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            print(f"Using existing collection: {collection_name}")
        except (ValueError, chromadb.errors.InvalidCollectionException):
            # Create new collection if it doesn't exist
            print(f"Creating new collection: {collection_name}")
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Turkish Legal Text Embeddings"}
            )
            # Initialize the vector store
            self._initialize_vector_store()

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

    def retrieve(self,
                 query: str,
                 n_results: int = 5,
                 metadata_filter: Optional[Dict[str, str]] = None) -> List[Dict]:
        """Retrieve relevant documents for a query with optional metadata filtering."""
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")

        if n_results < 1:
            raise ValueError("n_results must be a positive integer")

        query_params = {
            "query_texts": [query],
            "n_results": n_results
        }

        if metadata_filter:
            if not isinstance(metadata_filter, dict):
                raise ValueError("metadata_filter must be a dictionary")
            query_params["where"] = metadata_filter

        try:
            results = self.collection.query(**query_params)
            return self._format_search_results(results)
        except Exception as e:
            print(f"Error during retrieval: {str(e)}")
            return []

    def _format_search_results(self, results: Dict) -> List[Dict]:
        """Format search results into a more usable structure."""
        formatted_results = []
        if not results['ids']:
            return formatted_results

        for idx, doc_id in enumerate(results['ids'][0]):
            formatted_results.append({
                'id': doc_id,
                'content': results['documents'][0][idx],
                'metadata': results['metadatas'][0][idx],
                'distance': results.get('distances', [[]])[0][idx] if 'distances' in results else None
            })
        return formatted_results

    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents into a context string."""
        context_parts = []
        for doc in retrieved_docs:
            if doc['metadata']['type'] == 'article':
                context_parts.append(
                    f"Article {doc['metadata']['number']}: {doc['content']}")
            else:
                context_parts.append(
                    f"From Article {doc['metadata']['article_number']}: {doc['content']}")
        return "\n\n".join(context_parts)


class LegalQAChain:
    """A chain that combines RAG retrieval with LLM for legal QA."""

    def __init__(self,
                 rag_system: TurkishLegalRAG,
                 llm: Any,
                 callbacks: Optional[List[BaseCallbackHandler]] = None):
        """Initialize the QA chain with a RAG system and LLM."""
        if not isinstance(rag_system, TurkishLegalRAG):
            raise TypeError(
                "rag_system must be an instance of TurkishLegalRAG")

        self.rag = rag_system
        self.llm = llm
        self.callbacks = callbacks

        # Default prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal expert assistant specializing in Turkish Criminal Law. 
            Your task is to answer questions about the law using the provided context.
            Always cite the specific articles you reference in your answer.
            If the provided context doesn't contain enough information to answer the question confidently,
            say so explicitly."""),
            ("human", "Context:\n{context}\n\nQuestion: {question}\n\nPlease provide a detailed answer based on the Turkish Criminal Law:"),
        ])

        self.chain = LLMChain(llm=llm, prompt=self.prompt, callbacks=callbacks)

    def set_custom_prompt(self, prompt: ChatPromptTemplate):
        """Set a custom prompt template for the chain."""
        self.prompt = prompt
        self.chain = LLMChain(llm=self.llm, prompt=prompt,
                              callbacks=self.callbacks)

    def run(self,
            question: str,
            n_results: int = 5,
            metadata_filter: Optional[Dict[str, str]] = None) -> str:
        """Run the full RAG chain to answer a question."""
        if not question or not isinstance(question, str):
            raise ValueError("Question must be a non-empty string")

        try:
            # Retrieve relevant documents
            retrieved_docs = self.rag.retrieve(
                question, n_results, metadata_filter)
            if not retrieved_docs:
                return "I couldn't find any relevant information to answer your question."

            # Format context
            context = self.rag.format_context(retrieved_docs)

            # Generate answer
            response = self.chain.run(context=context, question=question)
            return response
        except Exception as e:
            return f"An error occurred while processing your question: {str(e)}"


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
