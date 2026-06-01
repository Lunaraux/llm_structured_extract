# core/prompt_builder.py
import asyncio
import re
import typing
from typing import Type, Tuple, Any, List, get_origin, get_args
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

@lru_cache(maxsize=1)
def _load_template_content() -> str:
    return _get_template_path().read_text(encoding="utf-8")

def _unwrap_annotation(annotation: Any) -> Tuple[Any, bool]:
    """Unwrap Optional[X], List[X], Annotated[X, ...] to find the inner type.

    Returns (inner_type, is_list).
    """
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Annotated types first (Pydantic v2 pattern):
    #   Annotated[Optional[SomeModel], ...] → unwrap to Optional[SomeModel] → recurse
    if origin is not None and getattr(origin, "__name__", None) == "Annotated":
        return _unwrap_annotation(args[0])

    if origin is typing.Union:
        non_none = [a for a in args if not (isinstance(a, type) and issubclass(a, type(None)))]
        if len(non_none) == 1:
            return _unwrap_annotation(non_none[0])
        # Multi-type union — cannot resolve deterministically
        return annotation, False

    if origin in (list, List):
        if args:
            inner, _ = _unwrap_annotation(args[0])
            return inner, True

    return annotation, False

def _extract_specs(model: Type[BaseModel], prefix: str = "", level: int = 0) -> List[str]:
    lines = []
    indent = "  " * level
    for name, field in model.model_fields.items():
        path = f"{prefix}.{name}" if prefix else name
        
        # 强制使用 markdown_title，不再使用 description
        extra = field.json_schema_extra or {}
        markdown_title = extra.get("markdown_title")
        hint = extra.get("extraction_hint") or ""
        hint_str = f" → {hint}" if hint else ""
        
        if not markdown_title:
            # 如果没有 markdown_title，可能是中间层级或 summary，
            # 如果是 summary，给一个默认提示，否则可能报错或跳过
            if name == "summary":
                markdown_title = "概要说明"
            else:
                # 对于叶子节点，如果没有 markdown_title，解析器会报错，这里保持一致
                markdown_title = f"（未定义标题: {name}）"

        lines.append(f"{indent}- `{path}`: {markdown_title}{hint_str}")
        # 处理嵌套模型
        annotation = field.annotation
        unwrapped_type, _ = _unwrap_annotation(annotation)
        
        if hasattr(unwrapped_type, "model_fields"):
            lines.extend(_extract_specs(unwrapped_type, path, level + 1))
    return lines

def build_prompt(
    text: str,
    model_cls: Type[BaseModel],
    module_name: str = "",
    few_shot_example: str | None = None
) -> str:
    business_arch = getattr(model_cls, "__business_architecture__", "")
    if not business_arch.strip():
        raise PromptError(f"__business_architecture__ is required for model {model_cls.__name__}")
    
    # 清理骨架中的 [id:xxx] 标记，避免干扰 LLM
    clean_arch = re.sub(r'\s*\[id:[a-zA-Z_][a-zA-Z0-9_]*\]', '', business_arch)
    
    specs_list = _extract_specs(model_cls)
    field_specs = "\n".join(specs_list)
    total_fields = len(specs_list)
    
    try:
        tpl_content = _load_template_content()
        tpl = Template(tpl_content)
        return tpl.render(
            schema=clean_arch,
            field_specs=field_specs,
            text=text,
            module_name=module_name,
            example=few_shot_example if few_shot_example is not None else settings.get_few_shot_example(),
            field_count=total_fields
        )
    except Exception as e:
        raise PromptError(f"Failed to build prompt: {str(e)}") from e

async def async_build_prompt(
    text: str,
    model_cls: Type[BaseModel],
    module_name: str = "",
    few_shot_example: str | None = None
) -> str:
    """异步构建提示词，避免阻塞事件循环"""
    return await asyncio.to_thread(build_prompt, text, model_cls, module_name, few_shot_example)
