"""Implement hierarchical structure for criminal law content.

This module provides functionality to implement and validate the hierarchical
structure of Turkish Criminal Law content, ensuring proper organization and
relationships between different content types.
"""

import ast
import os
import sys
from typing import Dict, List, Optional

import pandas as pd


class HierarchyImplementer:
    """Implement and validate content hierarchy.

    This class provides functionality to implement and validate hierarchical
    relationships between different pieces of criminal law content, including
    books, parts, chapters, and articles.
    """

    def __init__(self, input_path: str, output_path: str):
        """Initialize the hierarchy implementer.

        Args:
            input_path (str): Path to input CSV file containing criminal law content
            output_path (str): Path to save the processed hierarchical content
        """
        self.input_path = input_path
        self.output_path = output_path
        self.hierarchy_levels = {
            "book": ["BIRINCI KITAP", "IKINCI KITAP", "UCUNCU KITAP"],
            "part": ["BIRINCI KISIM", "IKINCI KISIM", "UCUNCU KISIM"],
            "chapter": ["BIRINCI BOLUM", "IKINCI BOLUM", "UCUNCU BOLUM"],
        }

        # Define TCK hierarchy structure
        self.tck_hierarchy = {
            "genel_hukumler": range(1, 76),  # Birinci Kitap: Genel Hükümler
            "özel_hukumler": range(76, 344),  # İkinci Kitap: Özel Hükümler
            "son_hukumler": range(344, 347),  # Üçüncü Kitap: Son Hükümler
        }

        # Define minimum required legal terms for content quality
        self.min_legal_terms = {
            # At least one of these should be present
            "basic": {"suç", "ceza", "hukuk"},
            # At least one if discussing procedure
            "procedural": {"soruşturma", "kovuşturma", "yargılama", "delil", "ispat"},
            # At least one if discussing sanctions
            "sanctions": {"hapis", "para cezası", "adli para", "müebbet"},
        }

        # Define validation rules
        self.validation_rules = {
            "content_quality": {
                "description": "Content must meet quality standards",
                "check": self._check_content_quality,
            }
        }

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

    def _check_content_quality(self, article: Dict) -> List[str]:
        """Check if content meets quality standards.

        Args:
            article (Dict): Dictionary containing article content and metadata

        Returns:
            List[str]: List of quality issues found in the content
        """
        issues = []

        # Check for minimum content length
        content_length = len(str(article["cleaned_content"]))
        if content_length < 100:
            issues.append("Content too short (less than 100 characters)")

        # Check for basic legal terminology
        legal_terms = set(article["legal_terms"])
        if not any(term in legal_terms for term in self.min_legal_terms["basic"]):
            issues.append("Missing basic legal terminology")

        # Check for procedural terms if title suggests procedural content
        procedural_keywords = {
            "soruşturma",
            "kovuşturma",
            "yargılama",
            "delil",
            "ispat",
            "muhakeme",
        }
        if any(keyword in article["title"].lower() for keyword in procedural_keywords):
            if not any(
                term in legal_terms for term in self.min_legal_terms["procedural"]
            ):
                issues.append("Missing procedural terminology in procedural content")

        # Check for sanction terms if title suggests sanctions content
        sanction_keywords = {"ceza", "hapis", "para", "müebbet", "yaptırım"}
        if any(keyword in article["title"].lower() for keyword in sanction_keywords):
            if not any(
                term in legal_terms for term in self.min_legal_terms["sanctions"]
            ):
                issues.append("Missing sanctions terminology in sanctions content")

        return issues

    def implement_hierarchy(self) -> None:
        """Implement the hierarchical structure.

        Reads the input file, processes the content to implement hierarchy,
        and saves the result to the output file.

        Raises:
            FileNotFoundError: If the input file cannot be found
            Exception: For other processing errors
        """
        try:
            # Read input file
            df = pd.read_csv(self.input_path)
            print(f"Read {len(df)} articles from {self.input_path}")

            # Implement hierarchy
            df["hierarchy_level"] = df.apply(self._determine_level, axis=1)
            df["parent_id"] = df.apply(self._determine_parent, axis=1)

            # Save hierarchical content
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            df.to_csv(self.output_path, index=False)
            print(f"Saved hierarchical content to {self.output_path}")

        except Exception as e:
            print(f"Error implementing hierarchy: {str(e)}")
            raise

    def _determine_level(self, row: pd.Series) -> str:
        """Determine the hierarchy level of a content item.

        Args:
            row (pd.Series): DataFrame row containing content information

        Returns:
            str: Determined hierarchy level (book, part, chapter, or article)
        """
        content = row["content"].upper()

        for level, keywords in self.hierarchy_levels.items():
            if any(keyword in content for keyword in keywords):
                return level

        return "article"

    def _determine_parent(self, row: pd.Series) -> Optional[str]:
        """Determine the parent ID of a content item.

        Args:
            row (pd.Series): DataFrame row containing content information

        Returns:
            Optional[str]: Parent ID if exists, None otherwise
        """
        try:
            level = row["hierarchy_level"]
            if level == "article":
                return None

            content = row["content"].upper()
            parent_levels = list(self.hierarchy_levels.keys())
            current_index = parent_levels.index(level)

            if current_index > 0:
                parent_level = parent_levels[current_index - 1]
                parent_keywords = self.hierarchy_levels[parent_level]

                for keyword in parent_keywords:
                    if keyword in content:
                        return f"{parent_level}_{keyword}"

            return None

        except (ValueError, KeyError, AttributeError) as e:
            print(f"Error determining parent: {str(e)}")
            return None

    def _determine_hierarchy_level(self, tck_refs: List[int]) -> str:
        """Determine hierarchy level based on TCK references.

        Args:
            tck_refs (List[int]): List of TCK article reference numbers

        Returns:
            str: Determined hierarchy level (genel_hukumler, özel_hukumler,
                 son_hukumler, mixed, or blog_only)
        """
        if not tck_refs:
            return "blog_only"

        levels = set()
        for ref in tck_refs:
            for section, range_obj in self.tck_hierarchy.items():
                if ref in range_obj:
                    levels.add(section)

        if len(levels) == 1:
            return levels.pop()
        elif len(levels) > 1:
            return "mixed"
        else:
            return "blog_only"


if __name__ == "__main__":
    try:
        implementer = HierarchyImplementer(
            "data/processed/criminal_law/analyzed_criminal_law_articles.csv",
            "data/processed/criminal_law/hierarchical_criminal_law_articles.csv",
        )
        implementer.implement_hierarchy()
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)
