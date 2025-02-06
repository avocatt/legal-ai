import os
import json
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Tuple

# Update output path to use the new data structure
DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), "data")
RAW_OUTPUT_PATH = os.path.join(
    DATA_DIR, "raw", "legal_terms", "legal_terms.json")
PROCESSED_OUTPUT_PATH = os.path.join(
    DATA_DIR, "processed", "legal_terms", "legal_terms.json")


def scrape_legal_terms() -> Dict[str, str]:
    """Scrape legal terms and their definitions from the website."""
    base_url = "https://www.hukukiyardim.gov.tr/hukuk-sozlugu"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        terms_dict = {}
        term_elements = soup.find_all('dt')
        definition_elements = soup.find_all('dd')

        for term, definition in zip(term_elements, definition_elements):
            term_text = term.get_text(strip=True)
            definition_text = definition.get_text(strip=True)
            if term_text and definition_text:
                terms_dict[term_text] = definition_text

        return terms_dict

    except requests.RequestException as e:
        print(f"Error scraping legal terms: {str(e)}")
        return {}


def process_terms(terms: Dict[str, str]) -> Dict[str, str]:
    """Process and clean the scraped terms."""
    processed_terms = {}

    for term, definition in terms.items():
        # Clean and process the term
        cleaned_term = term.strip().lower()

        # Clean and process the definition
        cleaned_definition = definition.strip()

        # Add to processed terms if both term and definition are valid
        if cleaned_term and cleaned_definition:
            processed_terms[cleaned_term] = cleaned_definition

    return processed_terms


def save_terms(terms: Dict[str, str], is_processed: bool = False) -> None:
    """Save terms to JSON file."""
    output_path = PROCESSED_OUTPUT_PATH if is_processed else RAW_OUTPUT_PATH
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(terms, f, ensure_ascii=False, indent=2)
        print(f"Terms saved to {output_path}")
    except Exception as e:
        print(f"Error saving terms: {str(e)}")


def main():
    """Main function to run the scraper."""
    print("Starting legal terms scraper...")

    # Scrape terms
    raw_terms = scrape_legal_terms()
    if not raw_terms:
        print("No terms were scraped. Exiting...")
        return

    # Save raw terms
    save_terms(raw_terms, is_processed=False)
    print(f"Saved {len(raw_terms)} raw terms")

    # Process terms
    processed_terms = process_terms(raw_terms)

    # Save processed terms
    save_terms(processed_terms, is_processed=True)
    print(f"Saved {len(processed_terms)} processed terms")


if __name__ == "__main__":
    main()
