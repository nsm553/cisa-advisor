from unicodedata import name
from bs4 import BeautifulSoup
import os
from utils import create_output_directory, get_page_content
from cisa_scrapper import parse_advisory_page
from datetime import datetime
import argparse
import json
import re

BASE_URL = "https://www.cisa.gov/news-events/cybersecurity-advisories"
OUTPUT_DIR = "target"

'''
Scrape all advisories, build markups for each of them
'''
def getAllAdvisories():
    parser = argparse.ArgumentParser(description='Scrape CISA cybersecurity advisories')
    parser.add_argument('--output-dir', default=OUTPUT_DIR, help='Directory to save the output files')
    args = parser.parse_args()
    
    try:
        create_output_directory(args.output_dir)
    except Exception as e:
        print(f"Error output directory {args.output_dir} to save generated files: {e}")

    advisories = {}
    
    # Start with the first page
    page = 1
    while True:
        print(f"Processing page {page}")
        url = f"{BASE_URL}?page={page-1}"

        content = get_page_content(url)
        
        if not content:
            break
        
        # soup = BeautifulSoup(open("cisa_news_events.html", 'r', encoding='utf-8'), 'html.parser')
        soup = BeautifulSoup(content, 'html.parser')
        advisory_rows = soup.find_all('div', class_='c-view__row')
        print(f"div: {len(advisory_rows)}")

        if not advisory_rows:
            print("No Advisory Rows found in this page to process")
            page += 1   
            continue

        for advisory_row in advisory_rows:
            advisory_type = advisory_row.find('div', class_='c-teaser__meta')
            print(f"advisory_type: {advisory_type.text}")
            
            if not advisory_type.text or "alert" not in advisory_type.text.lower():
                print("Not an Advisory, skipping this row")
                continue

            advisory_links = advisory_row.find_all('a')
            
            if not advisory_links:
                break
            
            for link in advisory_links:
                advisory = link.text.strip()
                advisory_url = f"https://www.cisa.gov{link.get('href')}"
                print(f"Processing advisory: {advisory}, at: {advisory_url}")
                advisories[advisory] = advisory_url
            
                advisory_content, html_content = parse_advisory_page(advisory_url)
                if advisory_content:
                    try:
                        md_file, html_file = save_files(advisory_content, html_content, args.output_dir)
                        print(f"Saved files: {md_file} and {html_file}")
                    except Exception as e:
                        print(f"Error saving files for {advisory_url}: {e}")
            
        page += 1

'''
Save both actual html and markdown content in individual files
'''
def save_files(advisory, html_content, output_dir):
    title = advisory['title'].replace('/', '-')
    date = datetime.now
    date_string = datetime.now().strftime("%Y-%m-%d-%f")

    # Create HTML file
    html_filename = os.path.join(output_dir, f"{title}_{date_string}.html")
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Create Markdown file
    md_filename = os.path.join(output_dir, f"{title}_{date_string}.json")
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(advisory))
    
    return md_filename, html_filename


if __name__ == "__main__":
    getAllAdvisories()
