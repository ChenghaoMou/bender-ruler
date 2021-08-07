# Bender Ruler

Simple check for mentioning of languages for ACL Anthology conference papers.

## Set up

    pip install -r requirements.txt

## Usage

1.  Download all papers by running `python data.py --conf acl --year 2021`
2.  Set up GROBID server for pdf parser from [repo](https://github.com/titipata/scipdf_parser)
3.  Analyze the pdfs by running `python ruler.py`

## Note

-   papers that target at more than one language or no language at all **are not excluded**

## Stats

- 758/1385 papers mention at least one language.
- top languages are:
  - ('English', 716)
  - ('Spanish', 58)
  - ('French', 46)
  - ('Arabic', 44)
  - ('Chinese', 21)
  - ('Portuguese', 13)
  - ('Mandarin', 10)
  - ('Hebrew', 8)
  - ('Russian', 8)
  - ('Latin', 8)
  - ('Japanese', 4)
  - ('Cantonese', 3)
  - ('Tagalog', 3)
  - ('C++', 2)
  - ('German', 2)

Feedbacks and suggestions are welcome.
