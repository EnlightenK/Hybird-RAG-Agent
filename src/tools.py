"""Search tools for PostgreSQL RAG Agent."""

import asyncio
import logging
import json
from typing import Optional, List, Dict, Any
from pydantic_ai import RunContext
from pydantic import BaseModel, Field

from src.dependencies import AgentDependencies

logger = logging.getLogger(__name__)


class SearchResult(BaseModel):
    """Model for search results."""

    chunk_id: str = Field(..., description="ID of chunk as string")
    document_id: str = Field(..., description="Parent document ID as string")
    content: str = Field(..., description="Chunk text content")
    similarity: float = Field(..., description="Relevance score (0-1)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")
    document_title: str = Field(..., description="Title from document lookup")
    document_source: str = Field(..., description="Source from document lookup")


async def semantic_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    match_count: Optional[int] = None
) -> List[SearchResult]:
    """
    Perform pure semantic search using PostgreSQL pgvector.

    Args:
        ctx: Agent runtime context with dependencies
        query: Search query text
        match_count: Number of results to return (default: 10)

    Returns:
        List of search results ordered by similarity
    """
    try:
        deps = ctx.deps

        # Use default if not specified
        if match_count is None:
            match_count = deps.settings.default_match_count

        # Validate match count
        match_count = min(match_count, deps.settings.max_match_count)

        # Generate embedding for query
        query_embedding = await deps.get_embedding(query)
        embedding_str = str(query_embedding)

        # Execute PostgreSQL query
        sql = """
            SELECT 
                c.id as chunk_id,
                c.document_id,
                c.content,
                1 - (c.embedding <=> $1) as similarity,
                c.metadata as chunk_metadata,
                d.filename as document_source,
                d.metadata->>'title' as document_title
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            ORDER BY c.embedding <=> $1
            LIMIT $2
        """

        if not deps.pg_pool:
            await deps.initialize()

        async with deps.pg_pool.acquire() as conn:
            rows = await conn.fetch(sql, embedding_str, match_count)

        search_results = []
        for row in rows:
            chunk_metadata = row['chunk_metadata']
            if isinstance(chunk_metadata, str):
                chunk_metadata = json.loads(chunk_metadata)
            elif chunk_metadata is None:
                chunk_metadata = {}
            
            title = row['document_title'] or row['document_source']

            search_results.append(SearchResult(
                chunk_id=str(row['chunk_id']),
                document_id=str(row['document_id']),
                content=row['content'],
                similarity=float(row['similarity']),
                metadata=chunk_metadata,
                document_title=title,
                document_source=row['document_source']
            ))

        logger.info(
            f"semantic_search_completed: query={query}, results={len(search_results)}, match_count={match_count}"
        )

        return search_results

    except Exception as e:
        logger.exception(f"semantic_search_error: query={query}, error={str(e)}")
        return []


async def text_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    match_count: Optional[int] = None
) -> List[SearchResult]:
    """
    Perform full-text search using PostgreSQL full-text search.

    Args:
        ctx: Agent runtime context with dependencies
        query: Search query text
        match_count: Number of results to return (default: 10)

    Returns:
        List of search results ordered by text relevance
    """
    try:
        deps = ctx.deps

        # Use default if not specified
        if match_count is None:
            match_count = deps.settings.default_match_count

        # Validate match count
        match_count = min(match_count, deps.settings.max_match_count)

        # Build PostgreSQL full-text search query
        sql = """
            SELECT 
                c.id as chunk_id,
                c.document_id,
                c.content,
                ts_rank_cd(to_tsvector('english', c.content), query) as similarity,
                c.metadata as chunk_metadata,
                d.filename as document_source,
                d.metadata->>'title' as document_title
            FROM chunks c
            JOIN documents d ON c.document_id = d.id,
            websearch_to_tsquery('english', $1) query
            WHERE to_tsvector('english', c.content) @@ query
            ORDER BY similarity DESC
            LIMIT $2
        """

        if not deps.pg_pool:
            await deps.initialize()

        async with deps.pg_pool.acquire() as conn:
            rows = await conn.fetch(sql, query, match_count * 2)

        search_results = []
        for row in rows:
            chunk_metadata = row['chunk_metadata']
            if isinstance(chunk_metadata, str):
                chunk_metadata = json.loads(chunk_metadata)
            elif chunk_metadata is None:
                chunk_metadata = {}
            
            title = row['document_title'] or row['document_source']

            search_results.append(SearchResult(
                chunk_id=str(row['chunk_id']),
                document_id=str(row['document_id']),
                content=row['content'],
                similarity=float(row['similarity']),
                metadata=chunk_metadata,
                document_title=title,
                document_source=row['document_source']
            ))

        logger.info(
            f"text_search_completed: query={query}, results={len(search_results)}, match_count={match_count}"
        )

        return search_results

    except Exception as e:
        logger.exception(f"text_search_error: query={query}, error={str(e)}")
        return []


def reciprocal_rank_fusion(
    search_results_list: List[List[SearchResult]],
    k: int = 60
) -> List[SearchResult]:
    """
    Merge multiple ranked lists using Reciprocal Rank Fusion.
    """
    rrf_scores: Dict[str, float] = {}
    chunk_map: Dict[str, SearchResult] = {}

    for results in search_results_list:
        for rank, result in enumerate(results):
            chunk_id = result.chunk_id
            rrf_score = 1.0 / (k + rank)

            if chunk_id in rrf_scores:
                rrf_scores[chunk_id] += rrf_score
            else:
                rrf_scores[chunk_id] = rrf_score
                chunk_map[chunk_id] = result

    sorted_chunks = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    merged_results = []
    for chunk_id, rrf_score in sorted_chunks:
        result = chunk_map[chunk_id]
        merged_result = SearchResult(
            chunk_id=result.chunk_id,
            document_id=result.document_id,
            content=result.content,
            similarity=rrf_score,
            metadata=result.metadata,
            document_title=result.document_title,
            document_source=result.document_source
        )
        merged_results.append(merged_result)

    return merged_results


async def hybrid_search(
    ctx: RunContext[AgentDependencies],
    query: str,
    match_count: Optional[int] = None,
    text_weight: Optional[float] = None
) -> List[SearchResult]:
    """
    Perform hybrid search combining semantic and keyword matching.
    """
    try:
        deps = ctx.deps

        if match_count is None:
            match_count = deps.settings.default_match_count

        match_count = min(match_count, deps.settings.max_match_count)
        fetch_count = match_count * 2

        semantic_results, text_results = await asyncio.gather(
            semantic_search(ctx, query, fetch_count),
            text_search(ctx, query, fetch_count),
            return_exceptions=True
        )

        if isinstance(semantic_results, Exception):
            semantic_results = []
        if isinstance(text_results, Exception):
            text_results = []

        if not semantic_results and not text_results:
            return []

        merged_results = reciprocal_rank_fusion(
            [semantic_results, text_results],
            k=60
        )

        return merged_results[:match_count]

    except Exception as e:
        logger.exception(f"hybrid_search_error: query={query}, error={str(e)}")
        try:
            return await semantic_search(ctx, query, match_count)
        except:
            return []
