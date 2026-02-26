import pytest
from llm_structured_extract.core.prompt_engine import build_prompt
from llm_structured_extract.core.exceptions import PromptError
from pydantic import BaseModel

class _ModelWithoutArch(BaseModel):
    pass

def test_missing_business_architecture_raises():
    with pytest.raises(PromptError):
        build_prompt("text", _ModelWithoutArch)
