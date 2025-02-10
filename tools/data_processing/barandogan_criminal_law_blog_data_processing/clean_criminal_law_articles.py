"""Clean and preprocess criminal law articles.

This module provides functionality to clean and preprocess criminal law articles,
removing HTML tags, fixing formatting, and preparing text for analysis.
"""

import os
import re
import sys
from typing import List

import pandas as pd
from bs4 import BeautifulSoup


def clean_html_content(content: str) -> str:
    """Clean HTML content from the text.

    Args:
        content (str): Raw HTML content to be cleaned

    Returns:
        str: Cleaned text content with HTML tags removed and spacing normalized
    """
    if not content or not isinstance(content, str):
        return ""

    # Remove HTML tags
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text(separator=" ")

    # Fix spacing
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_topics(text: str) -> List[str]:
    """Extract main topics and subtopics from the text.

    Args:
        text (str): The text content to analyze for topics

    Returns:
        List[str]: List of extracted topics (currently returns empty list as placeholder)
    """
    # This is a placeholder for topic extraction logic
    # We'll implement this in the next phase
    return []


def clean_criminal_law_articles() -> int:
    """Clean and process criminal law articles from raw data.

    This function reads raw criminal law articles from a CSV file,
    cleans the HTML content, extracts topics, and saves the processed
    data to a new CSV file.

    Returns:
        int: Number of successfully cleaned articles

    Raises:
        FileNotFoundError: If the input file cannot be found
        Exception: For other processing errors
    """
    input_file = "data/processed/criminal_law/criminal_law_articles.csv"
    output_dir = "data/processed/criminal_law"
    output_file = os.path.join(output_dir, "cleaned_criminal_law_articles.csv")

    try:
        print(f"Reading articles from: {input_file}")
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        df = pd.read_csv(input_file, encoding="utf-8")
        print(f"Successfully read {len(df)} articles")

        print("Cleaning article content...")
        df["cleaned_content"] = df["content"].apply(clean_html_content)

        # Remove articles with empty content after cleaning
        df = df[df["cleaned_content"].str.len() > 0]
        print(f"Retained {len(df)} articles after removing empty content")

        print("Extracting topics...")
        df["topics"] = df["cleaned_content"].apply(extract_topics)

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        print(f"Saving cleaned articles to: {output_file}")
        df.to_csv(output_file, index=False, encoding="utf-8")

        print("\nCleaning Statistics:")
        print(f"Original articles: {len(pd.read_csv(input_file))}")
        print(f"Articles after cleaning: {len(df)}")

        # Print sample of cleaned content
        if len(df) > 0:
            print("\nSample of cleaned content (first article):")
            print("-" * 80)
            print(df["cleaned_content"].iloc[0][:500] + "...")

        return len(df)
    except Exception as e:
        print(
            f"Error occurred in clean_criminal_law_articles: {str(e)}", file=sys.stderr
        )
        raise


if __name__ == "__main__":
    try:
        num_articles = clean_criminal_law_articles()
        print(f"\nTotal number of cleaned articles: {num_articles}")
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)
