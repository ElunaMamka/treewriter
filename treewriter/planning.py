"""Planning agent for recursive tree generation."""

import json
import re
from typing import Dict, List, Tuple, Optional
from openai import OpenAI

from .config import ModelConfig, ThresholdConfig
from .tree import WritingTree
from .prompts import get_planning_prompt, format_template
from .utils import setup_logger, GenerationError, ConfigurationError


logger = setup_logger(__name__)


class PlanningAgent:
    """Planning agent that recursively decomposes writing tasks.
    
    The agent uses a dual-check mechanism to determine whether to decompose nodes:
    1. Threshold check: Based on word count
    2. Agent check: LLM-based decision considering content complexity
    
    Attributes:
        model_config: Configuration for the LLM model
        threshold_config: Configuration for threshold-based checks
        prompt_template: Prompt template for the planning agent
        client: OpenAI client (for API models)
    """
    
    def __init__(
        self,
        model_config: ModelConfig,
        threshold_config: ThresholdConfig,
        prompt_template: Optional[str] = None,
        language: str = "cn"
    ):
        """Initialize planning agent.
        
        Args:
            model_config: Model configuration
            threshold_config: Threshold configuration
            prompt_template: Custom prompt template (optional)
            language: Language for prompts ("cn" or "en")
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Validate configurations
        try:
            model_config.validate()
            threshold_config.validate()
        except ValueError as e:
            raise ConfigurationError(f"Invalid configuration: {e}")
        
        self.model_config = model_config
        self.threshold_config = threshold_config
        self.language = language
        
        # Set prompt template
        if prompt_template:
            self.prompt_template = prompt_template
        else:
            self.prompt_template = get_planning_prompt(language)
        
        # Initialize model client
        if model_config.model_type == "api":
            self.client = OpenAI(
                api_key=model_config.api_key,
                base_url=model_config.api_endpoint
            )
        else:
            # For local models, we'll need to implement later
            raise NotImplementedError("Local model support not yet implemented")
        
        logger.info(f"PlanningAgent initialized with {model_config.model_type} model")
    
    def should_decompose_threshold(self, node: Dict) -> bool:
        """Check if node should be decomposed based on threshold.
        
        Args:
            node: Node metadata dictionary
            
        Returns:
            True if node should be decomposed based on threshold
        """
        word_count = node.get("word_count", 0)
        
        # Must decompose if above max threshold
        if word_count > self.threshold_config.max_word_count:
            logger.debug(f"Threshold check: DECOMPOSE (word_count {word_count} > {self.threshold_config.max_word_count})")
            return True
        
        # Don't decompose if below min threshold
        if word_count < self.threshold_config.min_word_count:
            logger.debug(f"Threshold check: NO DECOMPOSE (word_count {word_count} < {self.threshold_config.min_word_count})")
            return False
        
        # In between: let agent decide
        logger.debug(f"Threshold check: AGENT DECIDES (word_count {word_count} in range)")
        return True
    
    def should_decompose_agent(
        self,
        node: Dict,
        tree: WritingTree
    ) -> Tuple[bool, str]:
        """Use LLM to decide if node should be decomposed.
        
        Args:
            node: Node metadata dictionary
            tree: Current writing tree for context
            
        Returns:
            Tuple of (should_decompose: bool, reasoning: str)
            
        Raises:
            GenerationError: If LLM generation fails
        """
        try:
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
                "max_word_count": self.threshold_config.max_word_count,
                "min_children": self.threshold_config.min_children,
                "max_children": self.threshold_config.max_children,
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
            
            response_text = response.choices[0].message.content
            logger.debug(f"Agent response: {response_text[:200]}...")
            
            # Parse JSON response
            decision = self._parse_agent_response(response_text)
            
            should_decompose = decision.get("should_decompose", False)
            reasoning = decision.get("reasoning", "No reasoning provided")
            
            logger.info(f"Agent decision: {'DECOMPOSE' if should_decompose else 'NO DECOMPOSE'}")
            logger.debug(f"Reasoning: {reasoning}")
            
            return should_decompose, reasoning
            
        except Exception as e:
            logger.error(f"Agent check failed: {e}")
            raise GenerationError(
                f"Failed to get agent decision: {e}",
                node_name=node.get("content", "unknown"),
                context={"node": node}
            )
    
    def _parse_agent_response(self, response_text: str) -> Dict:
        """Parse agent response to extract decision.
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            Dictionary with decision and reasoning
        """
        # Try to extract JSON from response
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON without code blocks
            json_match = re.search(r'\{.*"should_decompose".*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                # Fallback: assume no decomposition if can't parse
                logger.warning("Could not parse JSON from response, defaulting to no decomposition")
                return {"should_decompose": False, "reasoning": "Failed to parse response", "children": []}
        
        try:
            decision = json.loads(json_str)
            return decision
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error: {e}, defaulting to no decomposition")
            return {"should_decompose": False, "reasoning": "JSON parse error", "children": []}
    
    def decompose_node(
        self,
        node_name: str,
        tree: WritingTree
    ) -> List[Dict]:
        """Decompose a node into child nodes.
        
        Args:
            node_name: Name of node to decompose
            tree: Writing tree
            
        Returns:
            List of child node specifications
            
        Raises:
            GenerationError: If decomposition fails
        """
        node = tree.get_node(node_name)
        
        try:
            # Get decomposition from agent
            _, reasoning = self.should_decompose_agent(node, tree)
            
            # Prepare prompt for decomposition
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
                "max_word_count": self.threshold_config.max_word_count,
                "min_children": self.threshold_config.min_children,
                "max_children": self.threshold_config.max_children,
            }
            
            prompt = format_template(self.prompt_template, **prompt_vars)
            
            # Call LLM for decomposition
            response = self.client.chat.completions.create(
                model=self.model_config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.model_config.temperature,
                top_p=self.model_config.top_p,
                max_tokens=self.model_config.max_tokens
            )
            
            response_text = response.choices[0].message.content
            decision = self._parse_agent_response(response_text)
            
            children = decision.get("children", [])
            
            # Validate children
            if not children:
                logger.warning("No children generated, marking as leaf")
                return []
            
            if len(children) < self.threshold_config.min_children:
                logger.warning(f"Too few children ({len(children)}), marking as leaf")
                return []
            
            if len(children) > self.threshold_config.max_children:
                logger.warning(f"Too many children ({len(children)}), truncating")
                children = children[:self.threshold_config.max_children]
            
            # Validate word count conservation
            total_child_words = sum(child.get("word_count", 0) for child in children)
            parent_words = node.get("word_count", 0)
            
            if abs(total_child_words - parent_words) > parent_words * 0.1:  # Allow 10% deviation
                logger.warning(
                    f"Word count mismatch: parent={parent_words}, "
                    f"children_sum={total_child_words}, adjusting..."
                )
                # Adjust children word counts proportionally
                if total_child_words > 0:
                    ratio = parent_words / total_child_words
                    for child in children:
                        child["word_count"] = int(child["word_count"] * ratio)
            
            logger.info(f"Decomposed into {len(children)} children")
            return children
            
        except Exception as e:
            logger.error(f"Decomposition failed: {e}")
            raise GenerationError(
                f"Failed to decompose node: {e}",
                node_name=node_name,
                context={"node": node}
            )
    
    def build_tree(
        self,
        root_task: str,
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
    ) -> WritingTree:
        """Build complete writing tree from root task.
        
        Args:
            root_task: Overall writing task description
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
            max_depth: Maximum tree depth to prevent infinite recursion
            
        Returns:
            Complete writing tree
        """
        tree = WritingTree()
        
        # Add root node
        tree.add_root_node(
            content=root_task,
            word_count=word_count,
            story_setting=story_setting,
            character_list=character_list,
            writing_tone=writing_tone,
            language_style=language_style,
            theme=theme,
            story_structure=story_structure,
            plot_development=plot_development,
            worldbuilding=worldbuilding,
            writing_goals=writing_goals
        )
        
        logger.info(f"Building tree for task: {root_task[:50]}...")
        
        # Process nodes recursively
        self._process_node_recursive("root", tree, depth=0, max_depth=max_depth)
        
        logger.info(f"Tree building complete: {len(tree)} nodes, {len(tree.get_leaf_nodes())} leaves")
        
        return tree
    
    def _process_node_recursive(
        self,
        node_name: str,
        tree: WritingTree,
        depth: int,
        max_depth: int
    ) -> None:
        """Recursively process a node and its children.
        
        Args:
            node_name: Name of node to process
            tree: Writing tree
            depth: Current depth in tree
            max_depth: Maximum allowed depth
        """
        if depth >= max_depth:
            logger.warning(f"Max depth {max_depth} reached, marking as leaf")
            tree.mark_as_leaf(node_name)
            return
        
        node = tree.get_node(node_name)
        
        # Step 1: Threshold check
        threshold_passed = self.should_decompose_threshold(node)
        tree.update_node_metadata(node_name, decompose_threshold_passed=threshold_passed)
        
        if not threshold_passed:
            logger.info(f"Node '{node_name}' marked as leaf (threshold check failed)")
            tree.mark_as_leaf(node_name)
            return
        
        # Step 2: Agent check
        try:
            agent_decision, reasoning = self.should_decompose_agent(node, tree)
            tree.update_node_metadata(
                node_name,
                decompose_agent_decision=agent_decision,
                decompose_agent_reasoning=reasoning
            )
        except GenerationError as e:
            logger.error(f"Agent check failed for '{node_name}': {e}")
            tree.mark_as_leaf(node_name)
            return
        
        # Step 3: Decide whether to decompose
        if not agent_decision:
            logger.info(f"Node '{node_name}' marked as leaf (agent decision)")
            tree.mark_as_leaf(node_name)
            return
        
        # Step 4: Decompose node
        try:
            children = self.decompose_node(node_name, tree)
        except GenerationError as e:
            logger.error(f"Decomposition failed for '{node_name}': {e}")
            tree.mark_as_leaf(node_name)
            return
        
        if not children:
            logger.info(f"Node '{node_name}' marked as leaf (no children generated)")
            tree.mark_as_leaf(node_name)
            return
        
        # Step 5: Add children to tree
        for i, child_spec in enumerate(children):
            child_name = f"{node_name}_child{i+1}"
            
            tree.add_node(
                node_name=child_name,
                content=child_spec.get("content", ""),
                word_count=child_spec.get("word_count", 0),
                story_setting=child_spec.get("story_setting", node.get("story_setting")),
                character_list=child_spec.get("character_list", node.get("character_list")),
                writing_tone=child_spec.get("writing_tone", node.get("writing_tone")),
                language_style=child_spec.get("language_style", node.get("language_style")),
                theme=child_spec.get("theme", node.get("theme")),
                story_structure=child_spec.get("story_structure", node.get("story_structure")),
                plot_development=child_spec.get("plot_development", node.get("plot_development")),
                worldbuilding=child_spec.get("worldbuilding", node.get("worldbuilding")),
                writing_goals=child_spec.get("writing_goals", node.get("writing_goals")),
                node_type="internal"
            )
            
            tree.add_edge(node_name, child_name)
            logger.debug(f"Added child '{child_name}' to '{node_name}'")
        
        # Step 6: Recursively process children
        for i in range(len(children)):
            child_name = f"{node_name}_child{i+1}"
            self._process_node_recursive(child_name, tree, depth + 1, max_depth)
