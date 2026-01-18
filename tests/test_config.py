"""Tests for configuration dataclasses."""

import pytest
from treewriter.config import ModelConfig, ThresholdConfig, NodeMetadata


class TestModelConfig:
    """Tests for ModelConfig."""
    
    def test_api_model_config_valid(self):
        """Test valid API model configuration."""
        config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        config.validate()  # Should not raise
    
    def test_local_model_config_valid(self):
        """Test valid local model configuration."""
        config = ModelConfig(
            model_type="local",
            model_path="/path/to/model",
            device="cuda"
        )
        config.validate()  # Should not raise
    
    def test_invalid_model_type(self):
        """Test invalid model type."""
        config = ModelConfig(model_type="invalid")
        with pytest.raises(ValueError, match="model_type must be"):
            config.validate()
    
    def test_api_model_missing_key(self):
        """Test API model with missing API key."""
        config = ModelConfig(
            model_type="api",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        with pytest.raises(ValueError, match="api_key is required"):
            config.validate()
    
    def test_api_model_missing_endpoint(self):
        """Test API model with missing endpoint."""
        config = ModelConfig(
            model_type="api",
            api_key="test_key",
            model_name="gpt-4"
        )
        with pytest.raises(ValueError, match="api_endpoint is required"):
            config.validate()
    
    def test_local_model_missing_path(self):
        """Test local model with missing path."""
        config = ModelConfig(model_type="local")
        with pytest.raises(ValueError, match="model_path is required"):
            config.validate()
    
    def test_invalid_temperature(self):
        """Test invalid temperature values."""
        config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4",
            temperature=3.0
        )
        with pytest.raises(ValueError, match="temperature must be between"):
            config.validate()
    
    def test_invalid_top_p(self):
        """Test invalid top_p values."""
        config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4",
            top_p=1.5
        )
        with pytest.raises(ValueError, match="top_p must be between"):
            config.validate()


class TestThresholdConfig:
    """Tests for ThresholdConfig."""
    
    def test_valid_threshold_config(self):
        """Test valid threshold configuration."""
        config = ThresholdConfig(
            min_word_count=1000,
            max_word_count=5000,
            min_children=2,
            max_children=5
        )
        config.validate()  # Should not raise
    
    def test_invalid_min_word_count(self):
        """Test invalid min_word_count."""
        config = ThresholdConfig(min_word_count=0)
        with pytest.raises(ValueError, match="min_word_count must be positive"):
            config.validate()
    
    def test_max_less_than_min_word_count(self):
        """Test max_word_count less than min_word_count."""
        config = ThresholdConfig(min_word_count=5000, max_word_count=1000)
        with pytest.raises(ValueError, match="max_word_count.*must be greater than"):
            config.validate()
    
    def test_invalid_min_children(self):
        """Test invalid min_children."""
        config = ThresholdConfig(min_children=1)
        with pytest.raises(ValueError, match="min_children must be at least 2"):
            config.validate()
    
    def test_max_less_than_min_children(self):
        """Test max_children less than min_children."""
        config = ThresholdConfig(min_children=5, max_children=2)
        with pytest.raises(ValueError, match="max_children.*must be >="):
            config.validate()


class TestNodeMetadata:
    """Tests for NodeMetadata."""
    
    def test_create_node_metadata(self):
        """Test creating node metadata."""
        metadata = NodeMetadata(
            content="Test content",
            word_count=1000,
            node_type="leaf"
        )
        assert metadata.content == "Test content"
        assert metadata.word_count == 1000
        assert metadata.node_type == "leaf"
    
    def test_to_dict(self):
        """Test converting metadata to dictionary."""
        metadata = NodeMetadata(
            content="Test content",
            word_count=1000,
            story_setting="Fantasy world"
        )
        data = metadata.to_dict()
        assert data["content"] == "Test content"
        assert data["word_count"] == 1000
        assert data["story_setting"] == "Fantasy world"
    
    def test_from_dict(self):
        """Test creating metadata from dictionary."""
        data = {
            "content": "Test content",
            "word_count": 1000,
            "node_type": "root",
            "theme": "Adventure"
        }
        metadata = NodeMetadata.from_dict(data)
        assert metadata.content == "Test content"
        assert metadata.word_count == 1000
        assert metadata.node_type == "root"
        assert metadata.theme == "Adventure"
    
    def test_round_trip_conversion(self):
        """Test converting to dict and back."""
        original = NodeMetadata(
            content="Test content",
            word_count=2000,
            story_setting="Sci-fi universe",
            character_list=["Alice", "Bob"],
            writing_tone="Suspenseful"
        )
        data = original.to_dict()
        restored = NodeMetadata.from_dict(data)
        
        assert restored.content == original.content
        assert restored.word_count == original.word_count
        assert restored.story_setting == original.story_setting
        assert restored.character_list == original.character_list
        assert restored.writing_tone == original.writing_tone
