"""Utility functions for TreeWriter."""

import logging
from typing import Dict, Any


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with consistent formatting.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def count_words(text: str) -> int:
    """Count words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


class TreeWriterError(Exception):
    """Base exception for TreeWriter errors."""
    pass


class ConfigurationError(TreeWriterError):
    """Raised for configuration issues."""
    pass


class GenerationError(TreeWriterError):
    """Raised when model generation fails."""
    
    def __init__(self, message: str, node_name: str, context: Dict[str, Any]):
        """Initialize generation error.
        
        Args:
            message: Error message
            node_name: Name of node where error occurred
            context: Additional context information
        """
        self.node_name = node_name
        self.context = context
        super().__init__(message)


class TreeStructureError(TreeWriterError):
    """Raised for tree structure violations."""
    pass
