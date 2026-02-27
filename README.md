# LLM Structured Extract (llm_structured_extract)

本项目是一个基于大语言模型（LLM）的结构化信息提取框架。它能够将非结构化的文本（如研报、新闻、合同等）按照预定义的业务架构（Business Architecture）提取为结构化的数据（Pydantic 模型或 JSON）。

## 主要功能

- **架构驱动提取**：使用直观的 Markdown 格式定义业务提取架构，支持多级嵌套。
- **自动模型生成**：提供工具脚本将 Markdown 架构一键转换为 Python Pydantic 代码。
- **结构化输出保证**：通过 Prompt 引导 LLM 输出符合层级规范的 Markdown，再通过内置解析器还原为对象。
- **模糊匹配解析**：解析器支持标题的模糊匹配和正规化处理，增强了对 LLM 输出波动的容错性。
- **异步与流式支持**：核心提取逻辑支持异步调用，适配高性能服务场景。
- **多模型适配**：通过 Adapter 模式支持多种 LLM 提供商（如阿里云 DashScope 等）。

## 使用流程

### 1. 定义业务架构 (Markdown)
在 `docs/architecture/` 目录下创建或修改 Markdown 文件。使用 `[id:field_name]` 标注字段 ID。
例如 `docs/architecture/example.md`:
```markdown
# 核心团队 [id:core_team]
## 创始人背景 [id:founder_bg]
### 教育经历 [id:education]
```

### 2. 生成 Python 模型
运行生成脚本，将 Markdown 转换为 Pydantic 模型：
```bash
python scripts/generate_models.py docs/architecture/example.md -o llm_structured_extract/models/example_view.py
```

### 3. 执行信息提取
在代码中调用 `extract_to_model` 函数：
```python
from llm_structured_extract.core.extract import extract_to_model

text = "这里是长篇非结构化文本内容..."
# schema_name 为模型类名注册后的 snake_case 形式，例如 'example_view'
result = extract_to_model(text, schema_name="example_view")

print(result.core_team.founder_bg.education)
```

---

## 核心实现逻辑

项目采用了 **"Schema -> Prompt -> LLM -> Markdown -> Pydantic"** 的闭环逻辑。

### 1. 模型生成层 (Model Generator)
- **逻辑**：解析 Markdown 标题层级，利用递归算法构建嵌套的 Pydantic 类。
- **关键点**：标题中的 `[id:xxx]` 标签被提取为 Pydantic 字段名，而标题文字则存储在 `Field(json_schema_extra={"markdown_title": "..."})` 中，用于后续的 Prompt 构建和解析匹配。

### 2. 提示词引擎 (Prompt Engine)
- **逻辑**：动态读取 Pydantic 模型的结构。
- **实现**：
    - 提取模型中的 `__business_architecture__` 骨架。
    - 遍历模型字段，生成对应的字段说明（Specs）。
    - 结合 Jinja2 模板，将架构、说明、示例和待提取文本组合成最终 Prompt。
- **优势**：确保 LLM 了解输出的层级要求（标题层级）和具体字段含义。

### 3. LLM 适配器 (LLM Adapter)
- **逻辑**：封装不同厂商的 API 调用细节。
- **实现**：提供统一的 `generate_text` 和 `agenerate_text` 接口。

### 4. 结构化解析器 (Markdown Parser)
这是本项目的核心逻辑难点：
- **分段逻辑**：通过正则表达式识别 Markdown 标题（`#`, `##` 等），将扁平的 LLM 输出文本切割成一个具有层级结构的字典树。
- **映射逻辑**：
    - 递归遍历 Pydantic 模型的字段。
    - 使用字段定义的 `markdown_title` 在当前的字典树层级中查找对应的 Section。
    - **模糊匹配**：如果标题不完全一致（例如 LLM 漏掉了序号），解析器会进行正规化处理（normalize）和包含匹配，极大提高了提取成功率。
- **数据转换**：将 Section 中的 Content 填充到 Pydantic 字段中，并利用 Pydantic 的 `model_validate` 进行最终的类型校验和转换。

### 5. 自动注册与发现 (Schema Registry)
- **逻辑**：项目启动时自动扫描 `models/` 目录，将所有 Pydantic 模型注册到全局注册表中。
- **实现**：通过 snake_case 转换，方便用户通过字符串名称（如 `company_basic_view`）动态加载对应的模型类。
