import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def verify():
    db_config = {
        "user": os.getenv("POSTGRES_USER", "rag_user"),
        "password": os.getenv("POSTGRES_PASSWORD", "rag_password"),
        "database": os.getenv("POSTGRES_DB", "rag_db"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }
    
    try:
        conn = await asyncpg.connect(**db_config)
        rows = await conn.fetch("""
            SELECT filename, COUNT(*) as chunk_count 
            FROM chunks 
            JOIN documents ON chunks.document_id = documents.id 
            GROUP BY filename
            ORDER BY filename;
        """)
        
        print("\n" + "="*50)
        print(f"{ 'Filename':<40} | { 'Chunks':<5}")
        print("-" * 50)
        for row in rows:
            print(f"{row['filename']:<40} | {row['chunk_count']:<5}")
        print("="*50 + "\n")
        
        await conn.close()
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify())

