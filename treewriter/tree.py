"""Writing tree data structure for hierarchical text generation."""

from collections import defaultdict
from typing import Dict, List, Iterator, Optional
from .config import NodeMetadata
from .utils import TreeStructureError


class WritingTree:
    """Tree structure for managing hierarchical writing tasks.
    
    The tree stores nodes with metadata and maintains parent-child relationships
    through an adjacency list. Each node represents a writing subtask with
    associated metadata like word count, story setting, characters, etc.
    
    Attributes:
        nodes: Dictionary mapping node names to their metadata
        adjacency_list: Dictionary mapping parent nodes to lists of child node names
    """
    
    def __init__(self):
        """Initialize an empty writing tree."""
        self.nodes: Dict[str, NodeMetadata] = {}
        self.adjacency_list: Dict[str, List[str]] = defaultdict(list)
    
    def add_root_node(
        self,
        content: str,
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
        node_name: str = "root"
    ) -> None:
        """Add the root node representing the overall writing task.
        
        Args:
            content: Overall writing task description
            word_count: Target word count for entire task
            story_setting: Story setting and background
            character_list: List of main characters
            writing_tone: Writing tone/mood
            language_style: Language style
            theme: Core theme
            story_structure: Story structure
            plot_development: Plot development
            worldbuilding: World-building details
            writing_goals: Specific writing goals
            node_name: Name for root node (default: "root")
            
        Raises:
            TreeStructureError: If root node already exists
        """
        if node_name in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' already exists")
        
        metadata = NodeMetadata(
            content=content,
            word_count=word_count,
            node_type="root",
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
        
        self.nodes[node_name] = metadata
        self.adjacency_list[node_name] = []
    
    def add_node(
        self,
        node_name: str,
        content: str,
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
        node_type: str = "internal"
    ) -> None:
        """Add a child node to the tree.
        
        Args:
            node_name: Unique name for the node
            content: Node description/requirement
            word_count: Target word count for this node
            story_setting: Story setting and background
            character_list: List of main characters
            writing_tone: Writing tone/mood
            language_style: Language style
            theme: Core theme
            story_structure: Story structure
            plot_development: Plot development
            worldbuilding: World-building details
            writing_goals: Specific writing goals
            node_type: Type of node ("internal" or "leaf")
            
        Raises:
            TreeStructureError: If node name already exists
        """
        if node_name in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' already exists")
        
        metadata = NodeMetadata(
            content=content,
            word_count=word_count,
            node_type=node_type,
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
        
        self.nodes[node_name] = metadata
        self.adjacency_list[node_name] = []
    
    def add_edge(self, parent: str, child: str) -> None:
        """Add a parent-child relationship.
        
        Args:
            parent: Parent node name
            child: Child node name
            
        Raises:
            TreeStructureError: If parent or child node doesn't exist
        """
        if parent not in self.nodes:
            raise TreeStructureError(f"Parent node '{parent}' does not exist")
        if child not in self.nodes:
            raise TreeStructureError(f"Child node '{child}' does not exist")
        
        if child not in self.adjacency_list[parent]:
            self.adjacency_list[parent].append(child)
    
    def get_node(self, node_name: str) -> Dict:
        """Retrieve node metadata as dictionary.
        
        Args:
            node_name: Name of node to retrieve
            
        Returns:
            Dictionary containing node metadata
            
        Raises:
            TreeStructureError: If node doesn't exist
        """
        if node_name not in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' does not exist")
        
        return self.nodes[node_name].to_dict()
    
    def get_children(self, node_name: str) -> List[str]:
        """Get all children of a node.
        
        Args:
            node_name: Name of parent node
            
        Returns:
            List of child node names
            
        Raises:
            TreeStructureError: If node doesn't exist
        """
        if node_name not in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' does not exist")
        
        return self.adjacency_list[node_name].copy()
    
    def get_leaf_nodes(self) -> List[str]:
        """Get all leaf nodes in the tree.
        
        Returns:
            List of leaf node names
        """
        leaf_nodes = []
        for node_name, metadata in self.nodes.items():
            if metadata.node_type == "leaf" or len(self.adjacency_list[node_name]) == 0:
                leaf_nodes.append(node_name)
        return leaf_nodes
    
    def traverse_dfs(self, start_node: str = "root") -> Iterator[str]:
        """Traverse tree in depth-first order.
        
        Args:
            start_node: Node to start traversal from (default: "root")
            
        Yields:
            Node names in depth-first order
            
        Raises:
            TreeStructureError: If start node doesn't exist
        """
        if start_node not in self.nodes:
            raise TreeStructureError(f"Start node '{start_node}' does not exist")
        
        visited = set()
        stack = [start_node]
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            
            visited.add(node)
            yield node
            
            # Add children in reverse order so they're processed in correct order
            children = self.adjacency_list[node]
            for child in reversed(children):
                if child not in visited:
                    stack.append(child)
    
    def update_node_metadata(self, node_name: str, **kwargs) -> None:
        """Update node metadata fields.
        
        Args:
            node_name: Name of node to update
            **kwargs: Metadata fields to update
            
        Raises:
            TreeStructureError: If node doesn't exist
        """
        if node_name not in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' does not exist")
        
        metadata = self.nodes[node_name]
        for key, value in kwargs.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
    
    def mark_as_leaf(self, node_name: str) -> None:
        """Mark a node as a leaf node.
        
        Args:
            node_name: Name of node to mark as leaf
            
        Raises:
            TreeStructureError: If node doesn't exist
        """
        if node_name not in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' does not exist")
        
        self.nodes[node_name].node_type = "leaf"
    
    def get_parent(self, node_name: str) -> Optional[str]:
        """Get the parent of a node.
        
        Args:
            node_name: Name of child node
            
        Returns:
            Parent node name, or None if node is root
            
        Raises:
            TreeStructureError: If node doesn't exist
        """
        if node_name not in self.nodes:
            raise TreeStructureError(f"Node '{node_name}' does not exist")
        
        for parent, children in self.adjacency_list.items():
            if node_name in children:
                return parent
        
        return None  # Node is root
    
    def __len__(self) -> int:
        """Get number of nodes in tree.
        
        Returns:
            Number of nodes
        """
        return len(self.nodes)
    
    def __contains__(self, node_name: str) -> bool:
        """Check if node exists in tree.
        
        Args:
            node_name: Node name to check
            
        Returns:
            True if node exists, False otherwise
        """
        return node_name in self.nodes
