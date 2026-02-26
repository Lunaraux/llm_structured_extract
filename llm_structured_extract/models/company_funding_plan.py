# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class CurrentRoundFundingPlanView(BaseModel):
    """## 本轮融资方案如何？ [id:current_round_funding_plan]"""
    amount_and_equity: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "本次融资金额多少？释放多少股份？"}
    )
    other_needs_besides_funding: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "本次除了融资以外是否有其他需求？"}
    )
@register_schema
class CompanyFundingPlanView(BaseModel):
    __business_architecture__: str = """
# 八、公司融资方案如何？ [id:company_funding_plan]

## 本轮融资方案如何？ [id:current_round_funding_plan]

### 本次融资金额多少？释放多少股份？ [id:amount_and_equity]
### 本次除了融资以外是否有其他需求？ [id:other_needs_besides_funding]
""".strip()

    """# 八、公司融资方案如何？ [id:company_funding_plan]"""
    current_round_funding_plan: CurrentRoundFundingPlanView = Field(
        default_factory=CurrentRoundFundingPlanView,
        json_schema_extra={"markdown_title": "本轮融资方案如何？"}
    )