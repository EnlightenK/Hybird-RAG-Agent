import os
import sys
import pytest
import asyncpg
import json
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
    pipeline._initialized = True # Mark as initialized
    
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
    
    # Save to PostgreSQL
    doc_id = await pipeline._save_to_postgres(title, source, content, chunks, metadata)
    assert doc_id is not None
    
    # Verify in DB
    async with pg_pool.acquire() as conn:
        doc = await conn.fetchrow("SELECT * FROM documents WHERE id = $1", doc_id)
        assert doc is not None
        assert doc['filename'] == source
        
        chunk = await conn.fetchrow("SELECT * FROM chunks WHERE document_id = $1", doc_id)
        assert chunk is not None
        assert chunk['content'] == chunks[0].content
        
        embedding_data = chunk['embedding']
        if isinstance(embedding_data, str):
            embedding_list = json.loads(embedding_data)
        else:
            embedding_list = list(embedding_data)
            
        assert len(embedding_list) == 768
        assert abs(embedding_list[0] - 0.1) < 1e-6

@pytest.mark.asyncio
async def test_clean_databases(pg_pool):
    """Test cleaning PostgreSQL database."""
    config = IngestionConfig()
    pipeline = DocumentIngestionPipeline(config)
    pipeline.pg_pool = pg_pool
    pipeline._initialized = True
    
    # Ensure there is data
    await pipeline._save_to_postgres(
        "To Clean", "clean.md", "Content", 
        [DocumentChunk("Content", 0, 0, 7, {}, 1, [0.0]*768)], {}
    )
    
    # Clean
    await pipeline._clean_databases()
    
    # Verify empty
    async with pg_pool.acquire() as conn:
        count_docs = await conn.fetchval("SELECT COUNT(*) FROM documents")
        count_chunks = await conn.fetchval("SELECT COUNT(*) FROM chunks")
        assert count_docs == 0
        assert count_chunks == 0
