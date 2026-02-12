from ingestion.parse_htmls import HTMLParser
from pathlib import Path
from utils import print_sections

DATA_DIR = Path(__file__).resolve().parents[0] / "data"

def main():

    doc_path = DATA_DIR / "flowmatrix" / "security_whitepaper.html"
    
    parser = HTMLParser()
    parsed_sections = parser.parse(doc_path)
    print_sections(parsed_sections, show_full_content=True)


if __name__ == "__main__":
    main()