import re
from llm_structured_extract.core.extract import extract
from llm_structured_extract.core.llm_adapters.base_adapter import ADAPTER_REGISTRY
from pydantic import BaseModel

class _FakeAdapter:
    def __init__(self, *args, **kwargs):
        pass
    def generate_text(self, prompt: str, context_cache_id=None) -> str:
        return "\n".join([
            "# 一、公司基本概况",
            "## 1. 风险核查",
            "- 近期受到处罚情况",
            "  ● 2023年因数据违规被网信办罚款80万元（处罚文号：公网安〔2023〕15号）",
            "## 7. 人力资源配置",
            "- 公司总人数",
            "  ● 总员工280人",
        ])

def test_markdown_structure_and_cleaning(monkeypatch):
    ADAPTER_REGISTRY['dashscope'] = _FakeAdapter
    text = "示例文本"
    md = extract(text, "company_basic_view")
    assert md.startswith("# "), "应以一级标题开头"
    assert "## 1. 风险核查" in md
    assert "●" in md
    assert "```" not in md
    assert "未提及" not in md
