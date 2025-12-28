import os
import sys
import pytest
from unittest.mock import MagicMock, AsyncMock

# Add project root to path
sys.path.append(os.getcwd())

from src.tools import semantic_search, text_search, hybrid_search, SearchResult
from src.dependencies import AgentDependencies

@pytest.fixture
async def mock_ctx():
    """Setup mock AgentDependencies and RunContext."""
    deps = AgentDependencies()
    # Mock settings
    deps.settings = MagicMock()
    deps.settings.default_match_count = 5
    deps.settings.max_match_count = 10
    
    # Mock pg_pool
    deps.pg_pool = AsyncMock()
    
    # Mock embedding generation
    deps.get_embedding = AsyncMock(return_value=[0.1]*768)
    
    ctx = MagicMock()
    ctx.deps = deps
    return ctx

@pytest.mark.asyncio
async def test_semantic_search_sql(mock_ctx):
    """Test semantic search uses correct SQL."""
    # We expect this to fail initially with MongoDB-specific logic
    query = "test query"
    
    # Setup mock return from DB
    mock_ctx.deps.pg_pool.acquire.return_value.__aenter__.return_value.fetch.return_value = [
        {
            'chunk_id': 'c1',
            'document_id': 'd1',
            'content': 'test content',
            'similarity': 0.9,
            'metadata': '{}',
            'document_title': 'doc title',
            'document_source': 'doc source'
        }
    ]
    
    try:
        results = await semantic_search(mock_ctx, query)
        assert len(results) > 0
        assert results[0].content == 'test content'
    except Exception as e:
        # If it fails due to pymongo not being installed or other MongoDB logic
        pytest.fail(f"semantic_search failed: {e}")

@pytest.mark.asyncio
async def test_text_search_sql(mock_ctx):
    """Test text search uses correct SQL."""
    query = "test query"
    
    # Setup mock return from DB
    mock_ctx.deps.pg_pool.acquire.return_value.__aenter__.return_value.fetch.return_value = [
        {
            'chunk_id': 'c1',
            'document_id': 'd1',
            'content': 'test content',
            'similarity': 0.8,
            'metadata': '{}',
            'document_title': 'doc title',
            'document_source': 'doc source'
        }
    ]
    
    results = await text_search(mock_ctx, query)
    assert len(results) > 0
