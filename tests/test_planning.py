"""Tests for PlanningAgent."""

import pytest
from unittest.mock import Mock, patch
from treewriter.planning import PlanningAgent
from treewriter.config import ModelConfig, ThresholdConfig
from treewriter.tree import WritingTree
from treewriter.utils import ConfigurationError, GenerationError


class TestPlanningAgentInit:
    """Tests for PlanningAgent initialization."""
    
    def test_init_with_valid_config(self):
        """Test initializing with valid configuration."""
        model_config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        threshold_config = ThresholdConfig()
        
        agent = PlanningAgent(model_config, threshold_config)
        assert agent.model_config == model_config
        assert agent.threshold_config == threshold_config
    
    def test_init_with_invalid_model_config(self):
        """Test initializing with invalid model config raises error."""
        model_config = ModelConfig(model_type="invalid")
        threshold_config = ThresholdConfig()
        
        with pytest.raises(ConfigurationError):
            PlanningAgent(model_config, threshold_config)
    
    def test_init_with_invalid_threshold_config(self):
        """Test initializing with invalid threshold config raises error."""
        model_config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        threshold_config = ThresholdConfig(min_word_count=-1)
        
        with pytest.raises(ConfigurationError):
            PlanningAgent(model_config, threshold_config)
    
    def test_init_with_local_model_not_implemented(self):
        """Test initializing with local model raises NotImplementedError."""
        model_config = ModelConfig(
            model_type="local",
            model_path="/path/to/model"
        )
        threshold_config = ThresholdConfig()
        
        with pytest.raises(NotImplementedError):
            PlanningAgent(model_config, threshold_config)


class TestThresholdCheck:
    """Tests for threshold-based decomposition check."""
    
    @pytest.fixture
    def agent(self):
        """Create a planning agent for testing."""
        model_config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        threshold_config = ThresholdConfig(
            min_word_count=1000,
            max_word_count=5000
        )
        return PlanningAgent(model_config, threshold_config)
    
    def test_threshold_check_above_max(self, agent):
        """Test threshold check with word count above max."""
        node = {"word_count": 6000}
        assert agent.should_decompose_threshold(node) is True
    
    def test_threshold_check_below_min(self, agent):
        """Test threshold check with word count below min."""
        node = {"word_count": 500}
        assert agent.should_decompose_threshold(node) is False
    
    def test_threshold_check_in_range(self, agent):
        """Test threshold check with word count in range."""
        node = {"word_count": 3000}
        # In range, so should return True (let agent decide)
        assert agent.should_decompose_threshold(node) is True
    
    def test_threshold_check_at_min(self, agent):
        """Test threshold check at minimum boundary."""
        node = {"word_count": 1000}
        assert agent.should_decompose_threshold(node) is True
    
    def test_threshold_check_at_max(self, agent):
        """Test threshold check at maximum boundary."""
        node = {"word_count": 5000}
        assert agent.should_decompose_threshold(node) is True


class TestParseAgentResponse:
    """Tests for parsing agent responses."""
    
    @pytest.fixture
    def agent(self):
        """Create a planning agent for testing."""
        model_config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        threshold_config = ThresholdConfig()
        return PlanningAgent(model_config, threshold_config)
    
    def test_parse_json_with_code_blocks(self, agent):
        """Test parsing JSON wrapped in code blocks."""
        response = '''```json
{
  "should_decompose": true,
  "reasoning": "Task is complex",
  "children": []
}
```'''
        result = agent._parse_agent_response(response)
        assert result["should_decompose"] is True
        assert result["reasoning"] == "Task is complex"
    
    def test_parse_json_without_code_blocks(self, agent):
        """Test parsing JSON without code blocks."""
        response = '{"should_decompose": false, "reasoning": "Task is simple", "children": []}'
        result = agent._parse_agent_response(response)
        assert result["should_decompose"] is False
        assert result["reasoning"] == "Task is simple"
    
    def test_parse_invalid_json(self, agent):
        """Test parsing invalid JSON returns default."""
        response = "This is not JSON at all"
        result = agent._parse_agent_response(response)
        assert result["should_decompose"] is False
        assert "children" in result
    
    def test_parse_json_with_extra_text(self, agent):
        """Test parsing JSON with surrounding text."""
        response = '''Here is my decision:
```json
{
  "should_decompose": true,
  "reasoning": "Needs breakdown"
}
```
That's my analysis.'''
        result = agent._parse_agent_response(response)
        assert result["should_decompose"] is True


class TestBuildTree:
    """Tests for tree building (without actual API calls)."""
    
    @pytest.fixture
    def agent(self):
        """Create a planning agent for testing."""
        model_config = ModelConfig(
            model_type="api",
            api_key="test_key",
            api_endpoint="https://api.example.com",
            model_name="gpt-4"
        )
        # Set high min threshold so nodes won't decompose
        threshold_config = ThresholdConfig(
            min_word_count=10000,
            max_word_count=50000
        )
        return PlanningAgent(model_config, threshold_config)
    
    def test_build_tree_creates_root(self, agent):
        """Test that build_tree creates root node."""
        tree = agent.build_tree(
            root_task="Write a story",
            word_count=500,  # Below threshold, won't decompose
            theme="Adventure"
        )
        
        assert len(tree) == 1
        assert "root" in tree
        
        root = tree.get_node("root")
        assert root["content"] == "Write a story"
        assert root["word_count"] == 500
        assert root["theme"] == "Adventure"
