import ujson as json
import os
from pathlib import Path

from db.client import supabase

directory = Path("data/raw")
json_files = list(directory.glob("*.json"))
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        articleJSON = json.load(f)
        # Insert into Supabase
  
        supabase.table("articles").insert({
            "id": articleJSON['id'],
            "title": articleJSON['title'],
            "URL": articleJSON['link'],
            "authors": articleJSON['authors'],
            "year": articleJSON['year'],
            "abstract": articleJSON['abstract'],
            "sections": json.dumps(articleJSON['sections']),
            "OSD": json.dumps(articleJSON['OSD']),
            "error": articleJSON['error']
        }).execute()
        
   

