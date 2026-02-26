import pytest
from llm_structured_extract.core.llm_adapters.base_adapter import ADAPTER_REGISTRY
from llm_structured_extract.core.extract import extract

from llm_structured_extract.core.exceptions import LLMCallError

class _BadAdapter:
    pass

def test_adapter_without_generate_text_errors(monkeypatch):
    ADAPTER_REGISTRY['dashscope'] = _BadAdapter
    with pytest.raises(LLMCallError):
        extract("x", "company_basic_view")
