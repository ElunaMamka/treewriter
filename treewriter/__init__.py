"""TreeWriter: A hierarchical long-text generation system.

TreeWriter decomposes complex writing tasks into manageable subtasks using a tree
structure, then generates text through a three-phase process: planning, thinking,
and writing.
"""

__version__ = "0.1.0"

from .tree import WritingTree
from .planning import PlanningAgent
from .thinking import ThinkingModel
from .writing import WritingModel
from .orchestrator import TreeWriter
from .config import ModelConfig, ThresholdConfig, NodeMetadata

__all__ = [
    "WritingTree",
    "PlanningAgent",
    "ThinkingModel",
    "WritingModel",
    "TreeWriter",
    "ModelConfig",
    "ThresholdConfig",
    "NodeMetadata",
]
