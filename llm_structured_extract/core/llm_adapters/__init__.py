import os
import importlib
from pathlib import Path

# 自动发现并导入当前目录下的所有适配器文件
def _discover_adapters():
    current_dir = Path(__file__).parent
    for file in current_dir.glob("*.py"):
        if file.name in ("__init__.py", "base_adapter.py"):
            continue
        
        module_name = f"llm_structured_extract.core.llm_adapters.{file.stem}"
        importlib.import_module(module_name)

_discover_adapters()