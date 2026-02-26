# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class BusinessModelView(BaseModel):
    """## 1.公司主要业务模式是什么？ [id:business_model]"""
    main_business_services: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司提供的主要业务服务是什么？"}
    )
    main_products_and_features: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司主要生产的产品是哪些？详细介绍一下公司产品和服务特点是什么？"}
    )
    product_revenue_breakdown: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司每一样产品或服务占收入的比重是多少？"}
    )
class ProfitModelView(BaseModel):
    """## 2.公司盈利模式如何？ [id:profit_model]"""
    profit_mechanism: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "详细说明公司具体是如何赚钱？"}
    )
class ProductSubView(BaseModel):
    """### 产品（product）如何？ [id:product]"""
    differentiation_advantage: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品的差异化优势是什么？"}
    )
    brand_image: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品的品牌形象是什么？"}
    )
    target_customers: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品主要针对的客户是什么？"}
    )
    customer_satisfaction: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "消费者对产品的满意度如何？"}
    )
    cost_structure: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品的成本结构如何构成？"}
    )
    pricing_basis: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品的价格制定依据是什么？"}
    )
    competitor_pricing_basis: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "竞争对手的定价依据是什么？"}
    )
    price_sensitivity_and_expectation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "消费者或客户对目前价格的敏感程度如何？价格是否符合消费者或客户的预期？"}
    )
class ChannelSubView(BaseModel):
    """### 渠道（place）如何？ [id:channel]"""
    sales_channels: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品的销售渠道目前有哪些？"}
    )
    channel_revenue_sharing: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "产品和销售渠道是如何分成的？"}
    )
    channel_coverage_and_efficiency: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "销售渠道覆盖范围和效率如何？"}
    )
    sales_team_building: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司自身的销售团队如何打造？"}
    )
    sales_team_incentives: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "销售团队的激励政策是什么？对团队是否有正向的激励作用？"}
    )
    customer_purchase_habits: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "消费者的购买习惯是什么？"}
    )
class PromotionSubView(BaseModel):
    """### 推广（promotion）如何？ [id:promotion]"""
    promotion_target_audience: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "推广活动的目标受众群体是什么？"}
    )
    promotion_strategy_and_channel: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "推广活动的策略是什么？主要考虑线上还是线下？"}
    )
    promotion_roi: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "推广活动的投入产出比如何？"}
    )
    promotion_effectiveness_evaluation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "推广活动的效果评估如何？"}
    )
class SalesModelView(BaseModel):
    """## 3.公司销售模式如何？（主要了解公司销售渠道，初步访谈简要了解；详细访谈深入了解） [id:sales_model]"""
    product: ProductSubView = Field(
        default_factory=ProductSubView,
        json_schema_extra={"markdown_title": "产品（product）如何？"}
    )
    channel: ChannelSubView = Field(
        default_factory=ChannelSubView,
        json_schema_extra={"markdown_title": "渠道（place）如何？"}
    )
    promotion: PromotionSubView = Field(
        default_factory=PromotionSubView,
        json_schema_extra={"markdown_title": "推广（promotion）如何？"}
    )
class CoreTechAndAdvantageView(BaseModel):
    """## 4.公司核心技术及优势是什么？ [id:core_tech_and_advantage]"""
    core_technology_and_barriers: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司核心技术以及核心竞争壁垒是什么？为什么竞争对手不能做出和公司一样的产品或服务？"}
    )
    sustainability_of_advantage: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司如何持续保证在这块的优势？"}
    )
    rd_system_and_strategy: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的研发体系和战略是什么？"}
    )
    rd_team_status: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司研发团队情况如何？"}
    )
    latest_rd_progress: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司最新研发进展情况如何？"}
    )
    rd_investment_history_and_plan: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司近三年在研发方面投入的情况如何？未来在研发上面的投入计划如何？"}
    )
    patents_and_qualifications: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司拥有的相关专利及资质情况如何？"}
    )
    qualification_application_difficulty: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司相关资质和牌照申请的难度如何？（针对不同行业不同资质）"}
    )
class ProductionProcessView(BaseModel):
    """## 5.公司生产流程及工艺如何？（只分析制造类企业，服务类企业不询问） [id:production_process]"""
    production_process_details: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "详细说明公司的生产工艺及流程如何？"}
    )
    capacity_and_bottlenecks: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前的产能情况如何？最大产能多少？目前限制产能主要的原因是什么？"}
    )
    production_equipment_and_risks: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司生产的主要设备有哪些？是自己研制的还是购买的？国产和国外的比例怎样？核心生产设备是否会存在海外限制或难以购买等情况？"}
    )
    product_yield_and_improvement: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "目前生产的产品良率如何？主要提升良率的办法是什么？"}
    )
class SupplyChainAndCustomerView(BaseModel):
    """## 6.原材料供应商及客户结构情况如何？ [id:supply_chain_and_customer]"""
    raw_material_inventory: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "原材料目前库存情况如何？"}
    )
    procurement_model_and_supplier_cooperation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "目前公司原材料采购模式是怎样的？和原材料供应商是如何合作的？"}
    )
    key_suppliers: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "原材目前最主要的供应商是哪些？"}
    )
    procurement_payment_terms: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "原材料采购是否有账期？账期的时间大概多久？"}
    )
    key_customers_and_concentration: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司主要客户是哪些？公司前五大客户是谁？前五大客户占收入占比分别是多少？"}
    )
    customer_payment_terms: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司客户的账期情况如何？前五大客户账期比重如何？"}
    )
    customer_payment_management_principle: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司对客户账期管理原则是什么？"}
    )
    top_customer_feedback: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "客户目前反馈的最多需求是什么？"}
    )
class BusinessStrategyAndPlanningView(BaseModel):
    """## 7.公司经营战略及未来规划如何？ [id:business_strategy_and_planning]"""
    future_direction_and_strategy: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司未来主要发展方向和战略是什么？基于什么样的考虑？"}
    )
    current_challenges_and_obstacles: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司实现未来发展战略眼下最需要解决的问题是什么？主要障碍是什么？"}
    )
@register_schema
class CompanyCoreBusinessView(BaseModel):
    __business_architecture__: str = """
# 五、公司核心业务情况如何？ [id:company_core_business]

## 1.公司主要业务模式是什么？ [id:business_model]

### 公司提供的主要业务服务是什么？ [id:main_business_services]
### 公司主要生产的产品是哪些？详细介绍一下公司产品和服务特点是什么？ [id:main_products_and_features]
### 公司每一样产品或服务占收入的比重是多少？ [id:product_revenue_breakdown]

## 2.公司盈利模式如何？ [id:profit_model]

### 详细说明公司具体是如何赚钱？ [id:profit_mechanism]

## 3.公司销售模式如何？（主要了解公司销售渠道，初步访谈简要了解；详细访谈深入了解） [id:sales_model]

### 产品（product）如何？ [id:product]

#### 产品的差异化优势是什么？ [id:differentiation_advantage]
#### 产品的品牌形象是什么？ [id:brand_image]
#### 产品主要针对的客户是什么？ [id:target_customers]
#### 消费者对产品的满意度如何？ [id:customer_satisfaction]
#### 产品的成本结构如何构成？ [id:cost_structure]
#### 产品的价格制定依据是什么？ [id:pricing_basis]
#### 竞争对手的定价依据是什么？ [id:competitor_pricing_basis]
#### 消费者或客户对目前价格的敏感程度如何？价格是否符合消费者或客户的预期？ [id:price_sensitivity_and_expectation]

### 渠道（place）如何？ [id:channel]

#### 产品的销售渠道目前有哪些？ [id:sales_channels]
#### 产品和销售渠道是如何分成的？ [id:channel_revenue_sharing]
#### 销售渠道覆盖范围和效率如何？ [id:channel_coverage_and_efficiency]
#### 公司自身的销售团队如何打造？ [id:sales_team_building]
#### 销售团队的激励政策是什么？对团队是否有正向的激励作用？ [id:sales_team_incentives]
#### 消费者的购买习惯是什么？ [id:customer_purchase_habits]

### 推广（promotion）如何？ [id:promotion]

#### 推广活动的目标受众群体是什么？ [id:promotion_target_audience]
#### 推广活动的策略是什么？主要考虑线上还是线下？ [id:promotion_strategy_and_channel]
#### 推广活动的投入产出比如何？ [id:promotion_roi]
#### 推广活动的效果评估如何？ [id:promotion_effectiveness_evaluation]

## 4.公司核心技术及优势是什么？ [id:core_tech_and_advantage]

### 公司核心技术以及核心竞争壁垒是什么？为什么竞争对手不能做出和公司一样的产品或服务？ [id:core_technology_and_barriers]
### 公司如何持续保证在这块的优势？ [id:sustainability_of_advantage]
### 公司的研发体系和战略是什么？ [id:rd_system_and_strategy]
### 公司研发团队情况如何？ [id:rd_team_status]
### 公司最新研发进展情况如何？ [id:latest_rd_progress]
### 公司近三年在研发方面投入的情况如何？未来在研发上面的投入计划如何？ [id:rd_investment_history_and_plan]
### 公司拥有的相关专利及资质情况如何？ [id:patents_and_qualifications]
### 公司相关资质和牌照申请的难度如何？（针对不同行业不同资质） [id:qualification_application_difficulty]

## 5.公司生产流程及工艺如何？（只分析制造类企业，服务类企业不询问） [id:production_process]

### 详细说明公司的生产工艺及流程如何？ [id:production_process_details]
### 公司目前的产能情况如何？最大产能多少？目前限制产能主要的原因是什么？ [id:capacity_and_bottlenecks]
### 公司生产的主要设备有哪些？是自己研制的还是购买的？国产和国外的比例怎样？核心生产设备是否会存在海外限制或难以购买等情况？ [id:production_equipment_and_risks]
### 目前生产的产品良率如何？主要提升良率的办法是什么？ [id:product_yield_and_improvement]

## 6.原材料供应商及客户结构情况如何？ [id:supply_chain_and_customer]

### 原材料目前库存情况如何？ [id:raw_material_inventory]
### 目前公司原材料采购模式是怎样的？和原材料供应商是如何合作的？ [id:procurement_model_and_supplier_cooperation]
### 原材目前最主要的供应商是哪些？ [id:key_suppliers]
### 原材料采购是否有账期？账期的时间大概多久？ [id:procurement_payment_terms]
### 公司主要客户是哪些？公司前五大客户是谁？前五大客户占收入占比分别是多少？ [id:key_customers_and_concentration]
### 公司客户的账期情况如何？前五大客户账期比重如何？ [id:customer_payment_terms]
### 公司对客户账期管理原则是什么？ [id:customer_payment_management_principle]
### 客户目前反馈的最多需求是什么？ [id:top_customer_feedback]

## 7.公司经营战略及未来规划如何？ [id:business_strategy_and_planning]

### 公司未来主要发展方向和战略是什么？基于什么样的考虑？ [id:future_direction_and_strategy]
### 公司实现未来发展战略眼下最需要解决的问题是什么？主要障碍是什么？ [id:current_challenges_and_obstacles]
""".strip()

    """# 五、公司核心业务情况如何？ [id:company_core_business]"""
    business_model: BusinessModelView = Field(
        default_factory=BusinessModelView,
        json_schema_extra={"markdown_title": "1.公司主要业务模式是什么？"}
    )
    profit_model: ProfitModelView = Field(
        default_factory=ProfitModelView,
        json_schema_extra={"markdown_title": "2.公司盈利模式如何？"}
    )
    sales_model: SalesModelView = Field(
        default_factory=SalesModelView,
        json_schema_extra={"markdown_title": "3.公司销售模式如何？（主要了解公司销售渠道，初步访谈简要了解；详细访谈深入了解）"}
    )
    core_tech_and_advantage: CoreTechAndAdvantageView = Field(
        default_factory=CoreTechAndAdvantageView,
        json_schema_extra={"markdown_title": "4.公司核心技术及优势是什么？"}
    )
    production_process: ProductionProcessView = Field(
        default_factory=ProductionProcessView,
        json_schema_extra={"markdown_title": "5.公司生产流程及工艺如何？（只分析制造类企业，服务类企业不询问）"}
    )
    supply_chain_and_customer: SupplyChainAndCustomerView = Field(
        default_factory=SupplyChainAndCustomerView,
        json_schema_extra={"markdown_title": "6.原材料供应商及客户结构情况如何？"}
    )
    business_strategy_and_planning: BusinessStrategyAndPlanningView = Field(
        default_factory=BusinessStrategyAndPlanningView,
        json_schema_extra={"markdown_title": "7.公司经营战略及未来规划如何？"}
    )