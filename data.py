import os
from dataclasses import dataclass
from collections import Counter

import requests
import typer
import dask.bag as bag
from bs4 import BeautifulSoup
from rich.progress import track
from rich.console import Console

console = Console()

@dataclass
class ACLAnthologyDownloader:
    
    conf: str
    year: int

    def download(self, save_path: str = "papers"):
        
        if not os.path.exists(save_path):
            os.path.mkdir(save_path)
        
        if not os.path.isdir(save_path):
            raise Exception(f"{save_path} is not a directory.")

        url = f"https://aclanthology.org/events/{self.conf}-{self.year}/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        
        urls = []
        for url in track(soup.find_all('a', attrs={'title': 'Open PDF'})):
            link = url.attrs.get('href')
            *_, filename = os.path.split(link)
            urls.append({"url": link, "filename": filename})
        
        def write_from_url(url: str, save_path: str, filename: str):
            if os.path.exists(os.path.join(save_path, filename)):
                return {"status": "downloaded"}
            r = requests.get(url, stream=True)
            with open(os.path.join(save_path, filename), 'wb') as f:
                f.write(r.content)
            return {"status": "success"}
        
        b = bag.from_sequence(urls)
        status = b.map(lambda x: write_from_url(x["url"], save_path, x["filename"])).compute()
        counter = Counter([x["status"] for x in status])
        console.log(f"Added {counter['success']} papers. {counter['downloaded'] + counter['success']} papers in total.")


if __name__ == "__main__":

    def run(
        conf: str = typer.Option(default="acl"),
        year: int = typer.Option(default=2021),
    ):
        downloader  = ACLAnthologyDownloader(conf, year)
        downloader.download()

    typer.run(run)
