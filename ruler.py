import scipdf
import os
import json
from tqdm import tqdm
from typing import List


def extract_data(dir: str):
    for root, _, files in os.walk(dir):
        for file in tqdm(files):
            filename, _ = os.path.splitext(file)
            try:
                article_dict = scipdf.parse_pdf_to_dict(os.path.join(root, file))
                with open(os.path.join(root, f"{filename}.json"), 'w') as o:
                    o.write(json.dumps(article_dict))
            except Exception:
                pass

def load_data(dir: str):

    documents: List[str] = []

    for root, _, files in os.walk(dir):
        for file in tqdm(files):
            filename, ext = os.path.splitext(file)
            if ext != ".json":
                continue
            with open(os.path.join(root, file), 'r') as f:
                d = json.loads(f.read())
                documents.append(
                    d["title"] + " " + d["abstract"] + " ".join([s["heading"] + " " + s["text"] for s in d["sections"]])
                )
    
    return documents

def analyze(documents: List[str]):

    count = 0
    for document in documents:
        if "english" in document.lower():
            count += 1
    print(count, len(documents))
    return count

if __name__ == '__main__':

    documents = load_data("papers")
    analyze(documents)