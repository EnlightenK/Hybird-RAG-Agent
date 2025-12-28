# Plan: Migrate RAG Pipeline to PostgreSQL and Gemini

## Phase 1: Environment and Database Setup
- [x] Task: Set up PostgreSQL with pgvector (local or Docker) and update `.env` d1368ae
- [ ] Task: Update `pyproject.toml` with `asyncpg` and remove MongoDB dependencies
- [ ] Task: Create PostgreSQL schema and migration scripts for `documents` and `chunks` tables
- [ ] Task: Conductor - User Manual Verification 'Environment and Database Setup' (Protocol in workflow.md)

## Phase 2: Core Infrastructure Migration
- [ ] Task: Write tests for PostgreSQL connection and dependency injection
- [ ] Task: Implement PostgreSQL connection management in `src/dependencies.py`
- [ ] Task: Write tests for Gemini embedding provider
- [ ] Task: Implement Gemini embedding provider in `src/providers.py`
- [ ] Task: Conductor - User Manual Verification 'Core Infrastructure Migration' (Protocol in workflow.md)

## Phase 3: Ingestion Pipeline Migration
- [ ] Task: Write tests for PostgreSQL ingestion logic
- [ ] Task: Update `src/ingestion/ingest.py` to support PostgreSQL
- [ ] Task: Write tests for chunk storage and retrieval
- [ ] Task: Conductor - User Manual Verification 'Ingestion Pipeline Migration' (Protocol in workflow.md)

## Phase 4: Search Tools and Agent Integration
- [ ] Task: Write tests for PostgreSQL hybrid search (Vector + Full-Text)
- [ ] Task: Re-implement search tools in `src/tools.py` using SQL and pgvector
- [ ] Task: Update `src/agent.py` and `src/cli.py` to ensure compatibility with PostgreSQL results
- [ ] Task: Run comprehensive E2E tests to verify the entire pipeline
- [ ] Task: Conductor - User Manual Verification 'Search Tools and Agent Integration' (Protocol in workflow.md)
