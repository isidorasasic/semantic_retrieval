from dataclasses import dataclass
from typing import List


@dataclass
class Section:
    title: str
    level: int
    content: str
    source_file: str


@dataclass
class Chunk:
    id: str
    text: str
    tool_name: str
    document_type: str
    source_doc: str
    section_title: str
    section_level: int
    chunk_index: int
    total_chunks: int
