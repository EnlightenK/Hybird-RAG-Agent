# MongoDB RAG Agent

## Project Overview

An agentic RAG (Retrieval-Augmented Generation) system combining MongoDB Atlas Vector Search with Pydantic AI for intelligent document retrieval. It features hybrid search capabilities (combining semantic vector search and full-text keyword search via Reciprocal Rank Fusion), multi-format document ingestion (PDF, Word, Audio, etc.) using Docling, and a rich conversational CLI.

**Key Technologies:**
- **Language:** Python 3.10+
- **Database:** MongoDB Atlas (Vector Search + Full-Text Search)
- **Framework:** Pydantic AI
- **Ingestion:** Docling (Document processing & chunking)
- **Package Manager:** uv
- **CLI:** Rich

## Building and Running

### Prerequisites
- **MongoDB Atlas Account:** Free M0 tier is sufficient.
- **LLM API Key:** OpenAI, OpenRouter, or compatible provider.
- **Package Manager:** [uv](https://github.com/astral-sh/uv) must be installed.

### Setup
1.  **Initialize Environment:**
    ```bash
    uv venv
    # Activate: .venv\Scripts\activate (Windows) or source .venv/bin/activate (Unix)
    uv sync
    ```

2.  **Configuration:**
    - Copy `.env.example` to `.env`.
    - Configure `MONGODB_URI` (from Atlas), `LLM_API_KEY`, and other settings.
    - Validate configuration:
      ```bash
      uv run python -m src.test_config
      ```

### Ingestion
Process and ingest documents from the `documents/` directory into MongoDB:
```bash
uv run python -m src.ingestion.ingest -d ./documents
```
*Note: After initial data population, ensure you create the required Vector and Atlas Search indexes in the MongoDB Atlas UI as described in `README.md`.*

### Running the Agent
Launch the interactive conversational agent:
```bash
uv run python -m src.cli
```

### Testing
Execute the test suite:
```bash
uv run pytest
```
Run the comprehensive end-to-end validation:
```bash
uv run python comprehensive_e2e_test.py
```

## Development Conventions

- **Architecture:**
    - `src/`: Contains the active MongoDB implementation. **Work here.**
    - `examples/`: Contains the reference PostgreSQL implementation. **Do not modify.** Use it as a pattern reference only.
    - `documents/`: Directory for placing user documents to be ingested.
- **Coding Standards:**
    - **Type Safety:** Mandatory type annotations for all functions and variables.
    - **Data Models:** Use Pydantic models for all data structures.
    - **Async:** Use `motor` for all MongoDB operations; ensure proper `async/await` usage.
    - **Documentation:** Use Google-style docstrings.
- **Key Patterns:**
    - **Hybrid Search:** Implemented via manual Reciprocal Rank Fusion (RRF) to support MongoDB Atlas M0 tier.
    - **Data Storage:** Uses a "Two-Collection Pattern": `documents` (metadata) and `chunks` (vectors + content).

## Key Files
- `src/agent.py`: Defines the Pydantic AI agent, tools, and system prompts.
- `src/cli.py`: Implements the Rich-based terminal interface and streaming logic.
- `src/tools.py`: Contains MongoDB search logic (Vector Search, Hybrid Search).
- `src/ingestion/ingest.py`: Main script for the document ingestion pipeline.
- `src/settings.py`: Configuration management using Pydantic Settings.
- `CLAUDE.md`: Detailed developer guide, including specific command references and architectural decisions.
