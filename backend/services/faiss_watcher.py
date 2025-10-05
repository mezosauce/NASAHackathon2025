# backend/services/faiss_watcher.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.services.faiss_service import load_index_and_model
from pathlib import Path
import time

INDEX_DIR = Path("data/index")

class IndexChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("faiss.index") or event.src_path.endswith("index_to_chunk.json"):
            print(f"Detected change in {event.src_path}, reloading FAISS index...")
            load_index_and_model()

def start_watcher(): 
    event_handler = IndexChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(INDEX_DIR), recursive=False)
    observer.start()
    print("Started FAISS index watcher")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
