# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class FuturePerformanceView(BaseModel):
    """## 公司未来业绩如何？ [id:future_performance]"""
    revenue_and_growth_rate: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司未来三年营业收入情况如何？未来增长率情况如何？"}
    )
    growth_logic_and_expectation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "未来的增长基于什么逻辑和预期？"}
    )
class CurrentValuationView(BaseModel):
    """## 公司目前估值情况如何？ [id:current_valuation]"""
    current_overall_valuation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前估值情况如何？"}
    )
    current_round_valuation_and_logic: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前这轮融资的估值是多少？这轮估值的定价逻辑是什么？"}
    )
class HistoricalFundingView(BaseModel):
    """## 公司历史融资情况如何？ [id:historical_funding]"""
    number_valuation_and_amount: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司之前有过几次融资？每次融资的估值是多少？每次融资的金额是多少？"}
    )
    redemption_clauses_and_deadlines: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "之前的融资是否有对赌或其他回购条款？对赌和回购的时间节点是什么？"}
    )
@register_schema
class CompanyPerformanceAndValuationView(BaseModel):
    __business_architecture__: str = """
# 公司业绩预测和估值如何？ [id:company_performance_and_valuation]

## 公司未来业绩如何？ [id:future_performance]

### 公司未来三年营业收入情况如何？未来增长率情况如何？ [id:revenue_and_growth_rate]
### 未来的增长基于什么逻辑和预期？ [id:growth_logic_and_expectation]

## 公司目前估值情况如何？ [id:current_valuation]

### 公司目前估值情况如何？ [id:current_overall_valuation]
### 公司目前这轮融资的估值是多少？这轮估值的定价逻辑是什么？ [id:current_round_valuation_and_logic]

## 公司历史融资情况如何？ [id:historical_funding]

### 公司之前有过几次融资？每次融资的估值是多少？每次融资的金额是多少？ [id:number_valuation_and_amount]
### 之前的融资是否有对赌或其他回购条款？对赌和回购的时间节点是什么？ [id:redemption_clauses_and_deadlines]
""".strip()

    """# 公司业绩预测和估值如何？ [id:company_performance_and_valuation]"""
    future_performance: FuturePerformanceView = Field(
        default_factory=FuturePerformanceView,
        json_schema_extra={"markdown_title": "公司未来业绩如何？"}
    )
    current_valuation: CurrentValuationView = Field(
        default_factory=CurrentValuationView,
        json_schema_extra={"markdown_title": "公司目前估值情况如何？"}
    )
    historical_funding: HistoricalFundingView = Field(
        default_factory=HistoricalFundingView,
        json_schema_extra={"markdown_title": "公司历史融资情况如何？"}
    )