# TreeWriter 使用指南

## 安装

### 从源码安装

```bash
# 克隆仓库
git clone <repository-url>
cd treewriter

# 安装依赖
pip install -r requirements.txt

# 开发模式安装（推荐）
pip install -e .
```

### 配置 API 密钥

TreeWriter 需要 OpenAI API 密钥来运行。有两种方式配置：

1. **环境变量**（推荐）：
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. **命令行参数**：
```bash
treewriter "任务描述" --word-count 3000 --api-key "your-api-key-here"
```

## 命令行使用

### 基本用法

最简单的使用方式：

```bash
treewriter "写一个关于冒险的故事" --word-count 3000 --output story.txt
```

### 完整示例

带所有元数据的完整示例：

```bash
treewriter "写一个科幻小说" \
  --word-count 8000 \
  --setting "2150年的火星殖民地" \
  --characters "工程师李明,AI助手ARIA,殖民地长官" \
  --theme "人工智能与人性的边界" \
  --tone "严肃思考" \
  --style "科技感强，细节丰富" \
  --structure "三幕式结构" \
  --plot "从日常工作到发现异常，再到解决危机" \
  --worldbuilding "火星地下城市，先进的AI系统" \
  --goals "探讨AI意识觉醒的可能性" \
  --output scifi_novel.txt
```

### 常用参数

#### 必需参数

- `task`: 写作任务描述（位置参数）
- `--word-count`: 目标字数

#### 模型配置

- `--api-key`: OpenAI API 密钥
- `--api-endpoint`: API 端点（默认：https://api.openai.com/v1）
- `--model`: 模型名称（默认：gpt-3.5-turbo）
- `--temperature`: 采样温度（默认：0.8）
- `--top-p`: Top-p 采样（默认：0.95）
- `--max-tokens`: 最大生成 token 数（默认：4096）

#### 分解阈值

- `--min-word-count`: 最小字数阈值（默认：1000）
- `--max-word-count`: 最大字数阈值（默认：5000）
- `--min-children`: 最少子节点数（默认：2）
- `--max-children`: 最多子节点数（默认：5）

#### 写作元数据

- `--setting`: 故事背景设定
- `--characters`: 角色列表（逗号分隔）
- `--theme`: 核心主题
- `--tone`: 写作语气
- `--style`: 语言风格
- `--structure`: 故事结构
- `--plot`: 情节发展
- `--worldbuilding`: 世界观设定
- `--goals`: 写作目标

#### 输出配置

- `--output, -o`: 输出文件路径（不指定则输出到终端）
- `--language`: 提示词语言（cn 或 en，默认：cn）
- `--max-depth`: 最大树深度（默认：10）
- `--verbose, -v`: 启用详细日志

### 使用技巧

1. **字数控制**：
   - 实际生成字数可能与目标字数有偏差（通常在 ±20% 范围内）
   - 可以通过调整 `--min-word-count` 和 `--max-word-count` 来控制分解粒度

2. **模型选择**：
   - `gpt-3.5-turbo`: 快速、经济，适合一般写作
   - `gpt-4`: 质量更高，但速度较慢、成本较高

3. **温度参数**：
   - 较低温度（0.5-0.7）：更保守、一致的输出
   - 较高温度（0.8-1.0）：更有创意、多样的输出

4. **元数据使用**：
   - 提供越详细的元数据，生成的内容越符合预期
   - 特别是 `theme`、`tone`、`style` 对最终效果影响较大

## Python API 使用

### 基本示例

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
    min_word_count=1000,
    max_word_count=5000,
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

# 保存到文件
with open("story.txt", "w", encoding="utf-8") as f:
    f.write(text)
```

### 高级用法

```python
from treewriter import TreeWriter, ModelConfig, ThresholdConfig

# 为不同阶段使用不同的模型配置
planning_config = ModelConfig(
    model_type="api",
    api_key="your-api-key",
    model_name="gpt-4",  # 规划阶段使用 GPT-4
    temperature=0.7
)

thinking_config = ModelConfig(
    model_type="api",
    api_key="your-api-key",
    model_name="gpt-4",  # 思考阶段使用 GPT-4
    temperature=0.8
)

writing_config = ModelConfig(
    model_type="api",
    api_key="your-api-key",
    model_name="gpt-3.5-turbo",  # 写作阶段使用 GPT-3.5
    temperature=0.9,
    max_tokens=8192
)

# 自定义阈值
threshold_config = ThresholdConfig(
    min_word_count=800,   # 更小的最小阈值
    max_word_count=3000,  # 更小的最大阈值
    min_children=3,       # 更多的子节点
    max_children=6
)

writer = TreeWriter(
    planning_config=planning_config,
    thinking_config=thinking_config,
    writing_config=writing_config,
    threshold_config=threshold_config,
    language="cn"
)

# 生成带完整元数据的文本
text = writer.generate(
    task="写一个科幻小说",
    word_count=10000,
    story_setting="2150年的火星殖民地",
    character_list=["工程师李明", "AI助手ARIA", "殖民地长官"],
    writing_tone="严肃思考",
    language_style="科技感强，细节丰富",
    theme="人工智能与人性的边界",
    story_structure="三幕式结构",
    plot_development="从日常工作到发现异常，再到解决危机",
    worldbuilding="火星地下城市，先进的AI系统",
    writing_goals="探讨AI意识觉醒的可能性",
    max_depth=8
)
```

## 工作原理

TreeWriter 使用三阶段流程生成长文本：

### 阶段 1：规划（Planning）

1. 从根任务开始，递归分解写作任务
2. 对每个节点进行双重检查：
   - **阈值检查**：基于字数判断是否需要分解
   - **AI 检查**：使用 LLM 判断内容复杂度
3. 生成完整的写作树结构

### 阶段 2：思考（Thinking）

1. 遍历所有叶子节点
2. 为每个叶子节点生成详细的写作大纲
3. 大纲考虑整体任务上下文和父节点内容

### 阶段 3：写作（Writing）

1. 遍历所有叶子节点
2. 根据大纲和元数据生成实际文本
3. 按深度优先顺序拼接所有文本

## 常见问题

### Q: 生成时间很长怎么办？

A: 生成时间取决于：
- 目标字数（字数越多，时间越长）
- 模型选择（GPT-4 比 GPT-3.5 慢）
- 树的深度和节点数

建议：
- 从较小的字数开始测试（如 1500-3000 字）
- 使用 `--verbose` 查看进度
- 考虑使用 GPT-3.5 而不是 GPT-4

### Q: 生成的字数与目标不符？

A: 这是正常的，因为：
- LLM 生成的字数难以精确控制
- 树的分解可能导致字数分配不均

建议：
- 允许 ±20% 的偏差
- 调整 `--min-word-count` 和 `--max-word-count` 参数

### Q: 如何提高生成质量？

A: 几个建议：
1. 提供详细的元数据（setting, theme, tone, style 等）
2. 使用更好的模型（如 GPT-4）
3. 调整温度参数（0.7-0.9 通常效果较好）
4. 提供清晰、具体的任务描述

### Q: 支持本地模型吗？

A: 目前仅支持 OpenAI API 兼容的接口。本地模型支持正在开发中。

### Q: 如何保存中间结果？

A: 检查点系统正在开发中。目前建议：
- 使用较小的字数进行测试
- 保存生成的文本到文件

## 示例场景

### 场景 1：写小说章节

```bash
treewriter "写《星际迷航》第三章：遭遇外星文明" \
  --word-count 5000 \
  --setting "23世纪，星舰企业号" \
  --characters "柯克船长,斯波克,麦考伊医生" \
  --theme "探索未知与文化冲突" \
  --tone "紧张刺激" \
  --style "科幻小说风格" \
  --output chapter3.txt
```

### 场景 2：写技术文档

```bash
treewriter "编写 Python 异步编程完整教程" \
  --word-count 8000 \
  --language en \
  --tone "professional and educational" \
  --style "clear and concise" \
  --structure "introduction, basics, advanced, examples" \
  --output async_tutorial.md
```

### 场景 3：写营销文案

```bash
treewriter "为新款智能手表撰写产品介绍" \
  --word-count 2000 \
  --theme "健康与科技的完美结合" \
  --tone "热情积极" \
  --style "简洁有力，突出卖点" \
  --goals "吸引年轻消费者" \
  --output product_intro.txt
```

## 更多资源

- [GitHub 仓库](https://github.com/your-repo/treewriter)
- [问题反馈](https://github.com/your-repo/treewriter/issues)
- [贡献指南](CONTRIBUTING.md)

## 许可证

MIT License
