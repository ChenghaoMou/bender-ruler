import json
import os
from typing import List
from collections import defaultdict, Counter

import scipdf
import spacy
from rich.console import Console
from rich.progress import track

console = Console()

def extract_data(dir: str):
    """Extract data from a directory of pdf files. Extracted data follows the GROBID data format.
    See https://github.com/kermitt2/grobid and https://github.com/titipata/scipdf_parser.

    Parameters
    ----------
    dir : str
        The directory of pdf files
    """
    for root, _, files in os.walk(dir):
        for file in track(files):
            filename, _ = os.path.splitext(file)
            if os.path.exists(os.path.join(root, f"{filename}.json")):
                continue
            try:
                article_dict = scipdf.parse_pdf_to_dict(os.path.join(root, file))
                with open(os.path.join(root, f"{filename}.json"), 'w') as o:
                    o.write(json.dumps(article_dict))
            except Exception:
                pass

def load_data(dir: str) -> List[str]:
    """Extract all text data from extracted GROBID data in the given directory.

    Parameters
    ----------
    dir : str
        Directory of extracted GROBID data

    Returns
    -------
    List[str]
        List of extracted documents
    """
    documents: List[str] = []

    for root, _, files in os.walk(dir):
        for file in track(files):
            _, ext = os.path.splitext(file)
            if ext != ".json":
                continue
            with open(os.path.join(root, file), 'r') as f:
                d = json.loads(f.read())
                documents.append(
                    (d["title"], d["title"] + " " + d["abstract"] + " ".join([s["heading"] + " " + s["text"] for s in d["sections"]]))
                )
    
    return documents

def analyze(documents: List[str]):

    mentions = []
    nlp = spacy.load("en_core_web_sm", disable=["tagger", "parser", "lemmatizer"])
    titles, documents = zip(*documents)
    counter = Counter()
    non_empty: int = 0

    for title, doc in track(zip(titles, documents), total=len(titles)):
        curr = defaultdict(int)
        with nlp.select_pipes(enable="ner"):
            doc = nlp(doc) # not using pipe because it is too slow
            for ent in doc.ents:
                if ent.label_ == "LANGUAGE":
                    curr[ent.text.title()] += 1
                    
            if curr:
                non_empty += 1
                for lan in curr:
                    counter[lan.title()] += 1
            
            mentions.append((title, curr))
    
    console.print(f"{non_empty}/{len(titles)} paper(s) mention(s) at least one language.")
    console.print(f"Languages mentioned: {counter.most_common()}")

    return mentions

if __name__ == '__main__':

    extract_data("papers")
    documents = load_data("papers")
    analyze(documents)