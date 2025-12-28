import os
import sys
import pytest
import asyncpg
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
sys.path.append(os.getcwd())

from src.ingestion.ingest import DocumentIngestionPipeline, IngestionConfig, DocumentChunk

@pytest.fixture(scope="function")
async def pg_pool():
    """Setup a test database pool."""
    from dotenv import load_dotenv
    load_dotenv()
    
    pool = await asyncpg.create_pool(
        user=os.getenv("POSTGRES_USER", "rag_user"),
        password=os.getenv("POSTGRES_PASSWORD", "rag_password"),
        database=os.getenv("POSTGRES_DB", "rag_db"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    yield pool
    await pool.close()

@pytest.mark.asyncio
async def test_save_to_postgres(pg_pool):
    """Test saving document and chunks to PostgreSQL."""
    config = IngestionConfig()
    pipeline = DocumentIngestionPipeline(config)
    # Inject pg_pool
    pipeline.pg_pool = pg_pool
    
    title = "Test Document"
    source = "test.md"
    content = "This is a test document."
    chunks = [
        DocumentChunk(
            content="This is a test document.",
            index=0,
            start_char=0,
            end_char=len("This is a test document."),
            metadata={"test": True},
            token_count=5,
            embedding=[0.1] * 768 # Gemini dimension
        )
    ]
    metadata = {"author": "Tester"}
    
    # We expect this to fail with NotImplementedError
    with pytest.raises(NotImplementedError):
        await pipeline._save_to_postgres(title, source, content, chunks, metadata)