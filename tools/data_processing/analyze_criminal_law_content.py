"""Analyze and extract metadata from criminal law articles.

This module provides functionality to analyze criminal law articles,
extract relevant metadata, and prepare them for the RAG system.
"""

import json
import os
import re
import sys
from collections import defaultdict

import pandas as pd


class CriminalLawAnalyzer:
    """Analyze criminal law content and extract metadata.

    This class provides methods to analyze criminal law articles, extract references,
    legal terms, and identify main topics within the content.
    """

    def __init__(self):
        """Initialize the CriminalLawAnalyzer with predefined patterns and keywords."""
        self.tck_patterns = {
            "article_reference": r"(?:TCK|Türk Ceza Kanunu)(?:\s+)?(?:m\.|madde|md\.|Art\.|Article)?(?:\s+)?(\d+)",
            "legal_terms": [
                "suç",
                "ceza",
                "yaptırım",
                "hapis",
                "para cezası",
                "adli para cezası",
                "müebbet",
                "ağırlaştırılmış müebbet",
                "tutuklama",
                "gözaltı",
                "yakalama",
                "soruşturma",
                "kovuşturma",
                "mahkumiyet",
                "beraat",
                "hüküm",
            ],
        }

        self.topic_keywords = {
            "genel_hukumler": [
                "suçun unsurları",
                "kast",
                "taksir",
                "teşebbüs",
                "iştirak",
            ],
            "ceza_sorumluluğu": [
                "kusur",
                "hukuka uygunluk",
                "meşru müdafaa",
                "zorunluluk hali",
            ],
            "yaptırımlar": ["hapis cezası", "adli para cezası", "güvenlik tedbirleri"],
            "özel_hukumler": [
                "kasten öldürme",
                "hırsızlık",
                "dolandırıcılık",
                "uyuşturucu",
            ],
            "usul_hukumleri": [
                "soruşturma",
                "kovuşturma",
                "delil",
                "ispat",
                "yargılama",
            ],
        }

    def extract_tck_references(self, text):
        """Extract Turkish Criminal Code article references from text.

        Args:
            text (str): The text content to analyze

        Returns:
            List[int]: A sorted list of unique TCK article numbers referenced in the text
        """
        references = []
        matches = re.finditer(self.tck_patterns["article_reference"], text)
        for match in matches:
            article_num = match.group(1)
            references.append(int(article_num))
        return sorted(list(set(references)))

    def extract_legal_terms(self, text):
        """Extract legal terms from text.

        Args:
            text (str): The text content to analyze

        Returns:
            List[str]: A list of unique legal terms found in the text
        """
        terms = []
        for term in self.tck_patterns["legal_terms"]:
            if term.lower() in text.lower():
                terms.append(term)
        return list(set(terms))

    def identify_main_topics(self, text):
        """Identify main topics present in the text.

        Args:
            text (str): The text content to analyze

        Returns:
            List[str]: A list of topic categories that have matching keywords in the text
        """
        topics = defaultdict(int)
        text_lower = text.lower()

        for category, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    topics[category] += 1

        return [topic for topic, count in topics.items() if count > 0]

    def analyze_content(self):
        """Analyze the criminal law content and extract comprehensive metadata.

        This method processes the cleaned criminal law articles, extracts various metadata
        including TCK references, legal terms, and main topics. It saves the analyzed
        data and generates summary statistics.

        Returns:
            Dict: A dictionary containing extracted metadata categories including:
                - total_articles: Total number of articles analyzed
                - articles_with_tck_refs: Number of articles with TCK references
                - unique_tck_articles: List of unique TCK article numbers referenced
                - topic_distribution: Distribution of main topics across articles
                - most_common_legal_terms: Most frequently occurring legal terms

        Raises:
            FileNotFoundError: If the input file cannot be found
            Exception: For other processing errors
        """
        input_file = "data/processed/criminal_law/cleaned_criminal_law_articles.csv"
        output_dir = "data/processed/criminal_law"
        output_file = os.path.join(output_dir, "analyzed_criminal_law_articles.csv")
        metadata_file = os.path.join(output_dir, "content_analysis_metadata.json")

        try:
            print(f"Reading cleaned articles from: {input_file}")
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")

            df = pd.read_csv(input_file)
            print(f"Successfully read {len(df)} articles")

            # Analyze content
            print("Analyzing content...")
            df["tck_references"] = df["cleaned_content"].apply(
                self.extract_tck_references
            )
            df["legal_terms"] = df["cleaned_content"].apply(self.extract_legal_terms)
            df["main_topics"] = df["cleaned_content"].apply(self.identify_main_topics)

            # Generate metadata
            metadata = {
                "total_articles": len(df),
                "articles_with_tck_refs": len(df[df["tck_references"].str.len() > 0]),
                "unique_tck_articles": sorted(
                    list(set([ref for refs in df["tck_references"] for ref in refs]))
                ),
                "topic_distribution": self.calculate_topic_distribution(
                    df["main_topics"]
                ),
                "most_common_legal_terms": self.get_most_common_terms(
                    df["legal_terms"]
                ),
            }

            # Save results
            print(f"Saving analyzed articles to: {output_file}")
            df.to_csv(output_file, index=False)

            print(f"Saving analysis metadata to: {metadata_file}")
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

            # Print summary
            print("\nAnalysis Summary:")
            print(f"Total articles analyzed: {metadata['total_articles']}")
            print(f"Articles with TCK references: {metadata['articles_with_tck_refs']}")
            print(
                f"Unique TCK articles referenced: {len(metadata['unique_tck_articles'])}"
            )
            print("\nTopic Distribution:")
            for topic, count in metadata["topic_distribution"].items():
                print(f"- {topic}: {count}")

            return metadata

        except Exception as e:
            print(f"Error occurred in analyze_content: {str(e)}", file=sys.stderr)
            raise

    def calculate_topic_distribution(self, topics_series):
        """Calculate the distribution of topics across all articles.

        Args:
            topics_series (pd.Series): Series containing lists of topics for each article

        Returns:
            Dict[str, int]: Dictionary mapping topic names to their frequency counts
        """
        topic_counts = defaultdict(int)
        for topics_list in topics_series:
            for topic in topics_list:
                topic_counts[topic] += 1
        return dict(topic_counts)

    def get_most_common_terms(self, terms_series, top_n=10):
        """Get the most commonly occurring legal terms.

        Args:
            terms_series (pd.Series): Series containing lists of legal terms for each article
            top_n (int, optional): Number of top terms to return. Defaults to 10.

        Returns:
            Dict[str, int]: Dictionary mapping terms to their frequency counts,
                           limited to the top N most frequent terms
        """
        term_counts = defaultdict(int)
        for terms_list in terms_series:
            for term in terms_list:
                term_counts[term] += 1
        return dict(
            sorted(term_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        )


if __name__ == "__main__":
    try:
        analyzer = CriminalLawAnalyzer()
        metadata = analyzer.analyze_content()
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)
