# llm_structured_extract/core/schema_registry.py
import re
from typing import Dict, Type, Any, Callable
from functools import lru_cache
from pathlib import Path
import importlib.util
from pydantic import BaseModel
from llm_structured_extract.core.exceptions import SchemaError

_SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {}
_SCHEMAS_DISCOVERED = False


def _to_snake_case(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def register_schema(model_cls: Type[BaseModel]) -> Type[BaseModel]:
    """
    显式注册Pydantic模型的装饰器（兼容自动发现逻辑）
    :param model_cls: Pydantic BaseModel子类
    :return: 原模型类
    """
    if not isinstance(model_cls, type) or not issubclass(model_cls, BaseModel):
        raise TypeError("Only Pydantic BaseModel subclasses can be registered")
    
    schema_name = _to_snake_case(model_cls.__name__)
    _SCHEMA_REGISTRY[schema_name] = model_cls
    return model_cls


def _auto_discover_schemas():
    global _SCHEMAS_DISCOVERED
    if _SCHEMAS_DISCOVERED:
        return

    root = Path(__file__).resolve().parents[1]
    models_dir = root / "models"
    if not models_dir.is_dir():
        raise SchemaError(f"Models directory not found: {models_dir.resolve()}")

    for file_path in models_dir.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue

        # 计算相对于 models 目录的模块路径
        relative_path = file_path.relative_to(models_dir)
        module_parts = list(relative_path.with_suffix("").parts)
        module_name = f"llm_structured_extract.models.{'.'.join(module_parts)}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            obj = getattr(module, attr_name)
            if (
                isinstance(obj, type)
                and issubclass(obj, BaseModel)
                and obj is not BaseModel
                and hasattr(obj, 'model_config')
            ):
                schema_name = _to_snake_case(obj.__name__)
                _SCHEMA_REGISTRY[schema_name] = obj

    _SCHEMAS_DISCOVERED = True


def get_model(schema_name: str) -> Type[BaseModel]:
    if not _SCHEMAS_DISCOVERED:
        _auto_discover_schemas()

    if schema_name not in _SCHEMA_REGISTRY:
        available = ", ".join(sorted(_SCHEMA_REGISTRY.keys()))
        raise SchemaError(
            f"Schema '{schema_name}' not found. Available schemas: {available}"
        )
    return _SCHEMA_REGISTRY[schema_name]


@lru_cache(maxsize=128)
def schema_fields_example(schema_name: str) -> Dict[str, Any]:
    model_cls = get_model(schema_name)
    schema = model_cls.model_json_schema()
    schema.pop("$schema", None)
    return schema


def list_available_schemas() -> list[str]:
    if not _SCHEMAS_DISCOVERED:
        _auto_discover_schemas()
    return sorted(_SCHEMA_REGISTRY.keys())


def get_all_schemas() -> Dict[str, Type[BaseModel]]:
    if not _SCHEMAS_DISCOVERED:
        _auto_discover_schemas()
    return _SCHEMA_REGISTRY.copy()


# 暴露公共接口
__all__ = ["register_schema", "get_model", "list_available_schemas", "get_all_schemas", "schema_fields_example"]