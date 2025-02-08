"""Filter criminal law articles from the blog data.

This module provides functionality to filter criminal law related articles
from the raw blog data based on content and metadata analysis.
"""

import os
import sys

import pandas as pd


def filter_criminal_law_articles(input_file: str, output_file: str) -> int:
    """Filter criminal law articles from the blog data.

    This function processes blog articles and identifies those related to criminal law
    based on the presence of TCK (Turkish Criminal Code) references and relevant keywords.

    Args:
        input_file (str): Path to the input CSV file containing blog articles
        output_file (str): Path where filtered articles will be saved

    Returns:
        int: Number of criminal law articles identified and saved

    Raises:
        FileNotFoundError: If the input file cannot be found
        Exception: For other processing errors
    """
    try:
        # Read input file
        df = pd.read_csv(input_file)
        print(f"Read {len(df)} articles from {input_file}")

        # Filter articles with TCK references
        tck_pattern = r"(?:TCK|Türk Ceza Kanunu)(?:\s+)?(?:m\.|madde|md\.|Art\.|Article)?(?:\s+)?(\d+)"
        df["has_tck_ref"] = df["content"].str.contains(
            tck_pattern, case=False, regex=True
        )

        # Filter articles with criminal law keywords
        keywords = [
            "ceza",
            "suç",
            "yaptırım",
            "hapis",
            "para cezası",
            "adli para",
            "mahkumiyet",
        ]
        keyword_pattern = "|".join(keywords)
        df["has_keywords"] = df["content"].str.contains(
            keyword_pattern, case=False, regex=True
        )

        # Keep articles with either TCK references or keywords
        df_filtered = df[df["has_tck_ref"] | df["has_keywords"]]
        print(f"Found {len(df_filtered)} criminal law articles")

        # Save filtered articles
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df_filtered.to_csv(output_file, index=False)
        print(f"Saved filtered articles to {output_file}")

        return len(df_filtered)

    except Exception as e:
        print(f"Error filtering articles: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        input_file = "data/raw/barandogan_blog_scraped/barandogan_articles.csv"
        output_file = "data/processed/criminal_law/criminal_law_articles.csv"
        num_articles = filter_criminal_law_articles(input_file, output_file)
        print(f"\nTotal number of criminal law articles processed: {num_articles}")
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)
