# core/llm_adapters/dashscope_adapter.py
import os
from typing import Optional
import dashscope
from llm_structured_extract.core.llm_adapters.base_adapter import BaseAdapter, register_adapter
from llm_structured_extract.config.settings import settings
from llm_structured_extract.core.exceptions import ConfigurationError, LLMCallError
from llm_structured_extract.utils.logger import get_logger

logger = get_logger(__name__)


@register_adapter("dashscope")
class DashScopeAdapter(BaseAdapter):
    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 DashScope 适配器
        使用统一配置系统中的模型配置
        """
        key = api_key or settings.DASHSCOPE_API_KEY or os.getenv("DASHSCOPE_API_KEY", "")
        if not key:
            raise ConfigurationError("DashScope API key is required. Set DASHSCOPE_API_KEY in env or settings.")
        dashscope.api_key = key
        
        # 从统一配置获取模型参数
        model_config = settings.get_model_config("dashscope")
        self.model = model or model_config.name

    def _prepare_params(self, prompt: str, context_cache_id: Optional[str] = None):
        """准备 API 调用参数"""
        model_config = settings.get_model_config("dashscope")
        system_prompt = settings.get_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        
        params = {
            "model": self.model,
            "messages": messages,
            "result_format": "message",
            "temperature": model_config.temperature,
            "max_tokens": model_config.max_tokens,
        }
        
        if context_cache_id:
            # 阿里灵积 Context Cache 参数
            params["context_cache_id"] = context_cache_id
            
        return params

    def _process_response(self, resp, is_async=False) -> str:
        """统一处理 API 响应"""
        if resp.status_code != 200:
            raise LLMCallError(f"DashScope API failed with status {resp.status_code}: {resp.message}")
        
        try:
            content = resp.output.choices[0].message.content
            if not content:
                raise LLMCallError("LLM returned empty response")
            
            mode = "Async" if is_async else "Sync"
            logger.debug(f"LLM Raw {mode} Response from {self.model}:\n{content}")
            return content.strip()
        except AttributeError as e:
            raise LLMCallError(f"DashScope API response format error: {str(e)}") from e
        except Exception as e:
            if isinstance(e, LLMCallError):
                raise
            raise LLMCallError(f"DashScope API call failed: {str(e)}") from e

    def generate_text(self, prompt: str, context_cache_id: Optional[str] = None) -> str:
        """生成纯净 Markdown 响应"""
        params = self._prepare_params(prompt, context_cache_id=context_cache_id)
        resp = dashscope.Generation.call(**params)
        return self._process_response(resp)

    async def agenerate_text(self, prompt: str, context_cache_id: Optional[str] = None) -> str:
        """异步生成纯净 Markdown 响应"""
        import asyncio
        # 使用 asyncio.to_thread 包装同步调用，确保兼容性并避免阻塞事件循环
        return await asyncio.to_thread(self.generate_text, prompt, context_cache_id=context_cache_id)

    def create_context_cache(self, text: str, ttl_seconds: int = 3600) -> Optional[str]:
        """
        创建上下文缓存以减少重复输入的 Token 消耗。
        
        :param text: 需要缓存的文本内容
        :param ttl_seconds: 缓存有效期（秒）
        :return: cache_id 或 None
        """
        try:
            # 这里的 messages 结构需要符合阿里 Context Cache 的要求
            # 通常是将长文本作为 system 或 user 消息的第一部分
            messages = [
                {"role": "system", "content": "你是一个专业的尽调分析师。"},
                {"role": "user", "content": f"请阅读以下参考文档：\n\n{text}"}
            ]
            
            # 注意：实际调用可能需要根据 dashscope SDK 版本调整
            # 这里的逻辑假设 dashscope.ContextCache 可用
            if hasattr(dashscope, 'ContextCache'):
                resp = dashscope.ContextCache.create(
                    model=self.model,
                    messages=messages,
                    ttl=ttl_seconds
                )
                if resp.status_code == 200:
                    logger.info(f"Context Cache created successfully: {resp.output.cache_id}")
                    return resp.output.cache_id
                else:
                    logger.warning(f"Failed to create Context Cache: {resp.message}")
            return None
        except Exception as e:
            logger.error(f"Error creating context cache: {str(e)}")
            return None
