"""Example usage of TreeWriter."""

import os
from treewriter import TreeWriter, ModelConfig, ThresholdConfig


def main():
    """Run a simple example of TreeWriter."""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set OPENAI_API_KEY environment variable")
        return
    
    # Configure models (using same model for all three roles for simplicity)
    model_config = ModelConfig(
        model_type="api",
        api_key=api_key,
        api_endpoint="https://api.openai.com/v1",
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=2048
    )
    
    # Configure thresholds
    threshold_config = ThresholdConfig(
        min_word_count=500,   # Don't decompose below 500 words
        max_word_count=2000,  # Must decompose above 2000 words
        min_children=2,
        max_children=4
    )
    
    # Initialize TreeWriter
    writer = TreeWriter(
        planning_config=model_config,
        thinking_config=model_config,
        writing_config=model_config,
        threshold_config=threshold_config,
        language="cn"  # Use Chinese prompts
    )
    
    # Generate text
    print("Starting text generation...")
    print("=" * 60)
    
    text = writer.generate(
        task="写一个关于勇敢的小女孩在森林中冒险的短篇故事",
        word_count=1500,
        story_setting="神秘的魔法森林",
        character_list=["小女孩艾拉", "智慧的老树精"],
        writing_tone="温馨而充满冒险感",
        language_style="生动活泼，适合儿童阅读",
        theme="勇气和成长",
        writing_goals="展现主角如何克服恐惧，学会独立",
        max_depth=3  # Limit depth for this example
    )
    
    print("=" * 60)
    print("Generated Text:")
    print("=" * 60)
    print(text)
    print("=" * 60)
    print(f"Total length: {len(text)} characters, ~{len(text.split())} words")
    
    # Save to file
    output_file = "generated_story.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\nText saved to: {output_file}")


if __name__ == "__main__":
    main()
