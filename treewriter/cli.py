"""Command-line interface for TreeWriter."""

import argparse
import os
import sys
from typing import Optional

from .config import ModelConfig, ThresholdConfig
from .orchestrator import TreeWriter
from .utils import setup_logger


logger = setup_logger(__name__)


def parse_args():
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="TreeWriter - Hierarchical long-text generation system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with API key from environment
  treewriter "写一个关于冒险的故事" --word-count 3000 --output story.txt
  
  # With custom configuration
  treewriter "Write an adventure story" \\
    --word-count 5000 \\
    --api-key YOUR_KEY \\
    --model gpt-4 \\
    --theme "courage and friendship" \\
    --tone "exciting" \\
    --output adventure.txt
  
  # With all metadata
  treewriter "写一个科幻小说" \\
    --word-count 8000 \\
    --setting "未来世界" \\
    --characters "主角,反派,导师" \\
    --theme "人工智能与人性" \\
    --tone "严肃思考" \\
    --style "科技感强" \\
    --output scifi.txt
        """
    )
    
    # Required arguments
    parser.add_argument(
        "task",
        type=str,
        help="Writing task description (e.g., '写一个关于冒险的故事')"
    )
    
    parser.add_argument(
        "--word-count",
        type=int,
        required=True,
        help="Target word count for the generated text"
    )
    
    # Model configuration
    model_group = parser.add_argument_group("Model Configuration")
    model_group.add_argument(
        "--api-key",
        type=str,
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI API key (default: from OPENAI_API_KEY env var)"
    )
    
    model_group.add_argument(
        "--api-endpoint",
        type=str,
        default="https://api.openai.com/v1",
        help="API endpoint URL (default: https://api.openai.com/v1)"
    )
    
    model_group.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="Model name (default: gpt-3.5-turbo)"
    )
    
    model_group.add_argument(
        "--temperature",
        type=float,
        default=0.8,
        help="Sampling temperature (default: 0.8)"
    )
    
    model_group.add_argument(
        "--top-p",
        type=float,
        default=0.95,
        help="Top-p sampling (default: 0.95)"
    )
    
    model_group.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum tokens per generation (default: 4096)"
    )
    
    # Threshold configuration
    threshold_group = parser.add_argument_group("Decomposition Thresholds")
    threshold_group.add_argument(
        "--min-word-count",
        type=int,
        default=1000,
        help="Minimum word count threshold (default: 1000)"
    )
    
    threshold_group.add_argument(
        "--max-word-count",
        type=int,
        default=5000,
        help="Maximum word count threshold (default: 5000)"
    )
    
    threshold_group.add_argument(
        "--min-children",
        type=int,
        default=2,
        help="Minimum number of children per node (default: 2)"
    )
    
    threshold_group.add_argument(
        "--max-children",
        type=int,
        default=5,
        help="Maximum number of children per node (default: 5)"
    )
    
    # Writing metadata
    metadata_group = parser.add_argument_group("Writing Metadata")
    metadata_group.add_argument(
        "--setting",
        type=str,
        help="Story setting (e.g., '未来世界', 'medieval fantasy')"
    )
    
    metadata_group.add_argument(
        "--characters",
        type=str,
        help="Comma-separated list of characters (e.g., '主角,反派,导师')"
    )
    
    metadata_group.add_argument(
        "--theme",
        type=str,
        help="Core theme (e.g., '勇气和友谊', 'courage and friendship')"
    )
    
    metadata_group.add_argument(
        "--tone",
        type=str,
        help="Writing tone (e.g., '激动人心', 'exciting')"
    )
    
    metadata_group.add_argument(
        "--style",
        type=str,
        help="Language style (e.g., '生动描述', 'vivid description')"
    )
    
    metadata_group.add_argument(
        "--structure",
        type=str,
        help="Story structure (e.g., '三幕式', 'three-act structure')"
    )
    
    metadata_group.add_argument(
        "--plot",
        type=str,
        help="Plot development notes"
    )
    
    metadata_group.add_argument(
        "--worldbuilding",
        type=str,
        help="Worldbuilding details"
    )
    
    metadata_group.add_argument(
        "--goals",
        type=str,
        help="Writing goals"
    )
    
    # Output configuration
    output_group = parser.add_argument_group("Output Configuration")
    output_group.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (default: print to stdout)"
    )
    
    output_group.add_argument(
        "--language",
        type=str,
        choices=["cn", "en"],
        default="cn",
        help="Prompt language (default: cn)"
    )
    
    output_group.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum tree depth (default: 10)"
    )
    
    output_group.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Set up logging
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)
    
    # Validate API key
    if not args.api_key:
        print("Error: API key is required. Set OPENAI_API_KEY environment variable or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Create model configuration
        model_config = ModelConfig(
            model_type="api",
            api_key=args.api_key,
            api_endpoint=args.api_endpoint,
            model_name=args.model,
            temperature=args.temperature,
            top_p=args.top_p,
            max_tokens=args.max_tokens
        )
        
        # Create threshold configuration
        threshold_config = ThresholdConfig(
            min_word_count=args.min_word_count,
            max_word_count=args.max_word_count,
            min_children=args.min_children,
            max_children=args.max_children
        )
        
        # Initialize TreeWriter
        print(f"Initializing TreeWriter...")
        writer = TreeWriter(
            planning_config=model_config,
            thinking_config=model_config,
            writing_config=model_config,
            threshold_config=threshold_config,
            language=args.language
        )
        
        # Parse character list
        character_list = None
        if args.characters:
            character_list = [c.strip() for c in args.characters.split(",")]
        
        # Generate text
        print(f"\nGenerating text for task: {args.task}")
        print(f"Target word count: {args.word_count}")
        print(f"This may take several minutes...\n")
        
        text = writer.generate(
            task=args.task,
            word_count=args.word_count,
            story_setting=args.setting,
            character_list=character_list,
            writing_tone=args.tone,
            language_style=args.style,
            theme=args.theme,
            story_structure=args.structure,
            plot_development=args.plot,
            worldbuilding=args.worldbuilding,
            writing_goals=args.goals,
            max_depth=args.max_depth
        )
        
        # Output text
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n✓ Text generated successfully!")
            print(f"✓ Saved to: {args.output}")
            print(f"✓ Word count: {len(text.split())} words")
        else:
            print("\n" + "="*80)
            print("GENERATED TEXT")
            print("="*80 + "\n")
            print(text)
            print("\n" + "="*80)
            print(f"Word count: {len(text.split())} words")
            print("="*80)
        
    except KeyboardInterrupt:
        print("\n\nGeneration interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
