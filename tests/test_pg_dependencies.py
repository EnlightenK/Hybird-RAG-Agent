import os
import sys
import pytest
import asyncpg

# Add project root to path
sys.path.append(os.getcwd())

from src.dependencies import AgentDependencies
from src.settings import load_settings

@pytest.mark.asyncio
async def test_pg_connection_initialization():
    """Test that PostgreSQL connection is initialized correctly."""
    deps = AgentDependencies()
    # Ensure settings are loaded
    await deps.initialize()
    
    try:
        # Check if pg_pool is initialized
        assert hasattr(deps, 'pg_pool'), "AgentDependencies should have a pg_pool attribute"
        assert deps.pg_pool is not None, "pg_pool should be initialized"
        
        # Test a simple query through the pool
        async with deps.pg_pool.acquire() as conn:
            val = await conn.fetchval("SELECT 1")
            assert val == 1
    finally:
        await deps.cleanup()
        # Verify cleanup
        assert not hasattr(deps, 'pg_pool') or deps.pg_pool is None, "pg_pool should be cleaned up"