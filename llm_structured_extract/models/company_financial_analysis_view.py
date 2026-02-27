# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class AssetStructureSubView(BaseModel):
    """##### 资产结构如何？（分析固定资产和无形资产是否过高） [id:asset_structure]"""
    exit_barrier: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "退出壁垒如何？（固定资产和无形资产高，企业自由选择权小）"}
    )
    operational_risk: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "经营风险如何？（固定资产和无形资产高，企业经营风险大）"}
    )
class CashContentSubView(BaseModel):
    """##### 现金含量如何？（分析现金在资产比例中的高低） [id:cash_content]"""
    financial_flexibility: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "财务弹性如何？（现金含量越大，财务弹性越大）"}
    )
    potential_loss: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "潜在损失如何？（现金含量越大，潜在损失风险越低）"}
    )
class AssetQualitySubView(BaseModel):
    """### 资产质量如何？ [id:asset_quality]"""
    asset_structure: AssetStructureSubView = Field(
        default_factory=AssetStructureSubView,
        json_schema_extra={"markdown_title": "资产结构如何？（分析固定资产和无形资产是否过高）"}
    )
    cash_content: CashContentSubView = Field(
        default_factory=CashContentSubView,
        json_schema_extra={"markdown_title": "现金含量如何？（分析现金在资产比例中的高低）"}
    )
class AssetCommonSizeAnalysisSubView(BaseModel):
    """### 资产共同比分析 [id:asset_common_size_analysis]"""
    anomalies: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "资产负债表中异常项是什么？单项占比特别高的原因？什么原因造成的单项比例异常？"}
    )
    debt_to_asset_ratio: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司负债率多少？短期负债和长期负债情况？"}
    )
    net_assets: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司净资产情况如何？"}
    )
    annual_interest_cost: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司每年利息成本多少？"}
    )
    accounts_receivable: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司应收账款情况如何？账期情况？"}
    )
    prepaid_accounts: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司预付账款情况如何？"}
    )
    accounts_payable: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司应付账款情况如何？是否有账期？"}
    )
    cash_on_hand: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司账面现金有多少？"}
    )
    inventory: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司存货情况如何？"}
    )
    goodwill: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司商誉情况如何？"}
    )
    fixed_assets: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司固定资产情况如何？"}
    )
class AssetTrendAnalysisSubView(BaseModel):
    """### 资产趋势分析 [id:asset_trend_analysis]"""
    historical_comparison: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "同一个企业不同时期的报表情况如何？"}
    )
class AssetComparativeAnalysisSubView(BaseModel):
    """### 资产对比分析 [id:asset_comparative_analysis]"""
    industry_benchmark: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "对比同行业企业数据情况如何？"}
    )
class SolvencySubView(BaseModel):
    """##### 偿债能力情况如何？ [id:solvency]"""
    short_term_solvency: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "短期偿债能力"}
    )
    long_term_solvency: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "长期偿债能力"}
    )
class OperationalCapabilitySubView(BaseModel):
    """##### 运营能力情况如何？ [id:operational_capability]"""
    ar_turnover: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "应收账款周转率及天数"}
    )
    inventory_turnover: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "存货周转率及天数"}
    )
    fa_turnover: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "固定资产周转率及天数"}
    )
    ta_turnover: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "总资产周转率及天数"}
    )
class AssetRatioAnalysisSubView(BaseModel):
    """### 资产比例分析 [id:asset_ratio_analysis]"""
    solvency: SolvencySubView = Field(
        default_factory=SolvencySubView,
        json_schema_extra={"markdown_title": "偿债能力情况如何？"}
    )
    operational_capability: OperationalCapabilitySubView = Field(
        default_factory=OperationalCapabilitySubView,
        json_schema_extra={"markdown_title": "运营能力情况如何？"}
    )
    equity_multiplier: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司权益乘数情况如何？"}
    )
class BalanceSheetAnalysisView(BaseModel):
    """## 资产负债表分析 [id:balance_sheet_analysis]"""
    quick_analysis: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "快速分析"}
    )
    asset_quality: AssetQualitySubView = Field(
        default_factory=AssetQualitySubView,
        json_schema_extra={"markdown_title": "资产质量如何？"}
    )
    detailed_analysis: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "详细分析"}
    )
    asset_common_size_analysis: AssetCommonSizeAnalysisSubView = Field(
        default_factory=AssetCommonSizeAnalysisSubView,
        json_schema_extra={"markdown_title": "资产共同比分析"}
    )
    asset_trend_analysis: AssetTrendAnalysisSubView = Field(
        default_factory=AssetTrendAnalysisSubView,
        json_schema_extra={"markdown_title": "资产趋势分析"}
    )
    asset_comparative_analysis: AssetComparativeAnalysisSubView = Field(
        default_factory=AssetComparativeAnalysisSubView,
        json_schema_extra={"markdown_title": "资产对比分析"}
    )
    asset_ratio_analysis: AssetRatioAnalysisSubView = Field(
        default_factory=AssetRatioAnalysisSubView,
        json_schema_extra={"markdown_title": "资产比例分析"}
    )
class RevenueQualitySubView(BaseModel):
    """##### 收入质量如何？ [id:revenue_quality]"""
    revenue_growth: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "成长性如何？（营业收入是否稳定增长）"}
    )
    revenue_volatility: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "波动性如何？（营业收入是否大范围波动）"}
    )
class NetProfitQualitySubView(BaseModel):
    """##### 利润质量如何？ [id:net_profit_quality]"""
    profit_growth: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "成长性如何？（净利润是否稳定增长）"}
    )
    profit_volatility: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "波动性如何？（净利润是否大范围波动）"}
    )
class GrossMarginQualitySubView(BaseModel):
    """##### 毛利率如何？ [id:gross_margin_quality]"""
    rd_investment_space: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "研发投入空间如何？（高毛利是否投入研发）"}
    )
    marketing_investment_space: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "营销投入空间如何？（高毛利是否投入营销）"}
    )
class ProfitQualitySubView(BaseModel):
    """### 盈利质量如何？ [id:profit_quality]"""
    revenue_quality: RevenueQualitySubView = Field(
        default_factory=RevenueQualitySubView,
        json_schema_extra={"markdown_title": "收入质量如何？"}
    )
    net_profit_quality: NetProfitQualitySubView = Field(
        default_factory=NetProfitQualitySubView,
        json_schema_extra={"markdown_title": "利润质量如何？"}
    )
    gross_margin_quality: GrossMarginQualitySubView = Field(
        default_factory=GrossMarginQualitySubView,
        json_schema_extra={"markdown_title": "毛利率如何？"}
    )
class AnnualRevenueSubView(BaseModel):
    """##### 公司目前年营收多少？ [id:annual_revenue]"""
    revenue_growth_3y: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "近三年年营收增长情况如何？"}
    )
    product_revenue_mix: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "主要产品占营收比重情况如何？"}
    )
    revenue_forecast: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "今年/明年公司营收预计多少？"}
    )
class NetProfitSubView(BaseModel):
    """##### 公司目前净利润情况如何？ [id:net_profit]"""
    profit_growth_3y: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司近三年净利润增长情况如何？"}
    )
    profit_forecast: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "今年/明年公司净利润预计多少？"}
    )
class IncomeCommonSizeAnalysisSubView(BaseModel):
    """### 利润表共同比分析 [id:income_common_size_analysis]"""
    income_anomalies: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "利润表中异常项是什么？单项占比特别高的原因？"}
    )
    sales_expenses: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司销售费用情况如何？"}
    )
    management_costs: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司管理成本情况如何？"}
    )
    rd_expenses: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司研发费用情况如何？"}
    )
    financial_expenses: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司财务费用情况如何？"}
    )
    annual_revenue: AnnualRevenueSubView = Field(
        default_factory=AnnualRevenueSubView,
        json_schema_extra={"markdown_title": "公司目前年营收多少？"}
    )
    gross_margin: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司毛利率情况如何？"}
    )
    top_cost_item: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司成本中占比最高的科目是什么？"}
    )
    net_profit: NetProfitSubView = Field(
        default_factory=NetProfitSubView,
        json_schema_extra={"markdown_title": "公司目前净利润情况如何？"}
    )
    government_subsidies: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前是否有政府或其他补助收入？"}
    )
    tax_rate: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前税率情况如何？"}
    )
class IncomeTrendAnalysisSubView(BaseModel):
    """### 利润表趋势分析 [id:income_trend_analysis]"""
    income_historical_comparison: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "同一个企业不同时期的报表情况如何？"}
    )
class IncomeComparativeAnalysisSubView(BaseModel):
    """### 利润表对比分析 [id:income_comparative_analysis]"""
    income_industry_benchmark: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "对比同行业企业数据情况如何？"}
    )
class IncomeRatioAnalysisSubView(BaseModel):
    """### 利润表比例分析 [id:income_ratio_analysis]"""
    profitability: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "盈利能力情况如何？"}
    )
    main_gross_margin: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司主营业务毛利率情况如何？"}
    )
    net_margin: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司净利率情况如何？"}
    )
    roa: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司总资产收益率情况如何？（ROA)"}
    )
    roe: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司净资产收益率情况如何？（ROE)"}
    )
    profit_to_cash_ratio: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "净利润现金比例情况如何？"}
    )
class GrowthCapabilitySubView(BaseModel):
    """### 发展能力情况如何？ [id:growth_capability]"""
    revenue_growth_rate: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "营业收入增长率如何？"}
    )
    asset_growth_rate: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "总资产增长率如何？"}
    )
class IncomeStatementAnalysisView(BaseModel):
    """## 利润表分析 [id:income_statement_analysis]"""
    quick_analysis_income: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "快速分析"}
    )
    profit_quality: ProfitQualitySubView = Field(
        default_factory=ProfitQualitySubView,
        json_schema_extra={"markdown_title": "盈利质量如何？"}
    )
    detailed_analysis_income: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "详细分析"}
    )
    income_common_size_analysis: IncomeCommonSizeAnalysisSubView = Field(
        default_factory=IncomeCommonSizeAnalysisSubView,
        json_schema_extra={"markdown_title": "利润表共同比分析"}
    )
    income_trend_analysis: IncomeTrendAnalysisSubView = Field(
        default_factory=IncomeTrendAnalysisSubView,
        json_schema_extra={"markdown_title": "利润表趋势分析"}
    )
    income_comparative_analysis: IncomeComparativeAnalysisSubView = Field(
        default_factory=IncomeComparativeAnalysisSubView,
        json_schema_extra={"markdown_title": "利润表对比分析"}
    )
    income_ratio_analysis: IncomeRatioAnalysisSubView = Field(
        default_factory=IncomeRatioAnalysisSubView,
        json_schema_extra={"markdown_title": "利润表比例分析"}
    )
    growth_capability: GrowthCapabilitySubView = Field(
        default_factory=GrowthCapabilitySubView,
        json_schema_extra={"markdown_title": "发展能力情况如何？"}
    )
class OperatingCashFlowStatusSubView(BaseModel):
    """##### 经营性现金流如何？ [id:operating_cash_flow_status]"""
    cash_generation_capability: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "造血功能如何？"}
    )
    ar_collection_quality: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "销售回款质量如何？"}
    )
class FreeCashFlowStatusSubView(BaseModel):
    """##### 自由现金流如何？ [id:free_cash_flow_status]"""
    debt_dividend_servicing: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "还本付息和股利支付能力如何？"}
    )
class CashFlowStatusSubView(BaseModel):
    """### 现金流量如何？ [id:cash_flow_status]"""
    operating_cash_flow_status: OperatingCashFlowStatusSubView = Field(
        default_factory=OperatingCashFlowStatusSubView,
        json_schema_extra={"markdown_title": "经营性现金流如何？"}
    )
    free_cash_flow_status: FreeCashFlowStatusSubView = Field(
        default_factory=FreeCashFlowStatusSubView,
        json_schema_extra={"markdown_title": "自由现金流如何？"}
    )
class CashFlowStatementAnalysisView(BaseModel):
    """## 现金流量表分析 [id:cash_flow_statement_analysis]"""
    quick_analysis_cash: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "快速分析"}
    )
    cash_flow_status: CashFlowStatusSubView = Field(
        default_factory=CashFlowStatusSubView,
        json_schema_extra={"markdown_title": "现金流量如何？"}
    )
    detailed_analysis_cash: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "详细分析"}
    )
    operating_cash_flow_net: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "经营活动现金流量净额是正的吗？"}
    )
    investing_cash_flow_net: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "投资活动现金流量净额多少？"}
    )
    financing_cash_flow_net: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "筹资活动现金流量净额多少？"}
    )
@register_schema
class CompanyFinancialAnalysisView(BaseModel):
    __business_architecture__: str = """
# 公司财务 [id:company_financial_analysis]

## 资产负债表分析 [id:balance_sheet_analysis]

### 快速分析 [id:quick_analysis]

### 资产质量如何？ [id:asset_quality]

##### 资产结构如何？（分析固定资产和无形资产是否过高） [id:asset_structure]

###### 退出壁垒如何？（固定资产和无形资产高，企业自由选择权小） [id:exit_barrier]
###### 经营风险如何？（固定资产和无形资产高，企业经营风险大） [id:operational_risk]

##### 现金含量如何？（分析现金在资产比例中的高低） [id:cash_content]

###### 财务弹性如何？（现金含量越大，财务弹性越大） [id:financial_flexibility]
###### 潜在损失如何？（现金含量越大，潜在损失风险越低） [id:potential_loss]

### 详细分析 [id:detailed_analysis]

### 资产共同比分析 [id:asset_common_size_analysis]

##### 资产负债表中异常项是什么？单项占比特别高的原因？什么原因造成的单项比例异常？ [id:anomalies]
##### 公司负债率多少？短期负债和长期负债情况？ [id:debt_to_asset_ratio]
##### 公司净资产情况如何？ [id:net_assets]
##### 公司每年利息成本多少？ [id:annual_interest_cost]
##### 公司应收账款情况如何？账期情况？ [id:accounts_receivable]
##### 公司预付账款情况如何？ [id:prepaid_accounts]
##### 公司应付账款情况如何？是否有账期？ [id:accounts_payable]
##### 公司账面现金有多少？ [id:cash_on_hand]
##### 公司存货情况如何？ [id:inventory]
##### 公司商誉情况如何？ [id:goodwill]
##### 公司固定资产情况如何？ [id:fixed_assets]

### 资产趋势分析 [id:asset_trend_analysis]

##### 同一个企业不同时期的报表情况如何？ [id:historical_comparison]

### 资产对比分析 [id:asset_comparative_analysis]

##### 对比同行业企业数据情况如何？ [id:industry_benchmark]

### 资产比例分析 [id:asset_ratio_analysis]

##### 偿债能力情况如何？ [id:solvency]

###### 短期偿债能力 [id:short_term_solvency]
###### 长期偿债能力 [id:long_term_solvency]

##### 运营能力情况如何？ [id:operational_capability]

###### 应收账款周转率及天数 [id:ar_turnover]
###### 存货周转率及天数 [id:inventory_turnover]
###### 固定资产周转率及天数 [id:fa_turnover]
###### 总资产周转率及天数 [id:ta_turnover]

##### 公司权益乘数情况如何？ [id:equity_multiplier]

## 利润表分析 [id:income_statement_analysis]

### 快速分析 [id:quick_analysis_income]

### 盈利质量如何？ [id:profit_quality]

##### 收入质量如何？ [id:revenue_quality]

###### 成长性如何？（营业收入是否稳定增长） [id:revenue_growth]
###### 波动性如何？（营业收入是否大范围波动） [id:revenue_volatility]

##### 利润质量如何？ [id:net_profit_quality]

###### 成长性如何？（净利润是否稳定增长） [id:profit_growth]
###### 波动性如何？（净利润是否大范围波动） [id:profit_volatility]

##### 毛利率如何？ [id:gross_margin_quality]

###### 研发投入空间如何？（高毛利是否投入研发） [id:rd_investment_space]
###### 营销投入空间如何？（高毛利是否投入营销） [id:marketing_investment_space]

### 详细分析 [id:detailed_analysis_income]

### 利润表共同比分析 [id:income_common_size_analysis]

##### 利润表中异常项是什么？单项占比特别高的原因？ [id:income_anomalies]
##### 公司销售费用情况如何？ [id:sales_expenses]
##### 公司管理成本情况如何？ [id:management_costs]
##### 公司研发费用情况如何？ [id:rd_expenses]
##### 公司财务费用情况如何？ [id:financial_expenses]
##### 公司目前年营收多少？ [id:annual_revenue]

###### 近三年年营收增长情况如何？ [id:revenue_growth_3y]
###### 主要产品占营收比重情况如何？ [id:product_revenue_mix]
###### 今年/明年公司营收预计多少？ [id:revenue_forecast]

##### 公司毛利率情况如何？ [id:gross_margin]
##### 公司成本中占比最高的科目是什么？ [id:top_cost_item]
##### 公司目前净利润情况如何？ [id:net_profit]

###### 公司近三年净利润增长情况如何？ [id:profit_growth_3y]
###### 今年/明年公司净利润预计多少？ [id:profit_forecast]

##### 公司目前是否有政府或其他补助收入？ [id:government_subsidies]
##### 公司目前税率情况如何？ [id:tax_rate]

### 利润表趋势分析 [id:income_trend_analysis]

##### 同一个企业不同时期的报表情况如何？ [id:income_historical_comparison]

### 利润表对比分析 [id:income_comparative_analysis]

##### 对比同行业企业数据情况如何？ [id:income_industry_benchmark]

### 利润表比例分析 [id:income_ratio_analysis]

##### 盈利能力情况如何？ [id:profitability]
##### 公司主营业务毛利率情况如何？ [id:main_gross_margin]
##### 公司净利率情况如何？ [id:net_margin]
##### 公司总资产收益率情况如何？（ROA) [id:roa]
##### 公司净资产收益率情况如何？（ROE) [id:roe]
##### 净利润现金比例情况如何？ [id:profit_to_cash_ratio]

### 发展能力情况如何？ [id:growth_capability]

##### 营业收入增长率如何？ [id:revenue_growth_rate]
##### 总资产增长率如何？ [id:asset_growth_rate]

## 现金流量表分析 [id:cash_flow_statement_analysis]

### 快速分析 [id:quick_analysis_cash]

### 现金流量如何？ [id:cash_flow_status]

##### 经营性现金流如何？ [id:operating_cash_flow_status]

###### 造血功能如何？ [id:cash_generation_capability]
###### 销售回款质量如何？ [id:ar_collection_quality]

##### 自由现金流如何？ [id:free_cash_flow_status]

###### 还本付息和股利支付能力如何？ [id:debt_dividend_servicing]

### 详细分析 [id:detailed_analysis_cash]

### 经营活动现金流量净额是正的吗？ [id:operating_cash_flow_net]
### 投资活动现金流量净额多少？ [id:investing_cash_flow_net]
### 筹资活动现金流量净额多少？ [id:financing_cash_flow_net]
""".strip()

    """# 公司财务 [id:company_financial_analysis]"""
    balance_sheet_analysis: BalanceSheetAnalysisView = Field(
        default_factory=BalanceSheetAnalysisView,
        json_schema_extra={"markdown_title": "资产负债表分析"}
    )
    income_statement_analysis: IncomeStatementAnalysisView = Field(
        default_factory=IncomeStatementAnalysisView,
        json_schema_extra={"markdown_title": "利润表分析"}
    )
    cash_flow_statement_analysis: CashFlowStatementAnalysisView = Field(
        default_factory=CashFlowStatementAnalysisView,
        json_schema_extra={"markdown_title": "现金流量表分析"}
    )