# Specification: Migrate RAG Pipeline to PostgreSQL and Gemini

## Overview
This track involves migrating the existing RAG system from MongoDB Atlas to PostgreSQL with `pgvector`. Additionally, the embedding generation will be transitioned from the current provider (OpenAI/OpenRouter) to Google Gemini.

## Requirements

### Database Migration
- Replace MongoDB collections (`documents`, `chunks`) with PostgreSQL tables.
- Implement `pgvector` for storing and searching high-dimensional embeddings.
- Maintain the "Two-Collection Pattern" (Metadata table and Chunks table).
- Implement Hybrid Search logic in PostgreSQL (Vector + Full-Text Search).

### Embedding Integration
- Replace existing embedding logic with Google Gemini Generative AI Embeddings.
- Update the chunking and ingestion pipeline to handle the new embedding dimensions (if different).

### Codebase Updates
- Update `src/dependencies.py` to handle PostgreSQL connections using `asyncpg`.
- Refactor `src/tools.py` to use SQL queries for vector and text search.
- Update `src/ingestion/ingest.py` to store data in PostgreSQL.
- Ensure all Pydantic models remain consistent with the new data source.

### Testing
- Maintain >80% code coverage.
- Implement unit tests for PostgreSQL operations and Gemini integration.
- Ensure the E2E RAG pipeline remains functional after migration.

## Success Criteria
- Successful ingestion of documents into PostgreSQL.
- Hybrid search returns relevant results comparable to the MongoDB implementation.
- All tests pass with required coverage.
- CLI remains fully functional with the new backend.
