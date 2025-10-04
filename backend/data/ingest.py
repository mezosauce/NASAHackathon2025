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

def extract_sections_from_html(html: str) -> dict:
    """Extract semantic sections from PMC article HTML"""
    soup = BeautifulSoup(html, "html.parser")

    

    sections = {}

    # Find all section titles
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

    meta_tag = soup.find("meta", attrs={"name": "citation_pmid"})
    
    if meta_tag and meta_tag.get("content"):
        pmid = meta_tag.get("content")              #This is the pmid
     
        
    return sections

    # Fallback: full text if no sections found
    #if not sections:
    if True:
        sections["Article content"] = soup.get_text(" ", strip=True)

    return sections

def process_article(title: str, link: str) -> dict:
    """Process a single article"""
    pub_id = sanitize_filename(title)
    out = {
        "id": pub_id,
        "title": title,
        "link": link,
        "sections": None,
        "error": None
    }

    
    try:
        html = fetch_html(link)
        sections = extract_sections_from_html(html)
        out["sections"] = sections
    except Exception as e:
        out["error"] = str(e)
        logger.error("Error processing %s: %s", link, e)


    # Save JSON
    json_path = RAW_DIR / f"{pub_id}.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(out, jf)
    #print(f"Saved article JSON to: {json_path.resolve()}")
    return out

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