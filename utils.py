from typing import List
from classes import Section
from classes import Chunk


def print_sections(
    sections: List[Section],
    max_content_length: int = 500,
    show_full_content: bool = False,
) -> None:
    """
    Pretty-print parsed sections for debugging.

    Args:
        sections: List of parsed Section objects
        max_content_length: Maximum characters to display per section
        show_full_content: If True, prints full content
    """

    if not sections:
        print("No sections parsed.")
        return

    print("\n========== PARSED SECTIONS ==========\n")

    for i, section in enumerate(sections, start=1):
        print("-" * 80)
        print(f"Section {i}")
        print(f"Source File : {section.source_file}")
        print(f"Title     : {section.title}")
        print(f"Level       : H{section.level}")
        print(f"Content Len : {len(section.content)} characters")
        print()

        if show_full_content:
            print(section.content)
        else:
            preview = section.content[:max_content_length]
            if len(section.content) > max_content_length:
                preview += "\n...\n[TRUNCATED]"
            print(preview)

        print()

    print("-" * 80)
    print(f"Total Sections: {len(sections)}")
    print("=====================================\n")


def count_tokens(text: str) -> int:
    """
    Approximate token count.
    """
    return len(text.split())


def print_chunks(
    chunks: List[Chunk],
    max_content_length: int = 500,
    show_full_content: bool = False,
) -> None:
    """
    Pretty-print chunks for debugging and validation.

    Args:
        chunks: List of Chunk objects
        max_content_length: Max characters to show per chunk
        show_full_content: If True, prints full chunk text
    """

    if not chunks:
        print("No chunks to display.")
        return

    print("\n========== GENERATED CHUNKS ==========\n")

    for i, chunk in enumerate(chunks, start=1):
        print("-" * 80)
        print(f"Chunk {i}")
        print(f"ID            : {chunk.id}")
        print(f"Source Doc    : {chunk.source_doc}")
        print(f"Tool          : {chunk.tool_name}")
        print(f"Document Type : {chunk.document_type}")
        print(f"Section       : {chunk.section_title} (H{chunk.section_level})")
        print(f"Chunk Index   : {chunk.chunk_index + 1} / {chunk.total_chunks}")
        print(f"Token Count   : {count_tokens(chunk.text)}")
        print()

        if show_full_content:
            print(chunk.text)
        else:
            preview = chunk.text[:max_content_length]
            if len(chunk.text) > max_content_length:
                preview += "\n...\n[TRUNCATED]"
            print(preview)

        print()

    print("-" * 80)
    print(f"Total Chunks: {len(chunks)}")
    print("=====================================\n")
