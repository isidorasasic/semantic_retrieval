from pydantic import BaseModel, field_validator
from pathlib import Path


ALLOWED_EMBEDDING_MODELS = {
    "l2-text-embedding-3-small",
    "l2-text-embedding-3-large",
}


class AppConfig(BaseModel):
    embedding_model: str = "l2-text-embedding-3-small"
    chunk_size: int
    overlap: int = 0
    top_k: int = 3
    neighbors: int = 1
    index_path: Path = Path("./data/embeddings")

    @field_validator("embedding_model")
    @classmethod
    def validate_embedding_model(cls, v: str) -> str:
        if v not in ALLOWED_EMBEDDING_MODELS:
            raise ValueError(
                f"embedding_model must be one of {sorted(ALLOWED_EMBEDDING_MODELS)}"
            )
        return v

    @field_validator("chunk_size")
    @classmethod
    def validate_chunk_size(cls, v: int) -> int:
        if not isinstance(v, int) or v <= 0:
            raise ValueError("chunk_size must be a positive integer")
        return v

    @field_validator("overlap")
    @classmethod
    def validate_overlap(cls, v: int, info) -> int:
        chunk_size = info.data.get("chunk_size")
        if chunk_size is not None and v >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        return v
