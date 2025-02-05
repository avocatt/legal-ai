import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from pathlib import Path
import re

class LegalTermScraper:
    def __init__(self):
        self.base_url = "https://sozluk.adalet.gov.tr"
        self.terms = {}
        self.turkish_alphabet = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZÂÎÛ'

    def get_soup(self, url, delay=1):
        time.sleep(delay)  # Rate limiting
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def scrape_terms_for_letter(self, letter_url, letter):
        soup = self.get_soup(letter_url)
        
        # Find total pages from the pagination text
        pagination_info = soup.find('div', class_='alert alert-info')
        if pagination_info:
            total_terms = int(pagination_info.text.split()[0])
            total_pages = (total_terms + 39) // 40  # 40 terms per page
        else:
            total_pages = 1
            
        print(f"Processing letter {letter} ({total_pages} pages)")
        terms_found = 0
        
        for page in range(1, total_pages + 1):
            page_url = f"{letter_url}?Sayfa={page}" if page > 1 else letter_url
            print(f"  Page {page}/{total_pages}", end='\r')
            
            soup = self.get_soup(page_url)
            content_area = soup.find('div', class_='ankat')
            
            # Find all term divs
            term_divs = content_area.find_all('div', class_='terim')
            
            for term_div in term_divs:
                # Get term from col-md-4 div
                term_element = term_div.find('div', class_='col-md-4')
                # Get definition from col-md-8 div
                definition_element = term_div.find('div', class_='col-md-8')
                
                if term_element and definition_element:
                    term = term_element.get_text(strip=True)
                    definition = definition_element.get_text(strip=True)
                    
                    # Skip empty or invalid terms
                    if not term or not definition:
                        continue
                        
                    # Clean up definition (remove any trailing labels)
                    definition = re.sub(r'\s*\[.*?\]\s*$', '', definition)
                    
                    # Store only the definition
                    self.terms[term] = definition
                    terms_found += 1
            
            # Add a small delay between pages
            if page < total_pages:
                time.sleep(2)
        
        print(f"\nFound {terms_found} terms for letter {letter}")
        return terms_found

    def save_terms(self):
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "legal_terms.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.terms, f, ensure_ascii=False, indent=2)
        
        print(f"\nSaved {len(self.terms)} terms to {output_file}")

    def run(self):
        """Run the scraper for all letters."""
        print("Starting to scrape all letters...")
        total_terms = 0
        
        for letter in self.turkish_alphabet:
            try:
                url = f"{self.base_url}/Harf/{letter}"
                terms_found = self.scrape_terms_for_letter(url, letter)
                total_terms += terms_found
                
                # Add a delay between letters
                if letter != self.turkish_alphabet[-1]:
                    time.sleep(3)
                    
            except Exception as e:
                print(f"Error processing letter {letter}: {str(e)}")
                continue
        
        self.save_terms()
        print(f"\nScraping completed! Total terms collected: {total_terms}")

if __name__ == "__main__":
    scraper = LegalTermScraper()
    scraper.run()