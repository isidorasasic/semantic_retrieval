from typing import List
from classes import Section, Chunk
from utils import count_tokens
import warnings


class SectionChunker:
    def __init__(
        self,
        chunk_size: int,
        overlap: int = 0,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_sections(
        self,
        sections: List[Section],
        tool_name: str,
        document_type: str,
    ) -> List[Chunk]:
        """
        Convert Sections into structure-aware Chunks.
        """
        chunks: List[Chunk] = []
        chunk_counter = 0

        for section_idx, section in enumerate(sections):
            section_chunks = self._chunk_single_section(section)

            total = len(section_chunks)

            for i, text in enumerate(section_chunks):
                chunk_id = self._make_chunk_id(
                    source_doc=section.source_file,
                    section_index=section_idx,
                    chunk_index=i,
                )

                chunks.append(
                    Chunk(
                        id=chunk_id,
                        text=text,
                        tool_name=tool_name,
                        document_type=document_type,
                        source_doc=section.source_file,
                        section_title=section.title,
                        section_level=section.level,
                        chunk_index=i,
                        total_chunks=total,
                    )
                )

                chunk_counter += 1

        return chunks

    def _chunk_single_section(self, section: Section) -> List[str]:
        """
        Split a single section into token-bounded chunks,
        preserving paragraph boundaries where possible.
        """
        paragraphs = [p.strip() for p in section.content.split("\n\n") if p.strip()]

        chunks = []
        current = []

        current_tokens = 0

        for para in paragraphs:
            para_tokens = count_tokens(para)

            # Paragraph too large → hard split
            if para_tokens > self.chunk_size:
                if current:
                    chunks.append("\n\n".join(current))
                    current = []
                    current_tokens = 0

                hard_chunks = self._hard_split(para)
                chunks.extend(hard_chunks)
                continue

            # Fits in current chunk
            if current_tokens + para_tokens <= self.chunk_size:
                current.append(para)
                current_tokens += para_tokens
            else:
                chunks.append("\n\n".join(current))
                current = [para]
                current_tokens = para_tokens

        if current:
            chunks.append("\n\n".join(current))

        # Optional overlap
        if self.overlap > 0 and len(chunks) > 1:
            chunks = self._apply_overlap(chunks)

        return chunks

    def _hard_split(self, text: str) -> List[str]:
        """
        Split oversized text by token count.
        """
        words = text.split()
        chunks = []
        current = []

        current_tokens = 0

        for word in words:
            token_count = count_tokens(word)

            if current_tokens + token_count <= self.chunk_size:
                current.append(word)
                current_tokens += token_count
            else:
                chunks.append(" ".join(current))
                current = [word]
                current_tokens = token_count

        if current:
            chunks.append(" ".join(current))

        return chunks

    def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """
        Apply token-based overlap between consecutive chunks.
        """
        overlapped = []

        for i, chunk in enumerate(chunks):
            if i == 0:
                overlapped.append(chunk)
                continue

            prev = overlapped[-1]
            overlap_text = self._last_tokens(prev, self.overlap)

            combined = overlap_text + "\n\n" + chunk
            overlapped.append(combined)

        return overlapped

    def _last_tokens(self, text: str, token_count: int) -> str:
        words = text.split()
        return " ".join(words[-token_count:])

    def _make_chunk_id(
        self,
        source_doc: str,
        section_index: int,
        chunk_index: int,
    ) -> str:
        """
        Deterministic chunk ID.
        """
        return f"{source_doc}::s{section_index}::c{chunk_index}"
