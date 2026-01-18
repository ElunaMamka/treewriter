# TreeWriter

TreeWriter 是一个层次化长文本生成系统，通过将复杂的写作任务分解为可管理的子任务，使用树结构组织，然后通过三阶段流程生成高质量的长文本内容。
本项目核心算法已发表于《计算机科学与探索》：

📖 **[TreeWriter：通过递归式任务分解实现任意长度文本生成](https://d.wanfangdata.com.cn/periodical/jsjkxyts20260104002)**


## 特性

- **层次化分解**：自动将大型写作任务分解为小的、可管理的子任务
- **双重检查机制**：结合阈值判断和 AI 模型判断来决定节点是否继续分解
- **三阶段生成**：
  1. **规划阶段**：递归生成写作树结构
  2. **思考阶段**：为每个叶子节点生成详细的写作大纲
  3. **写作阶段**：根据大纲生成实际文本内容
- **灵活配置**：支持 API 模型和本地模型（本地模型支持待实现）
- **中英文支持**：内置中英文提示词模板

## 安装

```bash
# 克隆仓库
git clone <repository-url>
cd treewriter

# 安装依赖
pip install -r requirements.txt
```

## 快速开始

### 命令行使用

TreeWriter 提供了便捷的命令行接口：

```bash
# 安装（开发模式）
pip install -e .

# 设置 API 密钥
export OPENAI_API_KEY="your-api-key"

# 基本使用
treewriter "写一个关于冒险的故事" --word-count 3000 --output story.txt

# 带完整配置
treewriter "写一个科幻小说" \
  --word-count 8000 \
  --setting "未来世界" \
  --characters "主角,反派,导师" \
  --theme "人工智能与人性" \
  --tone "严肃思考" \
  --style "科技感强" \
  --output scifi.txt

# 查看所有选项
treewriter --help
```

### Python API 使用

```python
from treewriter import TreeWriter, ModelConfig, ThresholdConfig

# 配置模型
model_config = ModelConfig(
    model_type="api",
    api_key="your-api-key",
    api_endpoint="https://api.openai.com/v1",
    model_name="gpt-3.5-turbo"
)

# 配置阈值
threshold_config = ThresholdConfig(
    min_word_count=1000,  # 低于此字数不分解
    max_word_count=5000,  # 高于此字数必须分解
    min_children=2,
    max_children=5
)

# 初始化 TreeWriter
writer = TreeWriter(
    planning_config=model_config,
    thinking_config=model_config,
    writing_config=model_config,
    threshold_config=threshold_config,
    language="cn"
)

# 生成文本
text = writer.generate(
    task="写一个关于冒险的故事",
    word_count=3000,
    theme="勇气和友谊",
    writing_tone="激动人心",
    language_style="生动描述"
)

print(text)
```

### 运行示例

```bash
# 设置 API 密钥
export OPENAI_API_KEY="your-api-key"

# 运行示例脚本
python -m treewriter.example

# 或使用命令行
python -m treewriter "写一个关于冒险的故事" --word-count 1500
```

## 架构

TreeWriter 由以下核心组件组成：

### 1. WritingTree
树结构数据类，管理写作任务的层次关系。

### 2. PlanningAgent
规划代理，负责：
- 递归分解写作任务
- 双重检查机制（阈值 + AI 判断）
- 生成完整的写作树结构

### 3. ThinkingModel
思考模型，负责：
- 为叶子节点生成详细的写作大纲
- 考虑整体任务上下文
- 提供结构化的内容指导

### 4. WritingModel
写作模型，负责：
- 根据大纲生成实际文本
- 保持与整体任务的一致性
- 控制字数和风格

### 5. TreeWriter
主协调器，负责：
- 协调三个阶段的执行
- 管理生成流程
- 拼接最终文本

## 配置

### ModelConfig

```python
ModelConfig(
    model_type="api",           # "api" 或 "local"
    api_key="...",              # API 密钥
    api_endpoint="...",         # API 端点
    model_name="...",           # 模型名称
    temperature=0.8,            # 采样温度
    top_p=0.95,                 # Top-p 采样
    max_tokens=4096             # 最大生成 token 数
)
```

### ThresholdConfig

```python
ThresholdConfig(
    min_word_count=1000,        # 最小字数阈值
    max_word_count=5000,        # 最大字数阈值
    min_children=2,             # 最少子节点数
    max_children=5              # 最多子节点数
)
```

## 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_tree.py -v

# 查看测试覆盖率
pytest tests/ --cov=treewriter --cov-report=html
```

## 项目结构

```
treewriter/
├── __init__.py          # 包初始化
├── config.py            # 配置数据类
├── tree.py              # 写作树数据结构
├── planning.py          # 规划代理
├── thinking.py          # 思考模型
├── writing.py           # 写作模型
├── orchestrator.py      # 主协调器
├── prompts.py           # 提示词模板
├── utils.py             # 工具函数
└── example.py           # 示例脚本

tests/
├── test_config.py       # 配置测试
├── test_tree.py         # 树结构测试
├── test_planning.py     # 规划代理测试
├── test_prompts.py      # 提示词测试
└── conftest.py          # 测试配置
```



## 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

## 许可证

MIT License


