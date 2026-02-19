from bs4 import BeautifulSoup
from pathlib import Path
from typing import List
from classes import Section


class HTMLParser:
    def __init__(self):
        pass

    def parse(self, file_path: Path) -> List[Section]:
        """
        Parse an HTML file and return structured sections
        preserving heading hierarchy and content grouping.
        """
        html = file_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")

        sections: List[Section] = []

        current_heading = "Document Start"
        current_level = 0
        current_content = []

        for element in soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table"]
        ):

            # If heading → start new section
            if element.name.startswith("h"):
                # Save previous section if it has content
                if current_content:
                    sections.append(
                        Section(
                            title=current_heading.strip(),
                            level=current_level,
                            content="\n\n".join(current_content).strip(),
                            source_file=file_path,
                        )
                    )
                    current_content = []

                current_heading = element.get_text(strip=True)
                current_level = int(element.name[1])

            else:
                text = self._extract_text(element)
                if text:
                    current_content.append(text)

        # Append last section
        if current_content:
            sections.append(
                Section(
                    title=current_heading.strip(),
                    level=current_level,
                    content="\n\n".join(current_content).strip(),
                    source_file=file_path,
                )
            )

        return sections

    def _extract_text(self, element) -> str:
        """
        Extract clean text from supported HTML elements.
        """

        if element.name == "p":
            return element.get_text(strip=True)

        elif element.name in ["ul", "ol"]:
            items = [
                f"- {li.get_text(strip=True)}"
                for li in element.find_all("li")
            ]
            return "\n".join(items)

        # elif element.name == "table":
        #     rows = []
        #     for tr in element.find_all("tr"):
        #         cells = [
        #             cell.get_text(strip=True)
        #             for cell in tr.find_all(["td", "th"])
        #         ]
        #         if cells:
        #             rows.append(" | ".join(cells))
        #     return "\n".join(rows)

        return ""
