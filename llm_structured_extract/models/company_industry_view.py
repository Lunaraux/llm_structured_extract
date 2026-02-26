# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class OverallIndustryView(BaseModel):
    """## 1.整体行业情况如何？（为何过去会这样？未来将会怎么样？以及政策对行业影像情况如何？） [id:overall_industry]"""
    market_size_and_trend: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "整体市场前三年以及未来三年市场规模如何？增速和市场变化趋势如何？"}
    )
    growth_drivers_past_and_future: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "整体市场过去三年增长 / 放缓的主要驱动因素是什么？和未来趋势是什么？"}
    )
    policy_impact_on_supply_demand: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "若为政策导向性市场，政策变动对市场供需带来的变动影响如何？"}
    )
class SubIndustryView(BaseModel):
    """## 2.细分行业情况如何？（细分市场过去和未来为何会这样？未来细分市场的占比情况会如何？） [id:sub_industry]"""
    segmentation_basis: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "细分市场基于整体市场应该如何划分？"}
    )
    submarket_size_and_trend: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "细分市场前三年以及未来三年市场规模如何？增速和市场变化趋势如何？"}
    )
    submarket_drivers_past_and_future: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "细分市场过去三年增长 / 放缓的主要驱动因素是什么？和未来趋势是什么？"}
    )
    policy_impact_on_submarket: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "细分市场若为政策导向性市场，政策变动对市场供需带来的变动影响如何？"}
    )
class IndustryChainView(BaseModel):
    """## 3.行业产业链情况如何？（产业链的每块成本和利润占比情况如何？未来产业链的变化方向是什么？） [id:industry_chain]"""
    industry_chain_structure: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "整个产业链是如何构成的？"}
    )
    cost_profit_distribution_by_segment: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "每个产业链板块所占成本和利润的比例情况如何？"}
    )
    future_evolution_and_logic: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "未来产业链会如何变化？基于什么逻辑和推断？"}
    )
class MarketCompetitionDynamicsSubView(BaseModel):
    """### 市场竞争态势如何？ [id:market_competition_dynamics]"""
    enterprise_count_and_concentration: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "市场的企业数量、市场集中度、进入和退出门槛如何？"}
    )
    product_homogenization_and_margin: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "市场的产品同质化情况、市场目前平均毛利情况如何？"}
    )
class QualitativeSubView(BaseModel):
    """#### 竞争者定性分析情况如何？ [id:qualitative]"""
    competitor_4p_strategy_and_basis: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "4P战略（产品、价格、营销和推广）如何？以及该4各方面是基于什么制定的？"}
    )
class QuantitativeSubView(BaseModel):
    """#### 竞争者定量分析情况如何？ [id:quantitative]"""
    quantitative_metrics: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "竞争对手的销售额、市场份额、各种财务数据和增长情况如何？"}
    )
class CompetitorAnalysisDetailSubView(BaseModel):
    """### 市场竞争者情况如何？（做的好的竞争者是为何？做的不好竞争者是为何？） [id:competitor_analysis_detail]"""
    qualitative: QualitativeSubView = Field(
        default_factory=QualitativeSubView,
        json_schema_extra={"markdown_title": "竞争者定性分析情况如何？"}
    )
    quantitative: QuantitativeSubView = Field(
        default_factory=QuantitativeSubView,
        json_schema_extra={"markdown_title": "竞争者定量分析情况如何？"}
    )
class IndustryCompetitionView(BaseModel):
    """## 4.行业竞争情况如何？ [id:industry_competition]"""
    market_competition_dynamics: MarketCompetitionDynamicsSubView = Field(
        default_factory=MarketCompetitionDynamicsSubView,
        json_schema_extra={"markdown_title": "市场竞争态势如何？"}
    )
    competitor_analysis_detail: CompetitorAnalysisDetailSubView = Field(
        default_factory=CompetitorAnalysisDetailSubView,
        json_schema_extra={"markdown_title": "市场竞争者情况如何？（做的好的竞争者是为何？做的不好竞争者是为何？）"}
    )
class CustomerAndConsumerView(BaseModel):
    """## 5.行业消费者和客户情况如何？（目前消费者和客户是否满意现在的产品和服务？基于消费者的需求未来产品变化的方向和趋势是什么？） [id:customer_and_consumer]"""
    satisfaction_and_core_need_fulfillment: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "消费者和客户对目前产品和服务的评价是什么？目前的产品是否解决了客户的核心需求？"}
    )
    main_complaints_and_dissatisfactions: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "目前消费者和客户对目前的产品和服务主要提出的问题和不满意的地方是什么？"}
    )
    future_needs_and_expectations: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "消费者和客户对未来产品和服务的意见 and 需求是什么？"}
    )
@register_schema
class CompanyIndustryView(BaseModel):
    __business_architecture__: str = """
# 四、公司所属行业如何？ [id:company_industry]

## 1.整体行业情况如何？（为何过去会这样？未来将会怎么样？以及政策对行业影像情况如何？） [id:overall_industry]

### 整体市场前三年以及未来三年市场规模如何？增速和市场变化趋势如何？ [id:market_size_and_trend]
### 整体市场过去三年增长 / 放缓的主要驱动因素是什么？和未来趋势是什么？ [id:growth_drivers_past_and_future]
### 若为政策导向性市场，政策变动对市场供需带来的变动影响如何？ [id:policy_impact_on_supply_demand]

## 2.细分行业情况如何？（细分市场过去和未来为何会这样？未来细分市场的占比情况会如何？） [id:sub_industry]

### 细分市场基于整体市场应该如何划分？ [id:segmentation_basis]
### 细分市场前三年以及未来三年市场规模如何？增速和市场变化趋势如何？ [id:submarket_size_and_trend]
### 细分市场过去三年增长 / 放缓的主要驱动因素是什么？和未来趋势是什么？ [id:submarket_drivers_past_and_future]
### 细分市场若为政策导向性市场，政策变动对市场供需带来的变动影响如何？ [id:policy_impact_on_submarket]

## 3.行业产业链情况如何？（产业链的每块成本和利润占比情况如何？未来产业链的变化方向是什么？） [id:industry_chain]

### 整个产业链是如何构成的？ [id:industry_chain_structure]
### 每个产业链板块所占成本和利润的比例情况如何？ [id:cost_profit_distribution_by_segment]
### 未来产业链会如何变化？基于什么逻辑和推断？ [id:future_evolution_and_logic]

## 4.行业竞争情况如何？ [id:industry_competition]

### 市场竞争态势如何？ [id:market_competition_dynamics]

#### 市场的企业数量、市场集中度、进入和退出门槛如何？ [id:enterprise_count_and_concentration]
#### 市场的产品同质化情况、市场目前平均毛利情况如何？ [id:product_homogenization_and_margin]

### 市场竞争者情况如何？（做的好的竞争者是为何？做的不好竞争者是为何？） [id:competitor_analysis_detail]

#### 竞争者定性分析情况如何？ [id:qualitative]

##### 4P战略（产品、价格、营销和推广）如何？以及该4各方面是基于什么制定的？ [id:competitor_4p_strategy_and_basis]

#### 竞争者定量分析情况如何？ [id:quantitative]

##### 竞争对手的销售额、市场份额、各种财务数据和增长情况如何？ [id:quantitative_metrics]

## 5.行业消费者和客户情况如何？（目前消费者和客户是否满意现在的产品和服务？基于消费者的需求未来产品变化的方向和趋势是什么？） [id:customer_and_consumer]

### 消费者和客户对目前产品和服务的评价是什么？目前的产品是否解决了客户的核心需求？ [id:satisfaction_and_core_need_fulfillment]
### 目前消费者和客户对目前的产品和服务主要提出的问题和不满意的地方是什么？ [id:main_complaints_and_dissatisfactions]
### 消费者和客户对未来产品和服务的意见 and 需求是什么？ [id:future_needs_and_expectations]
""".strip()

    """# 四、公司所属行业如何？ [id:company_industry]"""
    overall_industry: OverallIndustryView = Field(
        default_factory=OverallIndustryView,
        json_schema_extra={"markdown_title": "1.整体行业情况如何？（为何过去会这样？未来将会怎么样？以及政策对行业影像情况如何？）"}
    )
    sub_industry: SubIndustryView = Field(
        default_factory=SubIndustryView,
        json_schema_extra={"markdown_title": "2.细分行业情况如何？（细分市场过去和未来为何会这样？未来细分市场的占比情况会如何？）"}
    )
    industry_chain: IndustryChainView = Field(
        default_factory=IndustryChainView,
        json_schema_extra={"markdown_title": "3.行业产业链情况如何？（产业链的每块成本和利润占比情况如何？未来产业链的变化方向是什么？）"}
    )
    industry_competition: IndustryCompetitionView = Field(
        default_factory=IndustryCompetitionView,
        json_schema_extra={"markdown_title": "4.行业竞争情况如何？"}
    )
    customer_and_consumer: CustomerAndConsumerView = Field(
        default_factory=CustomerAndConsumerView,
        json_schema_extra={"markdown_title": "5.行业消费者和客户情况如何？（目前消费者和客户是否满意现在的产品和服务？基于消费者的需求未来产品变化的方向和趋势是什么？）"}
    )