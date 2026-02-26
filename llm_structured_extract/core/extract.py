import asyncio
from typing import Any, Dict, Type, Optional, List
from pydantic import BaseModel
from llm_structured_extract.config.settings import settings
from llm_structured_extract.core.schema_registry import get_model
from llm_structured_extract.core.prompt_engine import build_prompt, async_build_prompt
from llm_structured_extract.core.parser import MarkdownParser
from llm_structured_extract.core.exceptions import (
    SchemaError, PromptError, ProviderError, LLMCallError, ParserError
)
from llm_structured_extract.utils.logger import get_logger
from llm_structured_extract.utils.strings import clean_markdown_code_block

logger = get_logger(__name__)

def _get_adapter():
    """统一获取 LLM 适配器逻辑"""
    provider = settings.LLM_PROVIDER.lower()
    from llm_structured_extract.core.llm_adapters.base_adapter import ADAPTER_REGISTRY
    
    adapter_cls = ADAPTER_REGISTRY.get(provider)
    if not adapter_cls:
        supported = sorted(ADAPTER_REGISTRY.keys())
        raise ProviderError(
            f"Unsupported LLM provider '{provider}'. "
            f"Supported: {supported or ['(none registered)']}"
        )
    return adapter_cls()

def _validate_input(text: str, schema_name: str):
    """统一输入校验"""
    if not text.strip():
        raise ValueError("Input text cannot be empty")
    if not schema_name.strip():
        raise ValueError("Schema name cannot be empty")

def extract(text: str, schema_name: str, save_raw_to: Optional[str] = None, context_cache_id: Optional[str] = None) -> str:
    """
    从非结构化文本中提取信息，直接返回LLM生成的Markdown格式结果。
    """
    _validate_input(text, schema_name)

    try:
        model_cls: Type[BaseModel] = get_model(schema_name)
    except ValueError as e:
        raise SchemaError(f"Failed to load schema '{schema_name}': {str(e)}") from e

    prompt: str = build_prompt(text, model_cls)
    adapter = _get_adapter()

    try:
        markdown_output: str = adapter.generate_text(prompt, context_cache_id=context_cache_id)
        
        # 显式保存调试信息（如果指定）
        if save_raw_to:
            with open(save_raw_to, "w", encoding="utf-8") as f:
                f.write(markdown_output)
            logger.info(f"Raw output saved to {save_raw_to}")

        return clean_markdown_code_block(markdown_output)
    except Exception as e:
        logger.error(f"LLM generation failed for schema {schema_name}: {str(e)}")
        raise LLMCallError(f"LLM generation failed: {str(e)}") from e


async def async_extract(text: str, schema_name: str, save_raw_to: Optional[str] = None, context_cache_id: Optional[str] = None) -> str:
    """
    异步从非结构化文本中提取信息。
    """
    _validate_input(text, schema_name)

    try:
        model_cls: Type[BaseModel] = get_model(schema_name)
    except ValueError as e:
        raise SchemaError(f"Failed to load schema '{schema_name}': {str(e)}") from e

    prompt: str = await async_build_prompt(text, model_cls)
    adapter = _get_adapter()
    
    try:
        markdown_output: str = await adapter.agenerate_text(prompt, context_cache_id=context_cache_id)
        
        if save_raw_to:
            def _save():
                with open(save_raw_to, "w", encoding="utf-8") as f:
                    f.write(markdown_output)
            await asyncio.to_thread(_save)
            logger.info(f"Raw output saved to {save_raw_to}")
        
        return clean_markdown_code_block(markdown_output)
    except Exception as e:
        logger.error(f"LLM async generation failed for schema {schema_name}: {str(e)}")
        raise LLMCallError(f"LLM async generation failed: {str(e)}") from e


def extract_to_model(text: str, schema_name: str, save_raw_to: Optional[str] = None, context_cache_id: Optional[str] = None) -> BaseModel:
    """
    从非结构化文本中提取信息并转换为 Pydantic 模型实例。
    """
    markdown_output = extract(text, schema_name, save_raw_to=save_raw_to, context_cache_id=context_cache_id)
    
    model_cls = get_model(schema_name)
    parser = MarkdownParser(model_cls)
    return parser.parse(markdown_output)


async def async_extract_to_model(text: str, schema_name: str, save_raw_to: Optional[str] = None, context_cache_id: Optional[str] = None) -> BaseModel:
    """
    异步提取信息并转换为 Pydantic 模型。
    """
    markdown_output = await async_extract(text, schema_name, save_raw_to=save_raw_to, context_cache_id=context_cache_id)
    
    model_cls = get_model(schema_name)
    parser = MarkdownParser(model_cls)
    
    try:
        return await asyncio.to_thread(parser.parse, markdown_output)
    except Exception as e:
        logger.error(f"Markdown parsing failed in thread pool: {str(e)}")
        raise ParserError(f"Failed to parse structured output: {str(e)}") from e