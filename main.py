from ingestion.parse_html import HTMLParser
from ingestion.chunk_html import SectionChunker
from pathlib import Path
from utils import print_sections, print_chunks

DATA_DIR = Path(__file__).resolve().parents[0] / "data"

def main():

    doc_path = DATA_DIR / "flowmatrix" / "security_whitepaper.html"
    
    parser = HTMLParser()
    parsed_sections = parser.parse(doc_path)
    # print_sections(parsed_sections, show_full_content=True)

    chunker = SectionChunker(chunk_size=0, overlap=30)

    chunks =chunker.chunk_sections(
        sections=parsed_sections,
        tool_name="flowmatrix",
        document_type="security_whitepaper"
    )

    print(f"Generated {len(chunks)} chunks")

    print_chunks(chunks=chunks, show_full_content=True)


if __name__ == "__main__":
    main()