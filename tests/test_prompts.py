"""Tests for prompt templates."""

import pytest
from treewriter.prompts import (
    format_template,
    get_planning_prompt,
    get_thinking_prompt,
    get_writing_prompt,
    PLANNING_PROMPT_CN,
    THINKING_PROMPT_CN,
    WRITING_PROMPT_CN,
)


class TestFormatTemplate:
    """Tests for template formatting."""
    
    def test_format_simple_template(self):
        """Test formatting a simple template."""
        template = "Hello {name}, you are {age} years old."
        result = format_template(template, name="Alice", age=30)
        assert result == "Hello Alice, you are 30 years old."
    
    def test_format_template_with_missing_variable(self):
        """Test formatting template with missing variable raises error."""
        template = "Hello {name}, you are {age} years old."
        with pytest.raises(ValueError, match="Missing required variables"):
            format_template(template, name="Alice")
    
    def test_format_template_with_extra_variables(self):
        """Test formatting template with extra variables (should work)."""
        template = "Hello {name}!"
        result = format_template(template, name="Alice", age=30, city="NYC")
        assert result == "Hello Alice!"
    
    def test_format_template_no_variables(self):
        """Test formatting template with no variables."""
        template = "Hello world!"
        result = format_template(template)
        assert result == "Hello world!"
    
    def test_format_template_with_numbers(self):
        """Test formatting template with numeric values."""
        template = "Count: {count}, Price: {price}"
        result = format_template(template, count=5, price=19.99)
        assert result == "Count: 5, Price: 19.99"
    
    def test_format_template_with_none(self):
        """Test formatting template with None values."""
        template = "Value: {value}"
        result = format_template(template, value=None)
        assert result == "Value: None"


class TestGetPrompts:
    """Tests for getting prompt templates."""
    
    def test_get_planning_prompt_cn(self):
        """Test getting Chinese planning prompt."""
        prompt = get_planning_prompt("cn")
        assert "角色介绍" in prompt
        assert "分解决策" in prompt
        assert "{content}" in prompt
        assert "{word_count}" in prompt
    
    def test_get_planning_prompt_en(self):
        """Test getting English planning prompt."""
        prompt = get_planning_prompt("en")
        assert "Role Introduction" in prompt
        assert "Decomposition Decision" in prompt
        assert "{content}" in prompt
        assert "{word_count}" in prompt
    
    def test_get_planning_prompt_invalid_language(self):
        """Test getting planning prompt with invalid language."""
        with pytest.raises(ValueError, match="Unsupported language"):
            get_planning_prompt("fr")
    
    def test_get_thinking_prompt_cn(self):
        """Test getting Chinese thinking prompt."""
        prompt = get_thinking_prompt("cn")
        assert "角色介绍" in prompt
        assert "写作任务" in prompt
        assert "{content}" in prompt
        assert "{word_count}" in prompt
    
    def test_get_thinking_prompt_en(self):
        """Test getting English thinking prompt."""
        prompt = get_thinking_prompt("en")
        assert "Role Introduction" in prompt
        assert "Writing Task" in prompt
        assert "{content}" in prompt
        assert "{word_count}" in prompt
    
    def test_get_writing_prompt_cn(self):
        """Test getting Chinese writing prompt."""
        prompt = get_writing_prompt("cn")
        assert "角色介绍" in prompt
        assert "写作任务" in prompt
        assert "{content}" in prompt
        assert "{outline}" in prompt
    
    def test_get_writing_prompt_en(self):
        """Test getting English writing prompt."""
        prompt = get_writing_prompt("en")
        assert "Role Introduction" in prompt
        assert "Writing Task" in prompt
        assert "{content}" in prompt
        assert "{outline}" in prompt


class TestPromptVariables:
    """Tests for prompt template variables."""
    
    def test_planning_prompt_has_required_variables(self):
        """Test planning prompt contains all required variables."""
        prompt = PLANNING_PROMPT_CN
        required_vars = [
            "content", "word_count", "story_setting", "character_list",
            "writing_tone", "language_style", "theme", "story_structure",
            "plot_development", "worldbuilding", "writing_goals",
            "max_word_count", "min_children", "max_children"
        ]
        for var in required_vars:
            assert f"{{{var}}}" in prompt, f"Missing variable: {var}"
    
    def test_thinking_prompt_has_required_variables(self):
        """Test thinking prompt contains all required variables."""
        prompt = THINKING_PROMPT_CN
        required_vars = [
            "content", "word_count", "story_setting", "character_list",
            "writing_tone", "language_style", "theme", "story_structure",
            "plot_development", "worldbuilding", "writing_goals",
            "root_content", "parent_content"
        ]
        for var in required_vars:
            assert f"{{{var}}}" in prompt, f"Missing variable: {var}"
    
    def test_writing_prompt_has_required_variables(self):
        """Test writing prompt contains all required variables."""
        prompt = WRITING_PROMPT_CN
        required_vars = [
            "content", "outline", "word_count", "story_setting",
            "character_list", "writing_tone", "language_style", "theme",
            "plot_development", "worldbuilding", "writing_goals",
            "root_content", "previous_content"
        ]
        for var in required_vars:
            assert f"{{{var}}}" in prompt, f"Missing variable: {var}"


class TestPromptFormatting:
    """Tests for formatting complete prompts."""
    
    def test_format_planning_prompt(self):
        """Test formatting a complete planning prompt."""
        template = get_planning_prompt("cn")
        
        formatted = format_template(
            template,
            content="写一个冒险故事",
            word_count=5000,
            story_setting="中世纪奇幻世界",
            character_list=["英雄", "导师"],
            writing_tone="史诗般的",
            language_style="描述性的",
            theme="勇气",
            story_structure="三幕式",
            plot_development="英雄之旅",
            worldbuilding="魔法世界",
            writing_goals="展现成长",
            max_word_count=5000,
            min_children=2,
            max_children=5
        )
        
        assert "写一个冒险故事" in formatted
        assert "5000" in formatted
        assert "中世纪奇幻世界" in formatted
    
    def test_format_thinking_prompt(self):
        """Test formatting a complete thinking prompt."""
        template = get_thinking_prompt("cn")
        
        formatted = format_template(
            template,
            content="第一章：开始",
            word_count=2000,
            story_setting="村庄",
            character_list=["主角"],
            writing_tone="轻松",
            language_style="简洁",
            theme="冒险",
            story_structure="线性",
            plot_development="介绍",
            worldbuilding="普通世界",
            writing_goals="建立背景",
            root_content="完整故事",
            parent_content="第一部分"
        )
        
        assert "第一章：开始" in formatted
        assert "2000" in formatted
        assert "村庄" in formatted
    
    def test_format_writing_prompt(self):
        """Test formatting a complete writing prompt."""
        template = get_writing_prompt("cn")
        
        formatted = format_template(
            template,
            content="描写战斗场景",
            outline="1. 准备\n2. 战斗\n3. 结果",
            word_count=1000,
            story_setting="战场",
            character_list=["战士"],
            writing_tone="紧张",
            language_style="动作描写",
            theme="勇气",
            plot_development="高潮",
            worldbuilding="战争世界",
            writing_goals="展现勇气",
            root_content="完整故事",
            previous_content="之前的内容..."
        )
        
        assert "描写战斗场景" in formatted
        assert "1. 准备" in formatted
        assert "1000" in formatted
