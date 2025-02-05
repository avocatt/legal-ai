import time
from typing import Dict, Optional

from langchain_openai import ChatOpenAI
from ..core.config import get_settings
from src.rag import TurkishLegalRAG, LegalQAChain


class QAService:
    def __init__(self):
        self.settings = get_settings()
        self.rag_system = TurkishLegalRAG(
            law_json_path="data/processed/processed_law.json",
            terms_json_path="tools/legal-terminology-dict/output/legal_terms.json",
            collection_name=self.settings.COLLECTION_NAME,
            embedding_model=self.settings.EMBEDDING_MODEL
        )

        self.llm = ChatOpenAI(
            model_name=self.settings.LLM_MODEL,
            temperature=0
        )

        self.qa_chain = LegalQAChain(self.rag_system, self.llm)

    async def get_answer(
        self,
        question: str,
        metadata_filter: Optional[Dict[str, str]] = None,
        n_results: int = 5
    ) -> Dict:
        start_time = time.time()

        try:
            # Get answer from QA chain
            answer = self.qa_chain.run(
                question=question,
                metadata_filter=metadata_filter
            )

            # Get sources (including both articles and terms)
            sources = self.rag_system.retrieve(
                query=question,
                n_results=n_results,
                metadata_filter=metadata_filter
            )

            # Calculate processing time
            processing_time = time.time() - start_time

            return {
                "answer": answer,
                "confidence_score": 0.8,  # TODO: Implement confidence scoring
                "sources": sources,
                "processing_time": processing_time
            }

        except Exception as e:
            raise Exception(f"Error processing question: {str(e)}")


# Create singleton instance
qa_service = QAService()
