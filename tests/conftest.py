"""Pytest configuration and fixtures."""

import pytest
from treewriter.config import ModelConfig, ThresholdConfig, NodeMetadata


@pytest.fixture
def sample_model_config():
    """Sample model configuration for testing."""
    return ModelConfig(
        model_type="api",
        api_key="test_key",
        api_endpoint="https://api.example.com",
        model_name="test-model",
        temperature=0.7,
        top_p=0.9,
        max_tokens=2048
    )


@pytest.fixture
def sample_threshold_config():
    """Sample threshold configuration for testing."""
    return ThresholdConfig(
        min_word_count=1000,
        max_word_count=5000,
        min_children=2,
        max_children=5
    )


@pytest.fixture
def sample_node_metadata():
    """Sample node metadata for testing."""
    return NodeMetadata(
        content="Write a story about a hero's journey",
        word_count=3000,
        node_type="root",
        story_setting="Medieval fantasy world",
        character_list=["Hero", "Mentor", "Villain"],
        writing_tone="Epic and adventurous",
        language_style="Descriptive and vivid",
        theme="Courage and self-discovery"
    )
