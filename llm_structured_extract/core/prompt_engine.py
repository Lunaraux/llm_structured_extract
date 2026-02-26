# core/prompt_builder.py
import asyncio
import re
from typing import Type
from pydantic import BaseModel
from jinja2 import Template, Environment
from pathlib import Path
import os
from llm_structured_extract.config.settings import settings
from llm_structured_extract.core.exceptions import PromptError

from functools import lru_cache

@lru_cache(maxsize=1)
def _get_template_path() -> Path:
    custom = os.getenv("PROMPT_TEMPLATE_PATH", "")
    if custom and Path(custom).exists():
        return Path(custom)
    return Path(__file__).parent.parent / "templates" / "prompt.j2"

def _load_template_content() -> str:
    return _get_template_path().read_text(encoding="utf-8")

def _extract_specs(model, prefix=""):
    lines = []
    for name, field in model.model_fields.items():
        path = f"{prefix}.{name}" if prefix else name
        
        # 强制使用 markdown_title，不再使用 description
        markdown_title = None
        if field.json_schema_extra and "markdown_title" in field.json_schema_extra:
            markdown_title = field.json_schema_extra["markdown_title"]
        
        if not markdown_title:
            # 如果没有 markdown_title，可能是中间层级或 summary，
            # 如果是 summary，给一个默认提示，否则可能报错或跳过
            if name == "summary":
                markdown_title = "概要说明"
            else:
                # 对于叶子节点，如果没有 markdown_title，解析器会报错，这里保持一致
                markdown_title = f"（未定义标题: {name}）"

        lines.append(f"- `{path}`: {markdown_title}")
        # 处理嵌套模型
        annotation = field.annotation
        if hasattr(annotation, "model_fields"):
            lines.extend(_extract_specs(annotation, path))
    return lines

def build_prompt(text: str, model_cls: Type[BaseModel]) -> str:
    business_arch = getattr(model_cls, "__business_architecture__", "")
    if not business_arch.strip():
        raise PromptError(f"__business_architecture__ is required for model {model_cls.__name__}")
    
    # 清理骨架中的 [id:xxx] 标记，避免干扰 LLM
    clean_arch = re.sub(r'\s*\[id:[a-zA-Z_][a-zA-Z0-9_]*\]', '', business_arch)
    
    field_specs = "\n".join(_extract_specs(model_cls))
    
    try:
        tpl_content = _load_template_content()
        tpl = Template(tpl_content)
        return tpl.render(
            schema=clean_arch,
            field_specs=field_specs,
            text=text,
            example=settings.get_few_shot_example()
        )
    except Exception as e:
        raise PromptError(f"Failed to build prompt: {str(e)}") from e

async def async_build_prompt(text: str, model_cls: Type[BaseModel]) -> str:
    """异步构建提示词，避免阻塞事件循环"""
    return await asyncio.to_thread(build_prompt, text, model_cls)
