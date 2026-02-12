Overview

This project implements the Retrieval component of a Retrieval-Augmented Generation (RAG) architecture.

The system ingests structured HTML documents, parses them into structure-aware chunks, generates vector embeddings, persists the index to disk, and provides a command-line interface for semantic search over the indexed content.

This phase focuses exclusively on:

- Retrieval logic
- Embedding generation
- Structure-aware chunking
- Vector persistence
- Context expansion

No conversational features are included.