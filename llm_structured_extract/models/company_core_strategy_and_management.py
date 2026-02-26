# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class CoreStrategyAndMissionView(BaseModel):
    """## 1.公司的核心战略目标及使命是什么？ [id:core_strategy_and_mission]"""
    strategy_formulation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的战略目标和使命是基于什么制定的？"}
    )
    employee_alignment: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "普通员工是否认同公司的战略目标和使命？"}
    )
    communication_method: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的战略目标 and 使命是如何传达给普通员工的？"}
    )
class OrgSupportForStrategyView(BaseModel):
    """## 2.公司的组织架构是否支持公司的战略达成？ [id:org_support_for_strategy]"""
    structure_efficiency: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "组织架构中的各部门职责与分工是否清晰合理？"}
    )
    operational_efficiency: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "组织的运转效率如何？"}
    )
    leadership_competence: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "核心部门的领导是否胜任？"}
    )
class CollaborationAndConflictView(BaseModel):
    """## 3.如何保证人与人、人与部门、部门与部门之间的顺畅协同和沟通？ [id:collaboration_and_conflict]"""
    relationship_management: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "人与人、人与部门、部门与部门关系紧密程度如何？合作是否顺畅？"}
    )
    conflict_resolution_process: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "如果遇到冲突和问题如何解决？如何管理组织中的冲突？"}
    )
class BusinessSupportSystemView(BaseModel):
    """## 4.为了支持业务的顺利进行在有哪些方面的支持？ [id:business_support_system]"""
    hardware_support: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "支持业务顺利进行的硬件方面有哪些支持？"}
    )
    software_support: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "支持业务顺利进行的软件方面有哪些支持？"}
    )
    system_effectiveness: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "目前构建的系统是否能够有效的运行？"}
    )
    auxiliary_processes: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "辅助流程如审批、报销和汇报流程目前如何运行？"}
    )
class EmployeeIncentivePolicyView(BaseModel):
    """## 5.公司对员工的激励政策是什么？ [id:employee_incentive_policy]"""
    incentive_effectiveness: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的奖励和激励政策和员工的预期是否匹配？"}
    )
    target_reward_mechanism: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "每次确认业务目标时，是否有明确的奖励机制？"}
    )
    policy_impact: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的激励制度是否发挥了正向的作用？"}
    )
class LeadershipAndOperationsView(BaseModel):
    """## 6.公司领导如何保证企业整体的有效运作？ [id:leadership_and_operations]"""
    leadership_impact: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "领导的管理风格和领导风格是否对公司运营效率有正向帮助？"}
    )
    feedback_mechanism: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "领导对以上五个机制是否有完善的反馈机制？是否能够及时发现各个流程中问题和矛盾？"}
    )
    adjustment_capability: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "领导对以上五个流程是否有完整的调节方案和手段？"}
    )
@register_schema
class CompanyCoreStrategyAndManagementView(BaseModel):
    __business_architecture__: str = """
# 三、公司核心战略目标及管理情况如何？ [id:company_core_strategy_and_management]

## 1.公司的核心战略目标及使命是什么？ [id:core_strategy_and_mission]

### 公司的战略目标和使命是基于什么制定的？ [id:strategy_formulation]
### 普通员工是否认同公司的战略目标和使命？ [id:employee_alignment]
### 公司的战略目标 and 使命是如何传达给普通员工的？ [id:communication_method]

## 2.公司的组织架构是否支持公司的战略达成？ [id:org_support_for_strategy]

### 组织架构中的各部门职责与分工是否清晰合理？ [id:structure_efficiency]
### 组织的运转效率如何？ [id:operational_efficiency]
### 核心部门的领导是否胜任？ [id:leadership_competence]

## 3.如何保证人与人、人与部门、部门与部门之间的顺畅协同和沟通？ [id:collaboration_and_conflict]

### 人与人、人与部门、部门与部门关系紧密程度如何？合作是否顺畅？ [id:relationship_management]
### 如果遇到冲突和问题如何解决？如何管理组织中的冲突？ [id:conflict_resolution_process]

## 4.为了支持业务的顺利进行在有哪些方面的支持？ [id:business_support_system]

### 支持业务顺利进行的硬件方面有哪些支持？ [id:hardware_support]
### 支持业务顺利进行的软件方面有哪些支持？ [id:software_support]
### 目前构建的系统是否能够有效的运行？ [id:system_effectiveness]
### 辅助流程如审批、报销和汇报流程目前如何运行？ [id:auxiliary_processes]

## 5.公司对员工的激励政策是什么？ [id:employee_incentive_policy]

### 公司的奖励和激励政策和员工的预期是否匹配？ [id:incentive_effectiveness]
### 每次确认业务目标时，是否有明确的奖励机制？ [id:target_reward_mechanism]
### 公司的激励制度是否发挥了正向的作用？ [id:policy_impact]

## 6.公司领导如何保证企业整体的有效运作？ [id:leadership_and_operations]

### 领导的管理风格和领导风格是否对公司运营效率有正向帮助？ [id:leadership_impact]
### 领导对以上五个机制是否有完善的反馈机制？是否能够及时发现各个流程中问题和矛盾？ [id:feedback_mechanism]
### 领导对以上五个流程是否有完整的调节方案和手段？ [id:adjustment_capability]
""".strip()

    """# 三、公司核心战略目标及管理情况如何？ [id:company_core_strategy_and_management]"""
    core_strategy_and_mission: CoreStrategyAndMissionView = Field(
        default_factory=CoreStrategyAndMissionView,
        json_schema_extra={"markdown_title": "1.公司的核心战略目标及使命是什么？"}
    )
    org_support_for_strategy: OrgSupportForStrategyView = Field(
        default_factory=OrgSupportForStrategyView,
        json_schema_extra={"markdown_title": "2.公司的组织架构是否支持公司的战略达成？"}
    )
    collaboration_and_conflict: CollaborationAndConflictView = Field(
        default_factory=CollaborationAndConflictView,
        json_schema_extra={"markdown_title": "3.如何保证人与人、人与部门、部门与部门之间的顺畅协同和沟通？"}
    )
    business_support_system: BusinessSupportSystemView = Field(
        default_factory=BusinessSupportSystemView,
        json_schema_extra={"markdown_title": "4.为了支持业务的顺利进行在有哪些方面的支持？"}
    )
    employee_incentive_policy: EmployeeIncentivePolicyView = Field(
        default_factory=EmployeeIncentivePolicyView,
        json_schema_extra={"markdown_title": "5.公司对员工的激励政策是什么？"}
    )
    leadership_and_operations: LeadershipAndOperationsView = Field(
        default_factory=LeadershipAndOperationsView,
        json_schema_extra={"markdown_title": "6.公司领导如何保证企业整体的有效运作？"}
    )