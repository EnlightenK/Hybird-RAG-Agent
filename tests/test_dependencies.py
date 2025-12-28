import pytest
import importlib.util

def test_asyncpg_installed():
    """Verify asyncpg is installed."""
    assert importlib.util.find_spec("asyncpg") is not None, "asyncpg not installed"

def test_pymongo_removed():
    """Verify pymongo is removed."""
    # This test is expected to fail initially (pymongo IS installed)
    # And we want it to PASS eventually (pymongo IS NOT installed)
    assert importlib.util.find_spec("pymongo") is None, "pymongo is still installed"
