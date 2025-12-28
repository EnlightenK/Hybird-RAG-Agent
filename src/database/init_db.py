import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    print("Initializing database...")
    db_config = {
        "user": os.getenv("POSTGRES_USER", "rag_user"),
        "password": os.getenv("POSTGRES_PASSWORD", "rag_password"),
        "database": os.getenv("POSTGRES_DB", "rag_db"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }
    
    # Read schema
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    try:
        conn = await asyncpg.connect(**db_config)
        await conn.execute(schema_sql)
        print("Schema applied successfully.")
        await conn.close()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db())
