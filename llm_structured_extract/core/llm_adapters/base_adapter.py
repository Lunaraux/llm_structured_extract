from abc import ABC, abstractmethod
from typing import Type, Dict, Callable, Optional

ADAPTER_REGISTRY: Dict[str, Type['BaseAdapter']] = {}

def register_adapter(name: str) -> Callable[[Type['BaseAdapter']], Type['BaseAdapter']]:
    def decorator(cls: Type['BaseAdapter']) -> Type['BaseAdapter']:
        ADAPTER_REGISTRY[name] = cls
        return cls
    return decorator

class BaseAdapter(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, context_cache_id: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def agenerate_text(self, prompt: str, context_cache_id: Optional[str] = None) -> str:
        """异步生成文本接口"""
        ...

    def create_context_cache(self, text: str, ttl_seconds: int = 3600) -> Optional[str]:
        """
        创建上下文缓存接口。默认不执行任何操作，由支持的适配器覆盖。
        """
        return None
