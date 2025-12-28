import asyncio
import logging
from src.dependencies import AgentDependencies
from src.tools import semantic_search, text_search, hybrid_search
from pydantic_ai import RunContext

# Configure logging
logging.basicConfig(level=logging.INFO)

class MockContext:
    def __init__(self, deps):
        self.deps = deps

async def verify_search_tools():
    print("Initializing dependencies...")
    deps = AgentDependencies()
    await deps.initialize()
    ctx = MockContext(deps)
    
    query = "revenue breakdown 2024 financial results"
    
    print("\n--- Testing Semantic Search ---")
    results = await semantic_search(ctx, query, match_count=3)
    for r in results:
        print(f"- [{r.similarity:.4f}] {r.document_title}: {r.content[:100]}...")

    print("\n--- Testing Text Search ---")
    results = await text_search(ctx, query, match_count=3)
    for r in results:
        print(f"- [{r.similarity:.4f}] {r.document_title}: {r.content[:100]}...")

    print("\n--- Testing Hybrid Search ---")
    results = await hybrid_search(ctx, query, match_count=3)
    for r in results:
        print(f"- [{r.similarity:.4f}] {r.document_title}: {r.content[:100]}...")

    await deps.cleanup()

if __name__ == "__main__":
    asyncio.run(verify_search_tools())
