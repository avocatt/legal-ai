import json
import re
from pathlib import Path


def clean_article_content(content):
    """Clean up common OCR errors and format the content."""
    # Remove footnotes (numbered references)
    content = re.sub(r'\s*\d+\s*Bu Kanunun.*?bakınız\.', '', content)

    # Fix spacing around punctuation
    content = re.sub(r'\s+([.,;:!?])', r'\1', content)

    # Fix multiple spaces
    content = re.sub(r'\s+', ' ', content)

    # Fix spacing after punctuation
    content = re.sub(r'([.,;:!?])(\w)', r'\1 \2', content)

    # Remove any remaining footnote numbers
    content = re.sub(r'\s*\d+\s*$', '', content)

    return content.strip()


def extract_key_provisions(content):
    """Extract key provisions from the article content."""
    # Split content into paragraphs
    paragraphs = re.split(r'\(\d+\)', content)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Extract main points
    key_points = []
    for para in paragraphs:
        # Split on common conjunctions and punctuation
        points = re.split(r'(?<=[.!?])\s+(?=[A-ZĞÜŞİÖÇ])', para)
        key_points.extend([p.strip() for p in points if p.strip()])

    return key_points


def process_law_text(input_path, output_path):
    """Process the law text, clean it, and generate summaries."""
    # Load the structured law text
    with open(input_path, 'r', encoding='utf-8') as f:
        law_structure = json.load(f)

    # Process each article
    for book in law_structure['books']:
        for part in book['parts']:
            for chapter in part['chapters']:
                for article in chapter['articles']:
                    # Clean the content
                    article['content'] = clean_article_content(
                        article['content'])

                    # Extract key provisions
                    article['key_provisions'] = extract_key_provisions(
                        article['content'])

    # Save the processed structure
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(law_structure, f, ensure_ascii=False, indent=2)

    return law_structure


def print_statistics(structure):
    """Print statistics about the processed law text."""
    total_articles = 0
    total_provisions = 0

    for book in structure['books']:
        print(f"\nBook: {book['title']}")
        book_articles = 0
        book_provisions = 0

        for part in book['parts']:
            print(f"  Part: {part['title']}")
            part_articles = 0
            part_provisions = 0

            for chapter in part['chapters']:
                chapter_articles = len(chapter['articles'])
                chapter_provisions = sum(len(article['key_provisions'])
                                         for article in chapter['articles'])

                print(f"    Chapter: {chapter['title']}")
                print(f"      Articles: {chapter_articles}")
                print(f"      Key Provisions: {chapter_provisions}")

                part_articles += chapter_articles
                part_provisions += chapter_provisions

            print(
                f"    Total in Part - Articles: {part_articles}, Provisions: {part_provisions}")
            book_articles += part_articles
            book_provisions += part_provisions

        print(
            f"  Total in Book - Articles: {book_articles}, Provisions: {book_provisions}")
        total_articles += book_articles
        total_provisions += book_provisions

    print(f"\nTotal in Law:")
    print(f"Articles: {total_articles}")
    print(f"Key Provisions: {total_provisions}")


if __name__ == "__main__":
    input_path = "structured_law.json"
    output_path = "processed_law.json"

    # Process the law text
    processed_structure = process_law_text(input_path, output_path)
    print(f"Processed law text has been saved to {output_path}")

    # Print statistics
    print("\nStatistics:")
    print_statistics(processed_structure)
