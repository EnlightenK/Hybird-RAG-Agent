import asyncio
import asyncpg
import logging
from src.settings import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def clean_db():
    settings = load_settings()
    
    logger.info(f"Connecting to database {settings.postgres_db} at {settings.postgres_host}...")
    
    try:
        conn = await asyncpg.connect(
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db,
            host=settings.postgres_host,
            port=settings.postgres_port,
        )
        
        # Truncate tables
        # CASCADE ensures chunks are deleted when documents are deleted, but TRUNCATE ... CASCADE is explicit
        logger.info("Cleaning up 'documents' and 'chunks' tables...")
        await conn.execute("TRUNCATE TABLE documents CASCADE;")
        
        logger.info("Database cleaned successfully.")
        await conn.close()
        
    except Exception as e:
        logger.error(f"Failed to clean database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(clean_db())
