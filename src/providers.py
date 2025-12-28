"""Model providers for Semantic Search Agent."""

from typing import Optional, Union
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from src.settings import load_settings


def get_llm_model(model_choice: Optional[str] = None) -> Union[OpenAIModel, GoogleModel]:
    """
    Get LLM model configuration based on environment variables.
    Supports OpenAI-compatible API providers and Google Gemini.

    Args:
        model_choice: Optional override for model choice

    Returns:
        Configured LLM model
    """
    settings = load_settings()
    llm_provider = settings.llm_provider.lower()
    llm_choice = model_choice or settings.llm_model

    if llm_provider == "gemini":
        provider = GoogleProvider(api_key=settings.llm_api_key)
        return GoogleModel(llm_choice, provider=provider)
    
    # Default to OpenAI-compatible
    provider = OpenAIProvider(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    return OpenAIModel(llm_choice, provider=provider)


def get_embedding_model() -> Union[OpenAIModel, GoogleModel]:
    """
    Get embedding model configuration.
    Supports OpenAI embeddings API and Google Gemini.

    Returns:
        Configured embedding model
    """
    settings = load_settings()
    embedding_provider = settings.embedding_provider.lower()

    if embedding_provider == "gemini":
        provider = GoogleProvider(api_key=settings.embedding_api_key)
        return GoogleModel(settings.embedding_model, provider=provider)

    # For OpenAI-compatible embeddings
    provider = OpenAIProvider(
        base_url=settings.embedding_base_url, api_key=settings.embedding_api_key
    )

    return OpenAIModel(settings.embedding_model, provider=provider)


def get_model_info() -> dict:
    """
    Get information about current model configuration.

    Returns:
        Dictionary with model configuration info
    """
    settings = load_settings()

    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
        "embedding_provider": settings.embedding_provider,
        "embedding_model": settings.embedding_model,
    }


def validate_llm_configuration() -> bool:
    """
    Validate that LLM configuration is properly set.

    Returns:
        True if configuration is valid
    """
    try:
        # Check if we can create a model instance
        get_llm_model()
        return True
    except Exception as e:
        print(f"LLM configuration validation failed: {e}")
        return False
