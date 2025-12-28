"""Dependencies for PostgreSQL RAG Agent."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import logging
import asyncpg
import openai
import google.generativeai as genai
from src.settings import load_settings

logger = logging.getLogger(__name__)


@dataclass
class AgentDependencies:
    """Dependencies injected into the agent context."""

    # Core dependencies
    pg_pool: Optional[asyncpg.Pool] = None
    openai_client: Optional[openai.AsyncOpenAI] = None
    settings: Optional[Any] = None

    # Session context
    session_id: Optional[str] = None
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    query_history: list = field(default_factory=list)

    async def initialize(self) -> None:
        """
        Initialize external connections.

        Raises:
            Exception: If PostgreSQL connection fails
            ValueError: If settings cannot be loaded
        """
        if not self.settings:
            self.settings = load_settings()
            logger.info(f"Settings loaded for database: {self.settings.postgres_db}")

        # Initialize PostgreSQL pool
        if not self.pg_pool:
            try:
                self.pg_pool = await asyncpg.create_pool(
                    user=self.settings.postgres_user,
                    password=self.settings.postgres_password,
                    database=self.settings.postgres_db,
                    host=self.settings.postgres_host,
                    port=self.settings.postgres_port,
                    min_size=1,
                    max_size=10
                )
                logger.info(
                    f"PostgreSQL pool initialized for {self.settings.postgres_db} at {self.settings.postgres_host}"
                )
            except Exception as e:
                logger.exception(f"PostgreSQL connection failed: {e}")
                raise

        # Initialize Embedding Provider
        if self.settings.embedding_provider.lower() == "gemini":
            genai.configure(api_key=self.settings.embedding_api_key)
            logger.info(f"Gemini embedding initialized with model: {self.settings.embedding_model}")
        elif not self.openai_client:
            # Initialize OpenAI client for embeddings
            self.openai_client = openai.AsyncOpenAI(
                api_key=self.settings.embedding_api_key,
                base_url=self.settings.embedding_base_url,
            )
            logger.info(
                f"OpenAI client initialized with model: {self.settings.embedding_model}"
            )

    async def cleanup(self) -> None:
        """Clean up external connections."""
        if self.pg_pool:
            await self.pg_pool.close()
            self.pg_pool = None
            logger.info("PostgreSQL connection closed")

    async def get_embedding(self, text: str) -> list[float]:
        """
        Generate embedding for text using the configured provider (OpenAI or Gemini).

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats

        Raises:
            Exception: If embedding generation fails
        """
        if not self.settings:
            await self.initialize()

        if self.settings.embedding_provider.lower() == "gemini":
             result = genai.embed_content(
                model=self.settings.embedding_model,
                content=text,
                task_type="retrieval_query"
            )
             return result['embedding']
        else:
            if not self.openai_client:
                await self.initialize()

            response = await self.openai_client.embeddings.create(
                model=self.settings.embedding_model, input=text
            )
            return response.data[0].embedding

    def set_user_preference(self, key: str, value: Any) -> None:
        """
        Set a user preference for the session.

        Args:
            key: Preference key
            value: Preference value
        """
        self.user_preferences[key] = value

    def add_to_history(self, query: str) -> None:
        """
        Add a query to the search history.

        Args:
            query: Search query to add to history
        """
        self.query_history.append(query)
        # Keep only last 10 queries
        if len(self.query_history) > 10:
            self.query_history.pop(0)