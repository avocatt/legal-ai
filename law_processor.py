import re
import json
from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text


def clean_text(text):
    """Clean and normalize the text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove page numbers and headers
    text = re.sub(r'\n\d+\n', '\n', text)
    return text.strip()


def parse_law_structure(text):
    """Parse the law text into a structured format."""
    structure = {
        'title': '',
        'books': []
    }

    # Extract title
    title_match = re.search(r'TÜRK CEZA KANUNU', text)
    if title_match:
        structure['title'] = title_match.group(0)

    # Split text into lines for easier processing
    lines = text.split('\n')

    current_book = None
    current_part = None
    current_chapter = None
    current_article = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Book detection
        if re.match(r'^[A-ZĞÜŞİÖÇ]+ KİTAP$', line):
            current_book = {
                'title': line,
                'parts': []
            }
            structure['books'].append(current_book)
            current_part = None
            current_chapter = None
            continue

        # Part detection
        if re.match(r'^[A-ZĞÜŞİÖÇ]+ KISIM$', line):
            if current_book:
                current_part = {
                    'title': line,
                    'chapters': []
                }
                current_book['parts'].append(current_part)
                current_chapter = None
            continue

        # Chapter detection
        if re.match(r'^[A-ZĞÜŞİÖÇ]+ BÖLÜM$', line):
            if current_part:
                current_chapter = {
                    'title': line,
                    'articles': []
                }
                current_part['chapters'].append(current_chapter)
            continue

        # Article detection
        article_match = re.match(r'^Madde (\d+)-\s*(.+)$', line)
        if article_match and current_chapter:
            article_num = article_match.group(1)
            article_content = article_match.group(2)
            current_article = {
                'number': article_num,
                'content': article_content
            }
            current_chapter['articles'].append(current_article)
            continue

        # Append content to current article if it exists
        if current_article and line and not line.startswith('Madde '):
            current_article['content'] = current_article['content'] + ' ' + line

    return structure


def process_law_text(pdf_path, output_path):
    """Process the law text and save structured output."""
    # Extract text
    text = extract_text_from_pdf(pdf_path)

    # Parse structure
    structure = parse_law_structure(text)

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)

    return structure


if __name__ == "__main__":
    pdf_path = "türk-ceza-kanunu.pdf"
    output_path = "structured_law.json"

    structure = process_law_text(pdf_path, output_path)
    print(f"Law text has been processed and saved to {output_path}")

    # Print some statistics
    num_books = len(structure['books'])
    total_articles = sum(len(chapter['articles'])
                         for book in structure['books']
                         for part in book['parts']
                         for chapter in part['chapters'])
    print(f"\nStatistics:")
    print(f"Number of books: {num_books}")
    print(f"Total number of articles: {total_articles}")
