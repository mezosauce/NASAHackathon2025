"""
chunk_and_prepare.py

Reads per-publication JSONs from data/raw/ (created by ingest.py),
chunks sections into smaller overlapping pieces, and writes
chunk JSONs into data/chunks/ for embedding and retrieval.

Each chunk JSON contains:
- text: the chunk text
- section: the canonical section name (Results, Conclusion, etc.)
- publication_id: the source article's ID
- chunk_index: order of the chunk in that section
"""

import ujson as json
from pathlib import Path

# Directories
RAW_DIR = Path("data/raw")
CHUNKS_DIR = Path("data/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

# Chunking parameters
TARGET_WORDS = 250   # words per chunk
OVERLAP_WORDS = 50   # overlap between consecutive chunks


def chunk_text(text: str, target_words=TARGET_WORDS, overlap=OVERLAP_WORDS):
    """
    Split text into overlapping chunks.
    """
    words = text.split()
    if len(words) <= target_words:
        return [text]

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + target_words, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = end - overlap  # maintain overlap
    return chunks


def prioritized_sections(sections: dict):
    """
    Return sections in order of priority:
    Results > Conclusion > Abstract > Discussion > Introduction > Methods
    """
    order = ["results", "conclusion", "abstract", "discussion", "introduction", "methods"]
    ordered = [(k, sections[k]) for k in order if k in sections]
    # Add any other sections at the end
    for k, v in sections.items():
        if k not in dict(ordered):
            ordered.append((k, v))
    return ordered


def process_article(json_file: Path):
    article = json.load(open(json_file, "r", encoding="utf-8"))
    pub_id = article["id"]
    sections = article.get("sections", {})

    for sec_name, sec_text in prioritized_sections(sections):
        chunks = chunk_text(sec_text)
        for idx, c in enumerate(chunks):
            chunk_file = CHUNKS_DIR / f"{pub_id}_{sec_name}_{idx}.json"
            json.dump(
                {
                    "text": c,
                    "section": sec_name,
                    "publication_id": pub_id,
                    "chunk_index": idx,
                },
                open(chunk_file, "w", encoding="utf-8"),
            )


def main():
    json_files = list(RAW_DIR.glob("*.json"))
    if not json_files:
        print("No raw JSON files found in", RAW_DIR)
        return

    for jf in json_files:
        process_article(jf)

    print(f"Chunking complete. Chunks saved in {CHUNKS_DIR.resolve()}")


if __name__ == "__main__":
    main()
