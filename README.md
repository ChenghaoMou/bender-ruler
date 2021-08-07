# Bender Ruler

Simple check for mentioning of languages for ACL 2021 papers.

## Set up

    pip install -r requirements.txt

## Usage

1.  Download all papers by running `python data.py`
2.  Set up GROBID server for pdf parser from [repo](https://github.com/titipata/scipdf_parser)
3.  Analyze the pdfs by running `python ruler.py`

## Note

-   only 520/1168 papers are downloadable from arXiv
-   topics that target at more than one language or no language at all **are not excluded**

## Stats

-   258/520 papers mention at least one language
-   top languages are
    -   English 248
    -   Spanish 21
    -   Chinese 10 + Mandarin 2
    -   French 11
    -   Arabic 10
    -   Tagalog 4
    -   Latin 3
    -   Hebrew 3
    -   Russian 3

Feedbacks and suggestions are welcome.
