# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class RiskCheckView(BaseModel):
    """## 1.公司基本公司情况如何？（风险核查） [id:risk_check]"""
    legal_litigations: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司近期有无法律诉讼？"}
    )
    business_anomalies: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司近期有无经营异常情况？"}
    )
    penalties: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司近期是否受到过处罚？"}
    )
    equity_freezes: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司有无股权冻结情况？"}
    )
    controller_equity_freezes: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "实控人或重要股份有无股权冻结情况？"}
    )
class EquityStructureView(BaseModel):
    """## 2.公司股权架构情况如何？（主要了解实控人及其他股东持股情况） [id:equity_structure]"""
    controller_ratio: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司实控人占股比情况？"}
    )
    founder_team_ratio: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司其他创始人及团队占股比情况？"}
    )
    major_shareholders_ratio: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司主要股东和投资人持股比列情况？"}
    )
    concert_parties: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前实控人的一致行动人情况？"}
    )
class HistoricalMilestonesView(BaseModel):
    """## 3.公司历史沿革情况如何？ [id:historical_milestones]"""
    major_events: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司成立以来主要的事件有哪些？"}
    )
    financing_events: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司主要的融资事件有哪些？投资金额多少？估值多少进入？"}
    )
class OrgStructureView(BaseModel):
    """## 4.公司组织架构如何？ [id:org_structure]"""
    department_structure: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前各部门组织架构是如何设计的？"}
    )
    business_alignment: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的组织架构是否有针对公司业务特别设计？"}
    )
class SubsidiariesSubView(BaseModel):
    """### 公司目前子公司/分公司情况？ [id:subsidiaries]"""
    purpose: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "之前设立子公司/分公司的主要目的是什么？"}
    )
    business: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "子公司/分公司的业务分别是什么？"}
    )
    management_details: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "子公司/分公司是如何管理的？团队规模多大？营收情况如何？"}
    )
class RelatedCompaniesSubView(BaseModel):
    """### 实控人是否有关联公司？ [id:related_companies]"""
    business_scope: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "实控人关联公司主要的业务是什么？"}
    )
    competition_relation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "关联公司是否存在和目前这家公司存在同业竞争或业务相互关联的问题？"}
    )
class SubsidiariesAndAffiliatesView(BaseModel):
    """## 5.公司子公司及实控人关联公司情况如何？ [id:subsidiaries_and_affiliates]"""
    subsidiaries: SubsidiariesSubView = Field(
        default_factory=SubsidiariesSubView,
        json_schema_extra={"markdown_title": "公司目前子公司/分公司情况？"}
    )
    related_companies: RelatedCompaniesSubView = Field(
        default_factory=RelatedCompaniesSubView,
        json_schema_extra={"markdown_title": "实控人是否有关联公司？"}
    )
class BoardInfoView(BaseModel):
    """## 6.公司董事会成员情况如何？ [id:board_info]"""
    composition: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司董事会如何构成？目前关系是否融洽？"}
    )
    member_count: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司董事会成员目前多少位？"}
    )
    voting_power: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "实控人及一致行动人在董事会的投票权情况如何？"}
    )
class HrConfigurationView(BaseModel):
    """## 7.公司人力资源情况如何？ [id:hr_configuration]"""
    total_employees: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前总人数是多少？"}
    )
    rd_team: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前研发人员多少？学历构成比例情况如何？"}
    )
    sales_team: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司销售团队人员多少？如何配置销售团队人员？"}
    )
@register_schema
class CompanyBasicView(BaseModel):
    __business_architecture__: str = """
# 一、公司基本概况如何？ [id:company_basic]

## 1.公司基本公司情况如何？（风险核查） [id:risk_check]

### 公司近期有无法律诉讼？ [id:legal_litigations]
### 公司近期有无经营异常情况？ [id:business_anomalies]
### 公司近期是否受到过处罚？ [id:penalties]
### 公司有无股权冻结情况？ [id:equity_freezes]
### 实控人或重要股份有无股权冻结情况？ [id:controller_equity_freezes]

## 2.公司股权架构情况如何？（主要了解实控人及其他股东持股情况） [id:equity_structure]

### 公司实控人占股比情况？ [id:controller_ratio]
### 公司其他创始人及团队占股比情况？ [id:founder_team_ratio]
### 公司主要股东和投资人持股比列情况？ [id:major_shareholders_ratio]
### 公司目前实控人的一致行动人情况？ [id:concert_parties]

## 3.公司历史沿革情况如何？ [id:historical_milestones]

### 公司成立以来主要的事件有哪些？ [id:major_events]
### 公司主要的融资事件有哪些？投资金额多少？估值多少进入？ [id:financing_events]

## 4.公司组织架构如何？ [id:org_structure]

### 公司目前各部门组织架构是如何设计的？ [id:department_structure]
### 公司的组织架构是否有针对公司业务特别设计？ [id:business_alignment]

## 5.公司子公司及实控人关联公司情况如何？ [id:subsidiaries_and_affiliates]

### 公司目前子公司/分公司情况？ [id:subsidiaries]

#### 之前设立子公司/分公司的主要目的是什么？ [id:purpose]
#### 子公司/分公司的业务分别是什么？ [id:business]
#### 子公司/分公司是如何管理的？团队规模多大？营收情况如何？ [id:management_details]

### 实控人是否有关联公司？ [id:related_companies]

#### 实控人关联公司主要的业务是什么？ [id:business_scope]
#### 关联公司是否存在和目前这家公司存在同业竞争或业务相互关联的问题？ [id:competition_relation]

## 6.公司董事会成员情况如何？ [id:board_info]

### 公司董事会如何构成？目前关系是否融洽？ [id:composition]
### 公司董事会成员目前多少位？ [id:member_count]
### 实控人及一致行动人在董事会的投票权情况如何？ [id:voting_power]

## 7.公司人力资源情况如何？ [id:hr_configuration]

### 公司目前总人数是多少？ [id:total_employees]
### 公司目前研发人员多少？学历构成比例情况如何？ [id:rd_team]
### 公司销售团队人员多少？如何配置销售团队人员？ [id:sales_team]
""".strip()

    """# 一、公司基本概况如何？ [id:company_basic]"""
    risk_check: RiskCheckView = Field(
        default_factory=RiskCheckView,
        json_schema_extra={"markdown_title": "1.公司基本公司情况如何？（风险核查）"}
    )
    equity_structure: EquityStructureView = Field(
        default_factory=EquityStructureView,
        json_schema_extra={"markdown_title": "2.公司股权架构情况如何？（主要了解实控人及其他股东持股情况）"}
    )
    historical_milestones: HistoricalMilestonesView = Field(
        default_factory=HistoricalMilestonesView,
        json_schema_extra={"markdown_title": "3.公司历史沿革情况如何？"}
    )
    org_structure: OrgStructureView = Field(
        default_factory=OrgStructureView,
        json_schema_extra={"markdown_title": "4.公司组织架构如何？"}
    )
    subsidiaries_and_affiliates: SubsidiariesAndAffiliatesView = Field(
        default_factory=SubsidiariesAndAffiliatesView,
        json_schema_extra={"markdown_title": "5.公司子公司及实控人关联公司情况如何？"}
    )
    board_info: BoardInfoView = Field(
        default_factory=BoardInfoView,
        json_schema_extra={"markdown_title": "6.公司董事会成员情况如何？"}
    )
    hr_configuration: HrConfigurationView = Field(
        default_factory=HrConfigurationView,
        json_schema_extra={"markdown_title": "7.公司人力资源情况如何？"}
    )