import os
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from rich.progress import track
import typer

@dataclass
class ACLAnthologyDownloader:
    
    conf: str
    year: int

    def download(self, save_path: str = "papers"):
        
        url = f"https://aclanthology.org/events/{self.conf}-{self.year}/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        
        for url in track(soup.find_all('a', attrs={'title': 'Open PDF'})):
            link = url.attrs.get('href')
            *_, filename = os.path.split(link)
            r = requests.get(link, stream=True)
            with open(os.path.join(save_path, filename), 'wb') as f:
                f.write(r.content)


if __name__ == "__main__":

    def run(
        conf: str = typer.Option(default="acl"),
        year: int = typer.Option(default=2021),
    ):
        downloader  = ACLAnthologyDownloader(conf, year)
        downloader.download()

    
