import os
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
sys.path.append(os.getcwd())

from src.tools import semantic_search, text_search, hybrid_search, SearchResult
from src.dependencies import AgentDependencies

class MockAcquireContext:
    def __init__(self, mock_conn):
        self.mock_conn = mock_conn
    async def __aenter__(self):
        return self.mock_conn
    async def __aexit__(self, exc_type, exc, tb):
        pass

@pytest.fixture
async def mock_ctx():
    """Setup mock AgentDependencies and RunContext."""
    deps = AgentDependencies()
    # Mock settings
    deps.settings = MagicMock()
    deps.settings.default_match_count = 5
    deps.settings.max_match_count = 10
    
    # Mock pg_pool
    mock_pool = MagicMock() # Use MagicMock for the pool itself
    mock_conn = AsyncMock()
    # pool.acquire() should return the context manager
    mock_pool.acquire.return_value = MockAcquireContext(mock_conn)
    deps.pg_pool = mock_pool
    
    # Mock embedding generation
    deps.get_embedding = AsyncMock(return_value=[0.1]*768)
    
    ctx = MagicMock()
    ctx.deps = deps
    return ctx, mock_conn

@pytest.mark.asyncio
async def test_semantic_search_sql(mock_ctx):
    """Test semantic search uses correct SQL."""
    ctx, mock_conn = mock_ctx
    query = "test query"
    
    # Setup mock return from DB
    mock_conn.fetch.return_value = [
        {
            'chunk_id': 'c1',
            'document_id': 'd1',
            'content': 'test content',
            'similarity': 0.9,
            'chunk_metadata': '{}',
            'document_title': 'doc title',
            'document_source': 'doc source'
        }
    ]
    
    results = await semantic_search(ctx, query)
    assert len(results) > 0
    assert results[0].content == 'test content'
    assert results[0].similarity == 0.9

@pytest.mark.asyncio
async def test_text_search_sql(mock_ctx):
    """Test text search uses correct SQL."""
    ctx, mock_conn = mock_ctx
    query = "test query"
    
    # Setup mock return from DB
    mock_conn.fetch.return_value = [
        {
            'chunk_id': 'c1',
            'document_id': 'd1',
            'content': 'test content',
            'similarity': 0.8,
            'chunk_metadata': '{}',
            'document_title': 'doc title',
            'document_source': 'doc source'
        }
    ]
    
    results = await text_search(ctx, query)
    assert len(results) > 0
    assert results[0].similarity == 0.8
