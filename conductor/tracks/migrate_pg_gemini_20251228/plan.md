# Plan: Migrate RAG Pipeline to PostgreSQL and Gemini

## Phase 1: Environment and Database Setup [checkpoint: bb460c6]
- [x] Task: Set up PostgreSQL with pgvector (local or Docker) and update `.env` d1368ae
- [x] Task: Update `pyproject.toml` with `asyncpg` and remove MongoDB dependencies 54b7efe
- [x] Task: Create PostgreSQL schema and migration scripts for `documents` and `chunks` tables 9961a59
- [x] Task: Conductor - User Manual Verification 'Environment and Database Setup' (Protocol in workflow.md)

## Phase 2: Core Infrastructure Migration [checkpoint: bb7406e]
- [x] Task: Write tests for PostgreSQL connection and dependency injection b6c3046
- [x] Task: Implement PostgreSQL connection management in `src/dependencies.py` b12388f
- [x] Task: Write tests for Gemini embedding provider db46df5
- [x] Task: Implement Gemini embedding provider in `src/providers.py` 04808ee
- [x] Task: Conductor - User Manual Verification 'Core Infrastructure Migration' (Protocol in workflow.md)

## Phase 3: Ingestion Pipeline Migration [checkpoint: 0bbbc37]
- [x] Task: Write tests for PostgreSQL ingestion logic 72ee68f
- [x] Task: Update `src/ingestion/ingest.py` to support PostgreSQL 5aa5534
- [x] Task: Write tests for chunk storage and retrieval 884a17d
- [x] Task: Conductor - User Manual Verification 'Ingestion Pipeline Migration' (Protocol in workflow.md)

## Phase 4: Search Tools and Agent Integration
- [x] Task: Write tests for PostgreSQL hybrid search (Vector + Full-Text) 3601b19
- [x] Task: Re-implement search tools in `src/tools.py` using SQL and pgvector f5ed32e
- [x] Task: Update `src/agent.py` and `src/cli.py` to ensure compatibility with PostgreSQL results 418fb93
- [x] Task: Run comprehensive E2E tests to verify the entire pipeline (User Manual Verification)
- [ ] Task: Conductor - User Manual Verification 'Search Tools and Agent Integration' (Protocol in workflow.md)
