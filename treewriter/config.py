"""Configuration dataclasses for TreeWriter."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class ModelConfig:
    """Configuration for a model (planning/thinking/writing).
    
    Attributes:
        model_type: Type of model - "api" or "local"
        api_key: API key for API-based models
        api_endpoint: API endpoint URL for API-based models
        model_name: Model name/identifier for API-based models
        model_path: Path to local model files
        device: Device for local models (e.g., "cuda", "cpu")
        temperature: Sampling temperature for generation
        top_p: Top-p (nucleus) sampling parameter
        max_tokens: Maximum tokens to generate
    """
    
    model_type: str  # "api" or "local"
    
    # For API models
    api_key: Optional[str] = None
    api_endpoint: Optional[str] = None
    model_name: Optional[str] = None
    
    # For local models
    model_path: Optional[str] = None
    device: Optional[str] = "cuda"
    
    # Generation parameters
    temperature: float = 0.8
    top_p: float = 0.95
    max_tokens: int = 4096
    
    def validate(self) -> None:
        """Validate configuration parameters.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if self.model_type not in ["api", "local"]:
            raise ValueError(f"model_type must be 'api' or 'local', got '{self.model_type}'")
        
        if self.model_type == "api":
            if not self.api_key:
                raise ValueError("api_key is required for API models")
            if not self.api_endpoint:
                raise ValueError("api_endpoint is required for API models")
            if not self.model_name:
                raise ValueError("model_name is required for API models")
        
        if self.model_type == "local":
            if not self.model_path:
                raise ValueError("model_path is required for local models")
        
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError(f"temperature must be between 0 and 2, got {self.temperature}")
        
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError(f"top_p must be between 0 and 1, got {self.top_p}")
        
        if self.max_tokens <= 0:
            raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")


@dataclass
class ThresholdConfig:
    """Configuration for threshold-based decomposition check.
    
    Attributes:
        min_word_count: Don't decompose nodes below this word count
        max_word_count: Must decompose nodes above this word count
        min_children: Minimum number of children when decomposing
        max_children: Maximum number of children when decomposing
    """
    
    min_word_count: int = 1000
    max_word_count: int = 5000
    min_children: int = 2
    max_children: int = 5
    
    def validate(self) -> None:
        """Validate threshold configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if self.min_word_count <= 0:
            raise ValueError(f"min_word_count must be positive, got {self.min_word_count}")
        
        if self.max_word_count <= self.min_word_count:
            raise ValueError(
                f"max_word_count ({self.max_word_count}) must be greater than "
                f"min_word_count ({self.min_word_count})"
            )
        
        if self.min_children < 2:
            raise ValueError(f"min_children must be at least 2, got {self.min_children}")
        
        if self.max_children < self.min_children:
            raise ValueError(
                f"max_children ({self.max_children}) must be >= "
                f"min_children ({self.min_children})"
            )


@dataclass
class NodeMetadata:
    """Metadata for a tree node.
    
    Attributes:
        content: Node description/requirement
        word_count: Target word count for this node
        node_type: Type of node - "root", "internal", or "leaf"
        story_setting: Story setting and background
        character_list: List of main characters with descriptions
        writing_tone: Writing tone/mood
        language_style: Language style
        theme: Core theme
        story_structure: Story structure
        plot_development: Plot development
        worldbuilding: World-building details
        writing_goals: Specific writing goals
        outline: Writing outline (from thinking model)
        generated_text: Generated text content (from writing model)
        decompose_threshold_passed: Whether threshold check passed
        decompose_agent_decision: Agent's decomposition decision
        decompose_agent_reasoning: Agent's reasoning for decision
    """
    
    # Core attributes
    content: str
    word_count: int
    node_type: str = "internal"  # "root", "internal", or "leaf"
    
    # Writing parameters
    story_setting: Optional[str] = None
    character_list: Optional[List[str]] = None
    writing_tone: Optional[str] = None
    language_style: Optional[str] = None
    theme: Optional[str] = None
    story_structure: Optional[str] = None
    plot_development: Optional[str] = None
    worldbuilding: Optional[str] = None
    writing_goals: Optional[str] = None
    
    # Generation results
    outline: Optional[str] = None
    generated_text: Optional[str] = None
    
    # Decomposition metadata
    decompose_threshold_passed: Optional[bool] = None
    decompose_agent_decision: Optional[bool] = None
    decompose_agent_reasoning: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary.
        
        Returns:
            Dictionary representation of metadata
        """
        return {
            "content": self.content,
            "word_count": self.word_count,
            "node_type": self.node_type,
            "story_setting": self.story_setting,
            "character_list": self.character_list,
            "writing_tone": self.writing_tone,
            "language_style": self.language_style,
            "theme": self.theme,
            "story_structure": self.story_structure,
            "plot_development": self.plot_development,
            "worldbuilding": self.worldbuilding,
            "writing_goals": self.writing_goals,
            "outline": self.outline,
            "generated_text": self.generated_text,
            "decompose_threshold_passed": self.decompose_threshold_passed,
            "decompose_agent_decision": self.decompose_agent_decision,
            "decompose_agent_reasoning": self.decompose_agent_reasoning,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NodeMetadata":
        """Create NodeMetadata from dictionary.
        
        Args:
            data: Dictionary containing metadata
            
        Returns:
            NodeMetadata instance
        """
        return cls(**data)
