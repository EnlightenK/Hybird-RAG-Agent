import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.getcwd())

from src.providers import get_embedding_model
from src.settings import load_settings
# We expect GeminiModel to be available in pydantic-ai
from pydantic_ai.models.gemini import GeminiModel

def test_gemini_provider_returns_gemini_model():
    """Verify get_embedding_model returns GeminiModel when configured."""
    with patch('src.settings.load_settings') as mock_settings:
        mock_settings.return_value.embedding_provider = 'gemini'
        mock_settings.return_value.embedding_model = 'models/embedding-001'
        mock_settings.return_value.embedding_api_key = 'test-key'
        
        model = get_embedding_model()
        assert isinstance(model, GeminiModel)
        assert model.model_name == 'models/embedding-001'