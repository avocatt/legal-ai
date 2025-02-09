"""Create and manage vector stores for the RAG system.

This module provides functionality to create and manage vector stores
for law articles, blog content, and legal terminology.
"""

import ast
import os
import sys
from typing import Dict, List, Optional

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

# Create persistent storage directory if it doesn't exist
CHROMA_DB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "backend", "chroma_db"
)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)


class VectorStoreManager:
    """Manage vector stores for the RAG system.

    This class provides functionality to create and manage vector store collections,
    including adding documents and managing embeddings.
    """

    def __init__(
        self,
        db_path: str,
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ):
        """Initialize the vector store manager.

        Args:
            db_path (str): Path to ChromaDB directory
            embedding_model (str): Name of the embedding model to use. Defaults to
                                 multilingual MPNet model.
        """
        self.db_path = db_path
        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model
            )
        )
        self.client = chromadb.PersistentClient(path=db_path)

    def create_collection(
        self, name: str, description: Optional[str] = None
    ) -> chromadb.Collection:
        """Create a new collection in the vector store.

        Args:
            name (str): Name of the collection
            description (Optional[str]): Optional description of the collection

        Returns:
            chromadb.Collection: Created or retrieved collection

        Raises:
            ValueError: If collection already exists
        """
        try:
            return self.client.create_collection(
                name=name,
                embedding_function=self.embedding_function,
                metadata={"description": description} if description else None,
            )
        except ValueError as e:
            print(f"Collection {name} already exists: {str(e)}")
            return self.client.get_collection(
                name=name, embedding_function=self.embedding_function
            )

    def add_documents(
        self,
        collection: chromadb.Collection,
        documents: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict]] = None,
        batch_size: int = 100,
    ) -> None:
        """Add documents to a collection in batches.

        Args:
            collection (chromadb.Collection): Target collection
            documents (List[str]): List of documents to add
            ids (List[str]): List of document IDs
            metadatas (Optional[List[Dict]]): Optional list of metadata dictionaries
            batch_size (int): Size of batches for adding documents. Defaults to 100.

        Raises:
            Exception: If there's an error adding documents
        """
        try:
            for i in range(0, len(documents), batch_size):
                end_idx = min(i + batch_size, len(documents))
                batch_docs = documents[i:end_idx]
                batch_ids = ids[i:end_idx]
                batch_meta = metadatas[i:end_idx] if metadatas else None

                collection.add(
                    documents=batch_docs,
                    ids=batch_ids,
                    metadatas=batch_meta,
                )
                print(f"Added batch {i//batch_size + 1}")

        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            raise


class VectorStoreBuilder:
    """Build vector stores for blog articles, law articles, and legal terms.

    This class provides functionality to create and populate vector stores
    for different types of legal content, including blog articles and
    legal terminology.
    """

    def __init__(self):
        """Initialize the vector store builder with default settings."""
        # Set up paths
        self.data_dir = "data/processed/criminal_law"

        # Initialize embedding function
        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            )
        )

        # Initialize Chroma client with persistent storage
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

        # Collection names
        self.blog_collection_name = "turkish_criminal_law_blog"

    def _safe_eval(self, s: str) -> List:
        """Safely evaluate string representations of lists.

        Args:
            s (str): String representation of a list to evaluate

        Returns:
            List: Evaluated list or empty list if evaluation fails
        """
        if pd.isna(s):
            return []
        try:
            return ast.literal_eval(s)
        except (ValueError, SyntaxError) as e:
            print(f"Error evaluating string: {str(e)}")
            return []

    def create_blog_collection(self) -> bool:
        """Create vector store collection for blog articles.

        This method processes the hierarchical blog articles and creates
        a vector store collection with proper embeddings and metadata.

        Returns:
            bool: True if collection was created successfully

        Raises:
            Exception: If there's an error during collection creation
        """
        try:
            # Load the hierarchical articles
            print("Loading hierarchical articles...")
            articles_file = os.path.join(
                self.data_dir, "hierarchical_criminal_law_articles.csv"
            )
            df = pd.read_csv(articles_file)
            print(f"Loaded {len(df)} articles")

            # Convert string representations to lists
            print("Converting string representations to lists...")
            df["tck_references"] = df["tck_references"].apply(self._safe_eval)
            df["legal_terms"] = df["legal_terms"].apply(self._safe_eval)
            df["main_topics"] = df["main_topics"].apply(self._safe_eval)

            # Create or recreate blog articles collection
            print(f"\nSetting up collection: {self.blog_collection_name}")
            try:
                collection = self.chroma_client.get_collection(
                    name=self.blog_collection_name,
                    embedding_function=self.embedding_function,
                )
                self.chroma_client.delete_collection(name=self.blog_collection_name)
                print("Deleted existing collection")
            except chromadb.errors.NoIndexException:
                pass

            # Create new collection
            collection = self.chroma_client.create_collection(
                name=self.blog_collection_name,
                embedding_function=self.embedding_function,
                metadata={"description": "Turkish Criminal Law Blog Articles"},
            )

            # Prepare documents for embedding
            documents = []
            ids = []
            metadatas = []

            print("\nPreparing documents for embedding...")
            for idx, row in df.iterrows():
                try:
                    # Create document text combining title and content
                    doc_text = (
                        f"Title: {row['title']}\n\nContent: {row['cleaned_content']}"
                    )

                    # Create metadata
                    metadata = {
                        "title": row["title"],
                        "hierarchy_level": row["hierarchy_level"],
                        "tck_references": str(row["tck_references"]),
                        "legal_terms": str(row["legal_terms"]),
                        "main_topics": str(row["main_topics"]),
                        "category": row["category"],
                        "url": row["url"],
                        "type": "blog_article",
                    }

                    documents.append(doc_text)
                    ids.append(f"blog_article_{idx}")
                    metadatas.append(metadata)
                except (KeyError, AttributeError) as e:
                    print(f"Error processing row {idx}: {str(e)}")
                    continue

            # Add documents to collection in batches
            batch_size = 100
            total_batches = len(documents) // batch_size + (
                1 if len(documents) % batch_size > 0 else 0
            )

            print(f"\nAdding documents to vector store in {total_batches} batches...")
            for i in range(0, len(documents), batch_size):
                batch_end = min(i + batch_size, len(documents))
                print(f"Processing batch {i//batch_size + 1}/{total_batches}")

                collection.add(
                    documents=documents[i:batch_end],
                    ids=ids[i:batch_end],
                    metadatas=metadatas[i:batch_end],
                )

            # Print collection stats
            print("\nBlog articles vector store creation completed!")
            print(f"Total documents in collection: {collection.count()}")

            return True

        except Exception as e:
            print(
                f"Error creating blog articles vector store: {str(e)}", file=sys.stderr
            )
            raise


if __name__ == "__main__":
    try:
        builder = VectorStoreBuilder()
        success = builder.create_blog_collection()
        if success:
            print("\nVector store created successfully!")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
