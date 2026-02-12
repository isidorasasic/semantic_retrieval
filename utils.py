from typing import List
from classes import Section


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
        print(f"Heading     : {section.title}")
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
