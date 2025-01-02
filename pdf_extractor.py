import PyPDF2
import pdfplumber
import re
from pathlib import Path


def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return text


def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber."""
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text


def compare_extractions(pdf_path):
    """Compare extractions from both libraries."""
    print("Extracting with PyPDF2...")
    pypdf2_text = extract_with_pypdf2(pdf_path)
    print(f"PyPDF2 extracted {len(pypdf2_text)} characters")

    print("\nExtracting with pdfplumber...")
    pdfplumber_text = extract_with_pdfplumber(pdf_path)
    print(f"pdfplumber extracted {len(pdfplumber_text)} characters")

    # Save both extractions for comparison
    Path('extracted_pypdf2.txt').write_text(pypdf2_text, encoding='utf-8')
    Path('extracted_pdfplumber.txt').write_text(
        pdfplumber_text, encoding='utf-8')

    return pypdf2_text, pdfplumber_text


if __name__ == "__main__":
    pdf_path = "türk-ceza-kanunu.pdf"
    pypdf2_text, pdfplumber_text = compare_extractions(pdf_path)
