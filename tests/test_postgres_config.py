import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.getcwd())

def test_postgres_env_vars():
    """Test that PostgreSQL configuration variables exist."""
    load_dotenv()
    
    # We expect these to pass now
    assert os.getenv("POSTGRES_DB") is not None, "POSTGRES_DB not set"
    assert os.getenv("POSTGRES_USER") is not None, "POSTGRES_USER not set"
    assert os.getenv("POSTGRES_PASSWORD") is not None, "POSTGRES_PASSWORD not set"
    assert os.getenv("POSTGRES_HOST") is not None, "POSTGRES_HOST not set"
    assert os.getenv("POSTGRES_PORT") is not None, "POSTGRES_PORT not set"
