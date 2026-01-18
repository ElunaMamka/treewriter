"""Thinking model for generating writing outlines."""

from typing import Dict, Optional
from openai import OpenAI

from .config import ModelConfig
from .tree import WritingTree
from .prompts import get_thinking_prompt, format_template
from .utils import setup_logger, GenerationError, ConfigurationError


logger = setup_logger(__name__)


class ThinkingModel:
    """Thinking model that generates writing outlines for leaf nodes.
    
    The thinking model analyzes leaf node requirements and generates
    structured outlines to guide the writing process.
    
    Attributes:
        model_config: Configuration for the LLM model
        prompt_template: Prompt template for outline generation
        client: OpenAI client (for API models)
    """
    
    def __init__(
        self,
        model_config: ModelConfig,
        prompt_template: Optional[str] = None,
        language: str = "cn"
    ):
        """Initialize thinking model.
        
        Args:
            model_config: Model configuration
            prompt_template: Custom prompt template (optional)
            language: Language for prompts ("cn" or "en")
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        try:
            model_config.validate()
        except ValueError as e:
            raise ConfigurationError(f"Invalid configuration: {e}")
        
        self.model_config = model_config
        self.language = language
        
        if prompt_template:
            self.prompt_template = prompt_template
        else:
            self.prompt_template = get_thinking_prompt(language)
        
        if model_config.model_type == "api":
            self.client = OpenAI(
                api_key=model_config.api_key,
                base_url=model_config.api_endpoint
            )
        else:
            raise NotImplementedError("Local model support not yet implemented")
        
        logger.info(f"ThinkingModel initialized with {model_config.model_type} model")
    
    def generate_outline(
        self,
        node: Dict,
        tree: WritingTree
    ) -> str:
        """Generate writing outline for a leaf node.
        
        Args:
            node: Leaf node metadata
            tree: Complete writing tree for context
            
        Returns:
            Structured outline as string
            
        Raises:
            GenerationError: If outline generation fails
        """
        try:
            # Get context from tree
            root_node = tree.get_node("root")
            root_content = root_node.get("content", "")
            
            # Get parent content if exists
            parent_content = ""
            # Simple approach: just use root for now
            parent_content = root_content
            
            # Prepare prompt variables
            prompt_vars = {
                "content": node.get("content", ""),
                "word_count": node.get("word_count", 0),
                "story_setting": node.get("story_setting", "未指定"),
                "character_list": str(node.get("character_list", [])),
                "writing_tone": node.get("writing_tone", "未指定"),
                "language_style": node.get("language_style", "未指定"),
                "theme": node.get("theme", "未指定"),
                "story_structure": node.get("story_structure", "未指定"),
                "plot_development": node.get("plot_development", "未指定"),
                "worldbuilding": node.get("worldbuilding", "未指定"),
                "writing_goals": node.get("writing_goals", "未指定"),
                "root_content": root_content,
                "parent_content": parent_content,
            }
            
            # Format prompt
            prompt = format_template(self.prompt_template, **prompt_vars)
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model_config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.model_config.temperature,
                top_p=self.model_config.top_p,
                max_tokens=self.model_config.max_tokens
            )
            
            outline = response.choices[0].message.content
            logger.info(f"Generated outline ({len(outline)} chars)")
            logger.debug(f"Outline preview: {outline[:200]}...")
            
            return outline
            
        except Exception as e:
            logger.error(f"Outline generation failed: {e}")
            raise GenerationError(
                f"Failed to generate outline: {e}",
                node_name=node.get("content", "unknown"),
                context={"node": node}
            )
