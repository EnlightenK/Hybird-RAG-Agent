# PostgreSQL RAG Agent with Gemini - Intelligent Knowledge Base Search

Agentic RAG system combining PostgreSQL (pgvector) with Pydantic AI for intelligent document retrieval. Supports OpenAI and Google Gemini models.

## Features

- **Hybrid Search**: Combines semantic vector search (pgvector) with full-text keyword search (PostgreSQL TSVector) using Reciprocal Rank Fusion (RRF)
  - Proven RRF implementation for optimal retrieval quality
  - Concurrent execution for minimal latency overhead
- **Multi-Format Ingestion**: PDF, Word, PowerPoint, Excel, HTML, Markdown, Audio transcription
- **Intelligent Chunking**: Docling HybridChunker preserves document structure and semantic boundaries
- **Conversational CLI**: Rich-based interface with real-time streaming and tool call visibility
- **Multiple LLM Support**: OpenAI, OpenRouter, Ollama, Gemini
- **Open Source**: Runs on local PostgreSQL or any cloud provider

## Prerequisites

- Python 3.10+
- PostgreSQL 15+ with `pgvector` extension
- LLM provider API key (OpenAI, OpenRouter, Gemini, etc.)
- Embedding provider API key (OpenAI or Gemini)
- UV package manager

## Quick Start

### 1. Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup Project

```bash
git clone https://github.com/EnlightenK/Hybird-RAG-Agent.git
cd Hybird-RAG-Agent

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Unix/Mac
.venv\Scripts\activate     # Windows
uv sync
```

### 3. Set Up PostgreSQL

You can run PostgreSQL locally or using Docker.

**Option A: Docker (Recommended)**
```bash
docker-compose up -d
```
This starts a PostgreSQL container with `pgvector` pre-installed on port 5432.

**Option B: Local Installation**
1. Install PostgreSQL 15+
2. Install `pgvector` extension
3. Create a database (e.g., `rag_db`)

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your credentials:
- **Database Config**: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- **LLM Config**: `LLM_PROVIDER` (openai, gemini), `LLM_API_KEY`, `LLM_MODEL`
- **Embedding Config**: `EMBEDDING_PROVIDER` (openai, gemini), `EMBEDDING_API_KEY`, `EMBEDDING_MODEL`

### 5. Validate Configuration

```bash
uv run python -m src.test_config
```

You should see: `[OK] ALL CONFIGURATION CHECKS PASSED`

### 6. Run Ingestion Pipeline

```bash
# Add your documents to the documents/ folder
uv run python -m src.ingestion.ingest -d ./documents
```

This will:
- Initialize the database schema (tables and indexes)
- Process your documents (PDF, Word, Markdown, Audio, etc.)
- Chunk them intelligently
- Generate embeddings
- Store everything in PostgreSQL (`documents` and `chunks` tables)

### 7. Run the Agent

```bash
uv run python -m src.cli
```

Now you can ask questions and the agent will search your knowledge base!

## Project Structure

```
Postgres-RAG-Agent/
├── src/                           # Source code
│   ├── settings.py               # ✅ Configuration management
│   ├── providers.py              # ✅ LLM/embedding providers (OpenAI/Gemini)
│   ├── dependencies.py           # ✅ PostgreSQL connection & AgentDependencies
│   ├── test_config.py            # ✅ Configuration validation
│   ├── tools.py                  # ✅ Search tools (SQL + pgvector)
│   ├── agent.py                  # ✅ Pydantic AI agent with search tools
│   ├── cli.py                    # ✅ Rich-based conversational CLI
│   ├── prompts.py                # ✅ System prompts
│   ├── database/
│   │   ├── init_db.py            # ✅ Database initialization
│   │   ├── schema.sql            # ✅ Database schema (tables & indexes)
│   │   └── clean_db.py           # ✅ Database cleanup utility
│   └── ingestion/
│       ├── chunker.py            # ✅ Docling HybridChunker wrapper
│       ├── embedder.py           # ✅ Batch embedding generation
│       └── ingest.py             # ✅ PostgreSQL ingestion pipeline
├── documents/                     # Document folder
├── tests/                         # Unit tests
├── test_scripts/                  # E2E test scripts
└── pyproject.toml                # UV package configuration
```

## Technology Stack

- **Database**: PostgreSQL 15+ (Vector Search + Full-Text Search)
- **Extensions**: `pgvector` (vector embeddings), `btree_gin` (indexing)
- **Agent Framework**: Pydantic AI 0.1.0+
- **Document Processing**: Docling 2.14+ (PDF, Word, PowerPoint, Excel, Audio)
- **Async Driver**: asyncpg 0.29+
- **CLI**: Rich 13.9+ (terminal formatting and streaming)
- **Package Manager**: UV 0.5.0+ (fast dependency management)

## Hybrid Search Implementation

This project uses **Reciprocal Rank Fusion (RRF)** to combine vector and text search results, providing robust retrieval performance.

### How It Works

1. **Semantic Search**: Uses `pgvector` to calculate cosine distance (`<=>` operator) between query and chunk embeddings.
2. **Text Search**: Uses PostgreSQL's built-in full-text search (`ts_vector`, `ts_query`, `ts_rank_cd`) to find keyword matches.
3. **RRF Merging**: Combines results using the formula: `RRF_score = Σ(1 / (60 + rank))`
   - Documents appearing in both searches get higher combined scores
   - Automatic deduplication
   - Standard k=60 constant

## User Manual

### Starting the Agent
To start the interactive chat interface:
```bash
uv run python -m src.cli
```
Type your query and press Enter. Type `exit` or `quit` to stop.

### Ingesting Documents
To process new documents:
1. Place files in the `documents/` directory.
2. Run the ingestion command:
```bash
uv run python -m src.ingestion.ingest -d ./documents
```
The ingestion pipeline automatically handles file conversion, chunking, embedding generation, and database insertion.

### Managing the Database
To wipe all data from the database (useful for testing or resetting):
```bash
uv run python -m src.database.clean_db
```
**Warning**: This deletes all documents and chunks.

### Supported File Types
The system supports a wide range of formats via Docling:
- **Documents**: PDF, DOCX, PPTX, XLSX, MD, HTML, TXT
- **Audio**: MP3, WAV, M4A (automatically transcribed using Whisper)
- **Images**: PNG, JPG (OCR automatically applied)

### Configuration Reference
Key `.env` variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_DB` | Database name | `rag_db` |
| `POSTGRES_HOST` | Database host | `localhost` |
| `LLM_PROVIDER` | LLM service provider | `openai` or `gemini` |
| `LLM_API_KEY` | API key for LLM | `sk-...` |
| `EMBEDDING_PROVIDER` | Embedding service provider | `openai` or `gemini` |
| `EMBEDDING_MODEL` | Embedding model name | `text-embedding-3-small` or `models/embedding-001` |
