"""Prompt templates for TreeWriter models."""

from typing import Dict, Any
import re


# Planning Agent Prompt Template (Chinese)
PLANNING_PROMPT_CN = """## 角色介绍
你是一个专业的写作规划助手，能够将复杂的写作任务分解为可管理的子任务。你的目标是创建一个层次化的写作树结构。

## 当前任务
{content}

## 任务要求
- 目标字数：{word_count} 字
- 故事背景：{story_setting}
- 主要人物：{character_list}
- 写作基调：{writing_tone}
- 语言风格：{language_style}
- 核心主题：{theme}
- 故事结构：{story_structure}
- 情节发展：{plot_development}
- 世界观设定：{worldbuilding}
- 写作目标：{writing_goals}

## 分解决策
请判断当前任务是否需要进一步分解为子任务。

### 判断标准：
1. **字数考虑**：如果任务字数超过 {max_word_count} 字，通常需要分解
2. **复杂度考虑**：如果任务包含多个独立的情节线或主题，应该分解
3. **结构考虑**：如果任务可以自然地分为几个连贯的部分，建议分解
4. **完整性考虑**：如果任务已经足够具体和聚焦，可以不分解

### 如果需要分解：
- 将任务分解为 {min_children} 到 {max_children} 个子任务
- 确保子任务的字数总和等于父任务字数
- 每个子任务应该有明确的写作目标和内容要求
- 子任务之间应该有逻辑连贯性

## 输出格式
请以 JSON 格式输出你的决策：

```json
{{
  "should_decompose": true/false,
  "reasoning": "你的判断理由",
  "children": [
    {{
      "name": "子任务名称",
      "content": "子任务的具体写作要求",
      "word_count": 子任务字数,
      "story_setting": "子任务的场景设定",
      "character_list": ["人物1", "人物2"],
      "writing_goals": "子任务的写作目标"
    }}
  ]
}}
```

如果 should_decompose 为 false，children 数组应为空。
"""

# Planning Agent Prompt Template (English)
PLANNING_PROMPT_EN = """## Role Introduction
You are a professional writing planning assistant capable of decomposing complex writing tasks into manageable subtasks. Your goal is to create a hierarchical writing tree structure.

## Current Task
{content}

## Task Requirements
- Target word count: {word_count} words
- Story setting: {story_setting}
- Main characters: {character_list}
- Writing tone: {writing_tone}
- Language style: {language_style}
- Core theme: {theme}
- Story structure: {story_structure}
- Plot development: {plot_development}
- Worldbuilding: {worldbuilding}
- Writing goals: {writing_goals}

## Decomposition Decision
Please determine whether the current task needs to be further decomposed into subtasks.

### Criteria:
1. **Word Count**: If the task exceeds {max_word_count} words, it usually needs decomposition
2. **Complexity**: If the task contains multiple independent plot lines or themes, it should be decomposed
3. **Structure**: If the task can naturally be divided into several coherent parts, decomposition is recommended
4. **Completeness**: If the task is already specific and focused enough, it may not need decomposition

### If Decomposition is Needed:
- Decompose the task into {min_children} to {max_children} subtasks
- Ensure the sum of subtask word counts equals the parent task word count
- Each subtask should have clear writing goals and content requirements
- Subtasks should have logical coherence

## Output Format
Please output your decision in JSON format:

```json
{{
  "should_decompose": true/false,
  "reasoning": "Your reasoning",
  "children": [
    {{
      "name": "Subtask name",
      "content": "Specific writing requirements for subtask",
      "word_count": subtask_word_count,
      "story_setting": "Subtask setting",
      "character_list": ["Character1", "Character2"],
      "writing_goals": "Subtask writing goals"
    }}
  ]
}}
```

If should_decompose is false, the children array should be empty.
"""

# Thinking Model Prompt Template (Chinese)
THINKING_PROMPT_CN = """## 角色介绍
你是一个专业的写作大纲生成助手。你的任务是为给定的写作任务生成详细的写作大纲。

## 写作任务
{content}

## 任务要求
- 目标字数：{word_count} 字
- 故事背景：{story_setting}
- 主要人物：{character_list}
- 写作基调：{writing_tone}
- 语言风格：{language_style}
- 核心主题：{theme}
- 故事结构：{story_structure}
- 情节发展：{plot_development}
- 世界观设定：{worldbuilding}
- 写作目标：{writing_goals}

## 上下文信息
总体写作任务：{root_content}
父节点任务：{parent_content}

## 要求
请生成一个详细的写作大纲，包括：
1. 主要内容点（3-5个关键点）
2. 每个内容点的展开方向
3. 需要突出的细节和描写重点
4. 与整体任务的衔接方式

大纲应该：
- 符合指定的字数要求
- 体现指定的写作基调和语言风格
- 包含所有相关的人物和场景
- 服务于整体的写作目标

## 输出格式
请直接输出写作大纲，使用清晰的结构化格式（如编号列表或标题层次）。
"""

# Thinking Model Prompt Template (English)
THINKING_PROMPT_EN = """## Role Introduction
You are a professional writing outline generator. Your task is to generate a detailed writing outline for the given writing task.

## Writing Task
{content}

## Task Requirements
- Target word count: {word_count} words
- Story setting: {story_setting}
- Main characters: {character_list}
- Writing tone: {writing_tone}
- Language style: {language_style}
- Core theme: {theme}
- Story structure: {story_structure}
- Plot development: {plot_development}
- Worldbuilding: {worldbuilding}
- Writing goals: {writing_goals}

## Context Information
Overall writing task: {root_content}
Parent node task: {parent_content}

## Requirements
Please generate a detailed writing outline including:
1. Main content points (3-5 key points)
2. Development direction for each point
3. Details and descriptive focuses to highlight
4. How it connects to the overall task

The outline should:
- Match the specified word count
- Reflect the specified writing tone and language style
- Include all relevant characters and settings
- Serve the overall writing goals

## Output Format
Please output the writing outline directly, using a clear structured format (such as numbered lists or heading hierarchy).
"""

# Writing Model Prompt Template (Chinese)
WRITING_PROMPT_CN = """## 角色介绍
你是一个专业的创意写作助手。你的任务是根据提供的大纲和要求生成高质量的文本内容。

## 写作任务
{content}

## 写作大纲
{outline}

## 任务要求
- 目标字数：{word_count} 字
- 故事背景：{story_setting}
- 主要人物：{character_list}
- 写作基调：{writing_tone}
- 语言风格：{language_style}
- 核心主题：{theme}
- 情节发展：{plot_development}
- 世界观设定：{worldbuilding}
- 写作目标：{writing_goals}

## 上下文信息
总体写作任务：{root_content}
已生成的前序内容：
{previous_content}

## 要求
请根据以上大纲和要求，生成完整的文本内容。

写作时请注意：
1. 严格遵循提供的大纲结构
2. 字数应接近目标字数（允许±20%的偏差）
3. 保持与前序内容的连贯性和一致性
4. 充分体现指定的写作基调和语言风格
5. 生动描写人物和场景
6. 确保情节发展符合整体规划

## 输出格式
请直接输出完整的文本内容，不要包含任何元信息或说明。
"""

# Writing Model Prompt Template (English)
WRITING_PROMPT_EN = """## Role Introduction
You are a professional creative writing assistant. Your task is to generate high-quality text content based on the provided outline and requirements.

## Writing Task
{content}

## Writing Outline
{outline}

## Task Requirements
- Target word count: {word_count} words
- Story setting: {story_setting}
- Main characters: {character_list}
- Writing tone: {writing_tone}
- Language style: {language_style}
- Core theme: {theme}
- Plot development: {plot_development}
- Worldbuilding: {worldbuilding}
- Writing goals: {writing_goals}

## Context Information
Overall writing task: {root_content}
Previously generated content:
{previous_content}

## Requirements
Please generate complete text content based on the above outline and requirements.

When writing, please note:
1. Strictly follow the provided outline structure
2. Word count should be close to the target (±20% deviation allowed)
3. Maintain coherence and consistency with previous content
4. Fully reflect the specified writing tone and language style
5. Vividly describe characters and scenes
6. Ensure plot development aligns with overall planning

## Output Format
Please output the complete text content directly, without any meta-information or explanations.
"""


def format_template(template: str, **kwargs) -> str:
    """Format a template with variable substitution.
    
    Args:
        template: Template string with {variable} placeholders
        **kwargs: Variables to substitute
        
    Returns:
        Formatted template string
        
    Raises:
        ValueError: If required variables are missing
    """
    # Find all variables in template
    variables = re.findall(r'\{(\w+)\}', template)
    
    # Check for missing variables
    missing = [var for var in variables if var not in kwargs]
    if missing:
        raise ValueError(f"Missing required variables: {', '.join(missing)}")
    
    # Format template
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing variable: {e}")


def get_planning_prompt(language: str = "cn") -> str:
    """Get planning agent prompt template.
    
    Args:
        language: Language code ("cn" or "en")
        
    Returns:
        Planning prompt template
    """
    if language == "cn":
        return PLANNING_PROMPT_CN
    elif language == "en":
        return PLANNING_PROMPT_EN
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_thinking_prompt(language: str = "cn") -> str:
    """Get thinking model prompt template.
    
    Args:
        language: Language code ("cn" or "en")
        
    Returns:
        Thinking prompt template
    """
    if language == "cn":
        return THINKING_PROMPT_CN
    elif language == "en":
        return THINKING_PROMPT_EN
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_writing_prompt(language: str = "cn") -> str:
    """Get writing model prompt template.
    
    Args:
        language: Language code ("cn" or "en")
        
    Returns:
        Writing prompt template
    """
    if language == "cn":
        return WRITING_PROMPT_CN
    elif language == "en":
        return WRITING_PROMPT_EN
    else:
        raise ValueError(f"Unsupported language: {language}")
