"""Tests for WritingTree data structure."""

import pytest
from treewriter.tree import WritingTree
from treewriter.utils import TreeStructureError


class TestWritingTreeBasics:
    """Basic tests for WritingTree."""
    
    def test_create_empty_tree(self):
        """Test creating an empty tree."""
        tree = WritingTree()
        assert len(tree) == 0
    
    def test_add_root_node(self):
        """Test adding a root node."""
        tree = WritingTree()
        tree.add_root_node(
            content="Write a story",
            word_count=5000,
            theme="Adventure"
        )
        assert len(tree) == 1
        assert "root" in tree
        
        node = tree.get_node("root")
        assert node["content"] == "Write a story"
        assert node["word_count"] == 5000
        assert node["theme"] == "Adventure"
        assert node["node_type"] == "root"
    
    def test_add_root_node_duplicate(self):
        """Test adding duplicate root node raises error."""
        tree = WritingTree()
        tree.add_root_node(content="Story 1", word_count=1000)
        
        with pytest.raises(TreeStructureError, match="already exists"):
            tree.add_root_node(content="Story 2", word_count=2000)
    
    def test_add_child_node(self):
        """Test adding child nodes."""
        tree = WritingTree()
        tree.add_root_node(content="Main story", word_count=5000)
        tree.add_node(
            node_name="chapter1",
            content="Chapter 1",
            word_count=2000,
            node_type="internal"
        )
        
        assert len(tree) == 2
        assert "chapter1" in tree
        
        node = tree.get_node("chapter1")
        assert node["content"] == "Chapter 1"
        assert node["word_count"] == 2000
        assert node["node_type"] == "internal"
    
    def test_add_duplicate_node(self):
        """Test adding duplicate node raises error."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        tree.add_node(node_name="node1", content="Content", word_count=500)
        
        with pytest.raises(TreeStructureError, match="already exists"):
            tree.add_node(node_name="node1", content="Different", word_count=300)


class TestWritingTreeEdges:
    """Tests for tree edge management."""
    
    def test_add_edge(self):
        """Test adding edges between nodes."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=2000)
        tree.add_edge("root", "ch1")
        
        children = tree.get_children("root")
        assert "ch1" in children
        assert len(children) == 1
    
    def test_add_edge_nonexistent_parent(self):
        """Test adding edge with nonexistent parent raises error."""
        tree = WritingTree()
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=1000)
        
        with pytest.raises(TreeStructureError, match="does not exist"):
            tree.add_edge("nonexistent", "ch1")
    
    def test_add_edge_nonexistent_child(self):
        """Test adding edge with nonexistent child raises error."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        with pytest.raises(TreeStructureError, match="does not exist"):
            tree.add_edge("root", "nonexistent")
    
    def test_get_children(self):
        """Test getting children of a node."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=2000)
        tree.add_node(node_name="ch2", content="Chapter 2", word_count=3000)
        tree.add_edge("root", "ch1")
        tree.add_edge("root", "ch2")
        
        children = tree.get_children("root")
        assert len(children) == 2
        assert "ch1" in children
        assert "ch2" in children
    
    def test_get_children_nonexistent_node(self):
        """Test getting children of nonexistent node raises error."""
        tree = WritingTree()
        
        with pytest.raises(TreeStructureError, match="does not exist"):
            tree.get_children("nonexistent")
    
    def test_get_parent(self):
        """Test getting parent of a node."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=2000)
        tree.add_edge("root", "ch1")
        
        parent = tree.get_parent("ch1")
        assert parent == "root"
    
    def test_get_parent_of_root(self):
        """Test getting parent of root returns None."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        
        parent = tree.get_parent("root")
        assert parent is None


class TestWritingTreeTraversal:
    """Tests for tree traversal."""
    
    def test_traverse_dfs_single_node(self):
        """Test DFS traversal with single node."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        nodes = list(tree.traverse_dfs())
        assert nodes == ["root"]
    
    def test_traverse_dfs_linear_tree(self):
        """Test DFS traversal with linear tree."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=2000)
        tree.add_node(node_name="sec1", content="Section 1", word_count=1000)
        tree.add_edge("root", "ch1")
        tree.add_edge("ch1", "sec1")
        
        nodes = list(tree.traverse_dfs())
        assert nodes == ["root", "ch1", "sec1"]
    
    def test_traverse_dfs_branching_tree(self):
        """Test DFS traversal with branching tree."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=2000)
        tree.add_node(node_name="ch2", content="Chapter 2", word_count=3000)
        tree.add_edge("root", "ch1")
        tree.add_edge("root", "ch2")
        
        nodes = list(tree.traverse_dfs())
        # Should visit root, then ch1, then ch2 (or ch2 then ch1)
        assert nodes[0] == "root"
        assert set(nodes[1:]) == {"ch1", "ch2"}
    
    def test_traverse_dfs_nonexistent_start(self):
        """Test DFS traversal from nonexistent node raises error."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        with pytest.raises(TreeStructureError, match="does not exist"):
            list(tree.traverse_dfs("nonexistent"))


class TestWritingTreeLeafNodes:
    """Tests for leaf node operations."""
    
    def test_get_leaf_nodes_empty_tree(self):
        """Test getting leaf nodes from empty tree."""
        tree = WritingTree()
        leaves = tree.get_leaf_nodes()
        assert leaves == []
    
    def test_get_leaf_nodes_single_node(self):
        """Test getting leaf nodes with single node."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        leaves = tree.get_leaf_nodes()
        assert leaves == ["root"]
    
    def test_get_leaf_nodes_with_children(self):
        """Test getting leaf nodes in tree with children."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=5000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=2000)
        tree.add_node(node_name="ch2", content="Chapter 2", word_count=3000)
        tree.add_edge("root", "ch1")
        tree.add_edge("root", "ch2")
        
        leaves = tree.get_leaf_nodes()
        assert set(leaves) == {"ch1", "ch2"}
        assert "root" not in leaves
    
    def test_mark_as_leaf(self):
        """Test marking a node as leaf."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        tree.add_node(node_name="ch1", content="Chapter 1", word_count=500)
        
        tree.mark_as_leaf("ch1")
        node = tree.get_node("ch1")
        assert node["node_type"] == "leaf"


class TestWritingTreeMetadataUpdate:
    """Tests for updating node metadata."""
    
    def test_update_node_metadata(self):
        """Test updating node metadata."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        tree.update_node_metadata("root", theme="Adventure", writing_tone="Epic")
        node = tree.get_node("root")
        assert node["theme"] == "Adventure"
        assert node["writing_tone"] == "Epic"
    
    def test_update_nonexistent_node(self):
        """Test updating nonexistent node raises error."""
        tree = WritingTree()
        
        with pytest.raises(TreeStructureError, match="does not exist"):
            tree.update_node_metadata("nonexistent", theme="Adventure")
    
    def test_update_generated_text(self):
        """Test updating generated text."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        tree.update_node_metadata("root", generated_text="Once upon a time...")
        node = tree.get_node("root")
        assert node["generated_text"] == "Once upon a time..."
    
    def test_update_outline(self):
        """Test updating outline."""
        tree = WritingTree()
        tree.add_root_node(content="Story", word_count=1000)
        
        outline = "1. Introduction\n2. Rising action\n3. Climax"
        tree.update_node_metadata("root", outline=outline)
        node = tree.get_node("root")
        assert node["outline"] == outline
