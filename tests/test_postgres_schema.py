import pytest
import asyncpg
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER", "rag_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "rag_password"),
    "database": os.getenv("POSTGRES_DB", "rag_db"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

@pytest.mark.asyncio
async def test_tables_exist():
    """Verify documents and chunks tables exist."""
    # Ensure pgvector extension is enabled (optional check, but good)
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        # Check for documents table
        doc_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = 'public'
                AND    table_name   = 'documents'
            );
        """)
        assert doc_exists, "documents table does not exist"

        # Check for chunks table
        chunk_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = 'public'
                AND    table_name   = 'chunks'
            );
        """)
        assert chunk_exists, "chunks table does not exist"
    finally:
        await conn.close()
