#!/usr/bin/env python3
"""
ingest.py - Ingest NCBI PMC articles via HTML extraction

- Reads CSV with Title + Link
- Fetches HTML for each article
- Extracts semantic sections (Abstract, Introduction, Results, Discussion, Conclusion)
- Saves JSON per article: data/raw/<pub_id>.json
"""

import csv
import time
import re
import logging
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import ujson as json
from tqdm import tqdm

# Directories
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# HTTP settings
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NASA-Bio-Hack/1.0)"}
TIMEOUT = 20
RETRY = 3
SLEEP_BETWEEN = 0.2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest")

articleJSON = {
    "id": None,
    "title": None,
    "link": None,
    "authors": None,
    "year": None,
    "topic": None,
    "sections": None,
    "OSD": None,
    "error": None
}



def sanitize_filename(s: str) -> str:
    """Convert a title into a filesystem-safe string"""
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)[:100]

def fetch_html(url: str) -> str:
    """Fetch HTML content with retries"""
    for attempt in range(RETRY):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            return r.text
        except Exception as e:
            logger.warning("Attempt %d failed to fetch %s: %s", attempt + 1, url, e)
            time.sleep(1 + attempt * 2)
    raise RuntimeError(f"Failed to fetch {url}")

def extract_info_from_html(html: str):
    """Extract semantic sections from PMC article HTML"""
    soup = BeautifulSoup(html, "html.parser")

    # Find the pmid
    meta_tag = soup.find("meta", attrs={"name": "citation_pmid"})
    if meta_tag and meta_tag.get("content"):
        articleJSON["id"] = meta_tag.get("content")

    # Find the authors
    authors = []
    authors_html = soup.find_all("meta", attrs={"name": "citation_author"})
    for meta_tag in authors_html:
        if meta_tag and meta_tag.get("content"):
            authors.append(meta_tag.get("content"))
    articleJSON["authors"] = authors

    # Find the year
           
    meta_tag = soup.find("meta", attrs={"name": "citation_publication_date"})
    if meta_tag and meta_tag.get("content"):
        articleJSON["year"] = meta_tag.get("content")       #Actually stores publication date as a string

    sections = {}
    OSD_list = []
    # Find all section titles (and OIDs mentioned in article)
    for title_tag in soup.find_all(class_="pmc_sec_title"):
        #section_title = title_tag.get_text(strip=True)
        section_title = ''.join(title_tag.stripped_strings)
        section_text_parts = []

        # Collect all sibling paragraphs until next section
        for sibling in title_tag.find_next_siblings():
            # Stop when the next section starts
            if "pmc_sec_title" in sibling.get("class", []):
                break
            # Collect text
            section_text_parts.append(sibling.get_text(" ", strip=True))
            
        section_text = "\n".join(section_text_parts).strip()
        if section_title and section_text:
            sections[section_title] = section_text
            OSD_list.extend(re.findall(r'OSD-\d+', section_text))

    OSD_list = list(set(OSD_list))      #remove duplicates
    if(OSD_list):        
        print(OSD_list)

    articleJSON["sections"] = sections

def process_article(title: str, link: str):         # "Process a single article"

    for key in articleJSON:         #clear global JSON dictionary
        articleJSON[key] = None

    articleJSON["title"] = title
    articleJSON["link"] = link

    file_name = sanitize_filename(title)
    
    try:
        html = fetch_html(link)
        extract_info_from_html(html)
  

    except Exception as e:
        articleJSON["error"] = str(e)
        logger.error("Error processing %s: %s", link, e)

    # Save JSON
    json_path = RAW_DIR / f"{file_name}.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(articleJSON, jf)
    #print(f"Saved article JSON to: {json_path.resolve()}")

def process_csv(csv_path: str):
    """Read CSV and process all articles"""
    rows = []
    with open(csv_path, newline="", encoding="utf-8-sig") as fh:  # handles BOM
        reader = csv.DictReader(fh)
        for row in reader:
            title = (row.get("Title") or row.get("title") or "").strip()
            link = (row.get("Link") or row.get("link") or row.get("URL") or "").strip()
            if link:
                rows.append((title, link))

    for title, link in tqdm(rows, desc="Ingesting articles"):
        process_article(title, link)
        time.sleep(SLEEP_BETWEEN)

    logger.info("Ingestion complete.")

if __name__ == "__main__":
    """import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest.py articles.csv")
        raise SystemExit(1)
    csv_path = sys.argv[1]
    process_csv(csv_path)"""
    process_csv(r'C:\Users\muhaa\Documents\GitHub\NASAHackathon2025\backend\data\SB_publication_PMC.csv')