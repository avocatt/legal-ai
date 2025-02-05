"""
QA chain implementation for the Turkish Legal RAG system.
"""

from typing import Any, Dict, List, Optional
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel

from .retriever import DocumentRetriever

# Enhanced prompt template that better handles legal terminology
PROMPT_TEMPLATE = """Sen Türk Ceza Kanunu konusunda uzmanlaşmış bir hukuk asistanısın. SADECE Türk Ceza Kanunu ve verilen bağlam çerçevesinde soruları yanıtlayabilirsin.

Bağlam:
{context}

Soru: {question}

Yanıtını oluştururken şu kurallara kesinlikle uy:
1. SADECE verilen bağlamda bulunan bilgileri kullan
2. Eğer verilen bağlamda soruyu yanıtlamak için yeterli bilgi yoksa, "Üzgünüm, bu soru Türk Ceza Kanunu kapsamı dışındadır veya verilen bağlamda bu soruyu yanıtlamak için yeterli bilgi bulunmamaktadır." şeklinde yanıt ver
3. Verilen yasal terimleri doğru ve yerinde kullan
4. Cevabını yasal terminoloji ve kanun maddeleriyle destekle
5. Açık, anlaşılır ve profesyonel bir dil kullan
6. Asla verilen bağlam dışında bilgi uydurma veya tahmin yürütme

Yanıt:"""


class LegalQAChain:
    """A chain for question-answering about Turkish legal texts."""

    def __init__(
        self,
        rag_system: Any,
        llm: BaseLanguageModel,
    ):
        """Initialize the QA chain with RAG system and LLM."""
        self.rag_system = rag_system
        self.llm = llm
        self._setup_chain()

    def _setup_chain(self):
        """Set up the chain using the new LangChain syntax."""
        self.prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # Create the chain using the new syntax
        self.chain = (
            {
                "context": lambda x: self.format_context(
                    self.rag_system.retrieve(
                        query=x["question"],
                        metadata_filter=x.get("metadata_filter")
                    )
                ),
                "question": lambda x: x["question"]
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """Format retrieved documents and legal terms into a context string."""
        if not retrieved_docs:
            return "No relevant information found."

        context_parts = []

        # Separate articles and terms
        articles = [doc for doc in retrieved_docs if doc["metadata"].get(
            "type") != "legal_term"]
        terms = [doc for doc in retrieved_docs if doc["metadata"].get(
            "type") == "legal_term"]

        # Add relevant articles
        if articles:
            context_parts.append("İlgili Kanun Maddeleri:")
            for doc in articles:
                if doc["metadata"]["type"] == "article":
                    context_parts.append(
                        f"- Madde {doc['metadata']['number']}: {doc['content']}")
                else:
                    context_parts.append(f"- {doc['content']}")

        # Add relevant legal terms
        if terms:
            context_parts.append("\nİlgili Yasal Terimler:")
            for doc in terms:
                context_parts.append(f"- {doc['content']}")

        return "\n".join(context_parts)

    def run(
        self,
        question: str,
        metadata_filter: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Run the QA chain to answer a question.

        Args:
            question: The question to answer
            metadata_filter: Optional metadata filters for document retrieval

        Returns:
            str: The generated answer

        Raises:
            ValueError: If the question is empty or invalid
            Exception: If there's an error during processing
        """
        if not question or not isinstance(question, str):
            raise ValueError("Question must be a non-empty string")

        try:
            return self.chain.invoke({
                "question": question,
                "metadata_filter": metadata_filter
            })
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg.lower():
                return "Error: OpenAI API key is invalid or not configured properly."
            elif "rate limit" in error_msg.lower():
                return "Error: Rate limit exceeded. Please try again later."
            elif "context length" in error_msg.lower():
                return "Error: The question or context is too long to process."
            else:
                return f"An error occurred while processing your question: {error_msg}"
