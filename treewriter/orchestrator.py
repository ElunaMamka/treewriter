"""TreeWriter orchestrator - main coordinator for text generation."""

from typing import Optional, List
from .config import ModelConfig, ThresholdConfig
from .tree import WritingTree
from .planning import PlanningAgent
from .thinking import ThinkingModel
from .writing import WritingModel
from .utils import setup_logger, count_words


logger = setup_logger(__name__)


class TreeWriter:
    """Main orchestrator for hierarchical text generation.
    
    TreeWriter coordinates the three-phase generation process:
    1. Planning: Build writing tree structure
    2. Thinking: Generate outlines for leaf nodes
    3. Writing: Generate text content from outlines
    
    Attributes:
        planning_agent: Agent for tree generation
        thinking_model: Model for outline generation
        writing_model: Model for text generation
    """
    
    def __init__(
        self,
        planning_config: ModelConfig,
        thinking_config: ModelConfig,
        writing_config: ModelConfig,
        threshold_config: Optional[ThresholdConfig] = None,
        language: str = "cn"
    ):
        """Initialize TreeWriter with model configurations.
        
        Args:
            planning_config: Configuration for planning agent
            thinking_config: Configuration for thinking model
            writing_config: Configuration for writing model
            threshold_config: Configuration for decomposition thresholds
            language: Language for prompts ("cn" or "en")
        """
        if threshold_config is None:
            threshold_config = ThresholdConfig()
        
        self.planning_agent = PlanningAgent(
            planning_config,
            threshold_config,
            language=language
        )
        
        self.thinking_model = ThinkingModel(
            thinking_config,
            language=language
        )
        
        self.writing_model = WritingModel(
            writing_config,
            language=language
        )
        
        self.language = language
        
        logger.info("TreeWriter initialized successfully")
    
    def generate(
        self,
        task: str,
        word_count: int,
        story_setting: Optional[str] = None,
        character_list: Optional[List[str]] = None,
        writing_tone: Optional[str] = None,
        language_style: Optional[str] = None,
        theme: Optional[str] = None,
        story_structure: Optional[str] = None,
        plot_development: Optional[str] = None,
        worldbuilding: Optional[str] = None,
        writing_goals: Optional[str] = None,
        max_depth: int = 10
    ) -> str:
        """Generate long text for the given task.
        
        Args:
            task: Overall writing task description
            word_count: Target word count
            story_setting: Story setting
            character_list: List of characters
            writing_tone: Writing tone
            language_style: Language style
            theme: Core theme
            story_structure: Story structure
            plot_development: Plot development
            worldbuilding: Worldbuilding details
            writing_goals: Writing goals
            max_depth: Maximum tree depth
            
        Returns:
            Complete generated text
        """
        logger.info(f"Starting generation for task: {task[:50]}...")
        logger.info(f"Target word count: {word_count}")
        
        # Phase 1: Build tree structure
        logger.info("Phase 1: Building writing tree...")
        tree = self.planning_agent.build_tree(
            root_task=task,
            word_count=word_count,
            story_setting=story_setting,
            character_list=character_list,
            writing_tone=writing_tone,
            language_style=language_style,
            theme=theme,
            story_structure=story_structure,
            plot_development=plot_development,
            worldbuilding=worldbuilding,
            writing_goals=writing_goals,
            max_depth=max_depth
        )
        
        leaf_nodes = tree.get_leaf_nodes()
        logger.info(f"Tree built: {len(tree)} nodes, {len(leaf_nodes)} leaves")
        
        # Phase 2: Generate outlines for leaf nodes
        logger.info("Phase 2: Generating outlines...")
        for i, node_name in enumerate(leaf_nodes, 1):
            logger.info(f"Generating outline {i}/{len(leaf_nodes)} for '{node_name}'")
            node = tree.get_node(node_name)
            
            try:
                outline = self.thinking_model.generate_outline(node, tree)
                tree.update_node_metadata(node_name, outline=outline)
                logger.debug(f"Outline generated for '{node_name}'")
            except Exception as e:
                logger.error(f"Failed to generate outline for '{node_name}': {e}")
                # Continue with other nodes
        
        # Phase 3: Generate text for leaf nodes
        logger.info("Phase 3: Generating text...")
        for i, node_name in enumerate(leaf_nodes, 1):
            logger.info(f"Generating text {i}/{len(leaf_nodes)} for '{node_name}'")
            node = tree.get_node(node_name)
            outline = node.get("outline")
            
            if not outline:
                logger.warning(f"No outline for '{node_name}', skipping text generation")
                continue
            
            try:
                text = self.writing_model.generate_text(node, outline, tree)
                tree.update_node_metadata(node_name, generated_text=text)
                logger.debug(f"Text generated for '{node_name}'")
            except Exception as e:
                logger.error(f"Failed to generate text for '{node_name}': {e}")
                # Continue with other nodes
        
        # Phase 4: Concatenate text
        logger.info("Phase 4: Concatenating text...")
        final_text = self._concatenate_text(tree)
        
        final_word_count = count_words(final_text)
        logger.info(f"Generation complete: {final_word_count} words (target: {word_count})")
        
        return final_text
    
    def _concatenate_text(self, tree: WritingTree) -> str:
        """Concatenate text from leaf nodes in DFS order.
        
        Args:
            tree: Writing tree with generated text
            
        Returns:
            Concatenated text
        """
        text_segments = []
        
        # Traverse tree in DFS order
        for node_name in tree.traverse_dfs():
            node = tree.get_node(node_name)
            
            # Only include leaf nodes with generated text
            if node.get("node_type") == "leaf" and node.get("generated_text"):
                text_segments.append(node["generated_text"])
        
        # Join with double newlines
        final_text = "\n\n".join(text_segments)
        
        logger.info(f"Concatenated {len(text_segments)} text segments")
        
        return final_text
