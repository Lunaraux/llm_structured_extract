# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel, Field
from llm_structured_extract.core.schema_registry import register_schema


class TeamRecognitionSubView(BaseModel):
    """### 公司团队对公司的长期愿景和价值观是否有统一的认识和认同？ [id:team_recognition]"""
    awareness_and_endorsement: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司从上到下是否都充分了解公司的价值观和愿景？是否都十分认可公司的价值观和愿景？"}
    )
class VisionAndValuesView(BaseModel):
    """## 1. 公司是否具有清晰且共享的愿景及价值观？ [id:vision_and_values]"""
    team_recognition: TeamRecognitionSubView = Field(
        default_factory=TeamRecognitionSubView,
        json_schema_extra={"markdown_title": "公司团队对公司的长期愿景和价值观是否有统一的认识和认同？"}
    )
class TeamStructureAndCollaborationView(BaseModel):
    """## 2. 团队构成是否完整？（主要了解团队是否完整，相互之间是否互补） [id:team_structure_and_collaboration]"""
    team_completeness: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "团队技能是否互补？（团队成员是否覆盖产品、销售和综合管理等岗位？是否技能相互互补？）"}
    )
    industry_experience: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "团队行业经验是否足够？（创始人及核心团队成员是否拥有相关行业深入知识和经验？是否深刻理解市场？是否拥有较为广泛的人脉资源？）"}
    )
    role_clarity: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "团队成员间是否有明确的分工？协作是否顺畅？管理结构是否高效？"}
    )
class TeamCollaborationSubView(BaseModel):
    """### 公司团队关系及协作是否融洽？ [id:team_collaboration]"""
    prior_collaboration: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "团队成员是否在创业之前有过协作经历？"}
    )
    current_relationship: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "目前团队成员之间关系是否融洽？沟通是否顺畅？"}
    )
class TechnicalProductCapabilitySubView(BaseModel):
    """### 创始人及核心团队成员技术水平和产品打造能力如何？ [id:technical_product_capability]"""
    core_technical_skills: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员具备哪些核心技术能力？"}
    )
    zero_to_one_experience: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "是否有过从0到1构建产品的经历？"}
    )
class BusinessCapabilitySubView(BaseModel):
    """### 创始人及核心团队成员商业能力如何？ [id:business_capability]"""
    marketing_sales_exp: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员是否有过市场营销和销售的经历？"}
    )
    financing_exp: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员是否有过项目融资经历？"}
    )
    bd_negotiation_exp: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员是否有过商务拓展及合作谈判能力？"}
    )
class LeadershipManagementSubView(BaseModel):
    """### 创始人及核心团队成员管理能力如何？ [id:leadership_management]"""
    team_size_led: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员领导过多少人的团队？"}
    )
    motivation_approach: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员如何激励团队？"}
    )
    conflict_resolution: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队成员如何处理矛盾和冲突？"}
    )
class CoreQualitiesSubView(BaseModel):
    """### 创始人及核心团队核心品质如何？ [id:core_qualities]"""
    diligence: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "勤奋：团队是否总比别人要拼？"}
    )
    cost_efficiency: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "借鉴降本：压低各类费用开支产品成本，费用是否总比别人更省？"}
    )
    steadiness: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "稳健踏实：业务决策基本不出大错，是否步伐总比别人要稳健，诚实做人，踏实做事？"}
    )
    innovation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创新开拓：守正出奇，是否总是能持续研发新技术和新产品、在营销和管理等全方面都有创新？"}
    )
    standardized_management: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "规范管理：公司是否在财务、考勤、内控、人力、等多方面有完善和规范的制度？"}
    )
    resource_integration: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "整合发展：整合资源、借力发展、是否懂得整合资源和合作共赢？"}
    )
    self_improvement: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "修行修心：团队是否在创业过程中不断提升自己，并帮助别人？是否能做到说事不讲假话，做事不谋私利，同事不搞是非？"}
    )
class CoreCompetenciesView(BaseModel):
    """## 3. 创始人及核心团队综合能力情况如何？ [id:core_competencies]"""
    team_collaboration: TeamCollaborationSubView = Field(
        default_factory=TeamCollaborationSubView,
        json_schema_extra={"markdown_title": "公司团队关系及协作是否融洽？"}
    )
    technical_product_capability: TechnicalProductCapabilitySubView = Field(
        default_factory=TechnicalProductCapabilitySubView,
        json_schema_extra={"markdown_title": "创始人及核心团队成员技术水平和产品打造能力如何？"}
    )
    business_capability: BusinessCapabilitySubView = Field(
        default_factory=BusinessCapabilitySubView,
        json_schema_extra={"markdown_title": "创始人及核心团队成员商业能力如何？"}
    )
    leadership_management: LeadershipManagementSubView = Field(
        default_factory=LeadershipManagementSubView,
        json_schema_extra={"markdown_title": "创始人及核心团队成员管理能力如何？"}
    )
    core_qualities: CoreQualitiesSubView = Field(
        default_factory=CoreQualitiesSubView,
        json_schema_extra={"markdown_title": "创始人及核心团队核心品质如何？"}
    )
class FounderMarketFitView(BaseModel):
    """## 4. 创始人和市场契合情况如何？ [id:founder_market_fit]"""
    market_selection_reason: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人为什么选择了这个市场？"}
    )
    problem_insight: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人是否对目标用户面临的问题有切身体会或深刻洞察？"}
    )
    customer_centric: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人能否真正站在客户角度思考？"}
    )
    vision_alignment: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人的愿景是否与市场未来的发展方向一致？"}
    )
    passion_level: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人是否对所做的事情充满持久的热情，甚至到了痴迷的程度？"}
    )
    adaptability: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人是否能够根据市场变化调整策略？"}
    )
    cultural_fit: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人的个性和行事风格是否能融入目标市场的文化并建立连接？"}
    )
    unique_advantage: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人在这个市场具备何种独特的优势?"}
    )
class CeoFitSubView(BaseModel):
    """### 创始人的工作背景和经历如何？是否能够支持他担任公司CEO职位？ [id:ceo_fit]"""
    management_capability: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "主要的工作经历是否能够有足够能力管理好这家公司？"}
    )
class FourHighsSubView(BaseModel):
    """### 创始人四高如何？情商是否高？财商是否高？逆商是否高？智商是否高？ [id:four_highs]"""
    failure_experience: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人是否有重大失败过往？以前如何面对失败？对将来可能面临的失败如何看待？"}
    )
    eq_and_communication: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人和人沟通说话是否让人感觉舒服？是否能协调团队间的矛盾？"}
    )
    education_and_learning: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人学历情况如何？对新事物接纳能力如何？"}
    )
    money_mindset: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人对钱认知？过往是否赚过大钱？"}
    )
class TeamCharacterSubView(BaseModel):
    """### 创始人及核心团队四项品格如何？（诚信、大气、狼性、学习） [id:team_character]"""
    continuous_learning: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队如何保持持续学习能力？公司是否有相应机制保证团队成员不断学习？"}
    )
    integrity: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人是否说话算话，诚信靠谱？"}
    )
    competitiveness: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队是否有战斗力？是否有不断追求行业领先的动力和想法？"}
    )
    magnanimity: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人是否斤斤计较？是否在工作中抓大放小？"}
    )
class CognitiveJudgmentSubView(BaseModel):
    """### 创始人认知水平和对问题本质的判断能力如何？ [id:cognitive_judgment]"""
    founding_logic: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及团队决定创立这家公司的核心逻辑是什么？基于什么判断？最本质的逻辑是什么？"}
    )
    industry_trend: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "核心创始人对公司所处行业未来发展趋势的判断是什么？基于什么逻辑得出该判断？"}
    )
    decision_methodology: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人之前做过哪些重大决策和项目？但是决策的逻辑和方法是什么？"}
    )
    ultimate_vision: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人对这家公司最终的愿景是什么？"}
    )
    market_evaluation: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "创始人及核心团队如何评估市场？如发现市场发生变化如何快速调整和适应？"}
    )
class FounderPersonalTraitsView(BaseModel):
    """## 5. 创始人核心品质如何？ [id:founder_personal_traits]"""
    ceo_fit: CeoFitSubView = Field(
        default_factory=CeoFitSubView,
        json_schema_extra={"markdown_title": "创始人的工作背景和经历如何？是否能够支持他担任公司CEO职位？"}
    )
    four_highs: FourHighsSubView = Field(
        default_factory=FourHighsSubView,
        json_schema_extra={"markdown_title": "创始人四高如何？情商是否高？财商是否高？逆商是否高？智商是否高？"}
    )
    team_character: TeamCharacterSubView = Field(
        default_factory=TeamCharacterSubView,
        json_schema_extra={"markdown_title": "创始人及核心团队四项品格如何？（诚信、大气、狼性、学习）"}
    )
    cognitive_judgment: CognitiveJudgmentSubView = Field(
        default_factory=CognitiveJudgmentSubView,
        json_schema_extra={"markdown_title": "创始人认知水平和对问题本质的判断能力如何？"}
    )
class EquityIncentiveSubView(BaseModel):
    """### 创始团队间股权和利益分配机制如何？是否合理？是否满足创始团队间的预期？公司的核心激励策略是否能真正激励大家？ [id:equity_incentive]"""
    salary_expense: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司目前每年工资开销多少？"}
    )
    core_team_comp: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "核心创始团队目前工资和激励情况如何？"}
    )
    sales_incentives: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "销售团队的销售绩效和激励是如何制定的？"}
    )
    rd_metrics: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "研发团队是否涉及的相关的业绩考核指标？"}
    )
    esop: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司是否有员工持股计划？员工激励方案大概是怎么样的？"}
    )
class TalentStrategySubView(BaseModel):
    """### 公司人才制度如何？ [id:talent_strategy]"""
    talent_management: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司通过何种办法招揽和寻找最优质的人才？如何不断培养公司的人才？如何留住公司核心人才？"}
    )
class DecisionMakingSubView(BaseModel):
    """### 公司决策机制如何？ [id:decision_making]"""
    decision_process: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的重大决策如何制定？是否有完善的考虑机制和决策流程？"}
    )
class ConflictResolutionSystemSubView(BaseModel):
    """### 公司如何处理内部矛盾和冲突？ [id:conflict_resolution_system]"""
    internal_conflict_system: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "当公司面临重大公司矛盾和冲突时如何解决？是否有系统的解决方案和流程？如何保证公平公正和实事求是的解决问题？"}
    )
class LongTermPotentialView(BaseModel):
    """## 6. 创始团队长期潜力如何？ [id:long_term_potential]"""
    vision_ambition: Optional[str] = Field(
        None,
        json_schema_extra={"markdown_title": "公司的长期愿景和使命是否清晰并具有雄心？"}
    )
    equity_incentive: EquityIncentiveSubView = Field(
        default_factory=EquityIncentiveSubView,
        json_schema_extra={"markdown_title": "创始团队间股权和利益分配机制如何？是否合理？是否满足创始团队间的预期？公司的核心激励策略是否能真正激励大家？"}
    )
    talent_strategy: TalentStrategySubView = Field(
        default_factory=TalentStrategySubView,
        json_schema_extra={"markdown_title": "公司人才制度如何？"}
    )
    decision_making: DecisionMakingSubView = Field(
        default_factory=DecisionMakingSubView,
        json_schema_extra={"markdown_title": "公司决策机制如何？"}
    )
    conflict_resolution_system: ConflictResolutionSystemSubView = Field(
        default_factory=ConflictResolutionSystemSubView,
        json_schema_extra={"markdown_title": "公司如何处理内部矛盾和冲突？"}
    )
@register_schema
class CompanyFounderAndTeamView(BaseModel):
    __business_architecture__: str = """
# 二、公司创始人和团队 [id:company_founder_and_team]

## 1. 公司是否具有清晰且共享的愿景及价值观？ [id:vision_and_values]

### 公司团队对公司的长期愿景和价值观是否有统一的认识和认同？ [id:team_recognition]

#### 公司从上到下是否都充分了解公司的价值观和愿景？是否都十分认可公司的价值观和愿景？ [id:awareness_and_endorsement]

## 2. 团队构成是否完整？（主要了解团队是否完整，相互之间是否互补） [id:team_structure_and_collaboration]

### 团队技能是否互补？（团队成员是否覆盖产品、销售和综合管理等岗位？是否技能相互互补？） [id:team_completeness]
### 团队行业经验是否足够？（创始人及核心团队成员是否拥有相关行业深入知识和经验？是否深刻理解市场？是否拥有较为广泛的人脉资源？） [id:industry_experience]
### 团队成员间是否有明确的分工？协作是否顺畅？管理结构是否高效？ [id:role_clarity]

## 3. 创始人及核心团队综合能力情况如何？ [id:core_competencies]

### 公司团队关系及协作是否融洽？ [id:team_collaboration]

#### 团队成员是否在创业之前有过协作经历？ [id:prior_collaboration]
#### 目前团队成员之间关系是否融洽？沟通是否顺畅？ [id:current_relationship]

### 创始人及核心团队成员技术水平和产品打造能力如何？ [id:technical_product_capability]

#### 创始人及核心团队成员具备哪些核心技术能力？ [id:core_technical_skills]
#### 是否有过从0到1构建产品的经历？ [id:zero_to_one_experience]

### 创始人及核心团队成员商业能力如何？ [id:business_capability]

#### 创始人及核心团队成员是否有过市场营销和销售的经历？ [id:marketing_sales_exp]
#### 创始人及核心团队成员是否有过项目融资经历？ [id:financing_exp]
#### 创始人及核心团队成员是否有过商务拓展及合作谈判能力？ [id:bd_negotiation_exp]

### 创始人及核心团队成员管理能力如何？ [id:leadership_management]

#### 创始人及核心团队成员领导过多少人的团队？ [id:team_size_led]
#### 创始人及核心团队成员如何激励团队？ [id:motivation_approach]
#### 创始人及核心团队成员如何处理矛盾和冲突？ [id:conflict_resolution]

### 创始人及核心团队核心品质如何？ [id:core_qualities]

#### 勤奋：团队是否总比别人要拼？ [id:diligence]
#### 借鉴降本：压低各类费用开支产品成本，费用是否总比别人更省？ [id:cost_efficiency]
#### 稳健踏实：业务决策基本不出大错，是否步伐总比别人要稳健，诚实做人，踏实做事？ [id:steadiness]
#### 创新开拓：守正出奇，是否总是能持续研发新技术和新产品、在营销和管理等全方面都有创新？ [id:innovation]
#### 规范管理：公司是否在财务、考勤、内控、人力、等多方面有完善和规范的制度？ [id:standardized_management]
#### 整合发展：整合资源、借力发展、是否懂得整合资源和合作共赢？ [id:resource_integration]
#### 修行修心：团队是否在创业过程中不断提升自己，并帮助别人？是否能做到说事不讲假话，做事不谋私利，同事不搞是非？ [id:self_improvement]

## 4. 创始人和市场契合情况如何？ [id:founder_market_fit]

### 创始人为什么选择了这个市场？ [id:market_selection_reason]
### 创始人是否对目标用户面临的问题有切身体会或深刻洞察？ [id:problem_insight]
### 创始人能否真正站在客户角度思考？ [id:customer_centric]
### 创始人的愿景是否与市场未来的发展方向一致？ [id:vision_alignment]
### 创始人是否对所做的事情充满持久的热情，甚至到了痴迷的程度？ [id:passion_level]
### 创始人是否能够根据市场变化调整策略？ [id:adaptability]
### 创始人的个性和行事风格是否能融入目标市场的文化并建立连接？ [id:cultural_fit]
### 创始人在这个市场具备何种独特的优势? [id:unique_advantage]

## 5. 创始人核心品质如何？ [id:founder_personal_traits]

### 创始人的工作背景和经历如何？是否能够支持他担任公司CEO职位？ [id:ceo_fit]

#### 主要的工作经历是否能够有足够能力管理好这家公司？ [id:management_capability]

### 创始人四高如何？情商是否高？财商是否高？逆商是否高？智商是否高？ [id:four_highs]

#### 创始人是否有重大失败过往？以前如何面对失败？对将来可能面临的失败如何看待？ [id:failure_experience]
#### 创始人和人沟通说话是否让人感觉舒服？是否能协调团队间的矛盾？ [id:eq_and_communication]
#### 创始人学历情况如何？对新事物接纳能力如何？ [id:education_and_learning]
#### 创始人对钱认知？过往是否赚过大钱？ [id:money_mindset]

### 创始人及核心团队四项品格如何？（诚信、大气、狼性、学习） [id:team_character]

#### 创始人及核心团队如何保持持续学习能力？公司是否有相应机制保证团队成员不断学习？ [id:continuous_learning]
#### 创始人是否说话算话，诚信靠谱？ [id:integrity]
#### 创始人及核心团队是否有战斗力？是否有不断追求行业领先的动力和想法？ [id:competitiveness]
#### 创始人是否斤斤计较？是否在工作中抓大放小？ [id:magnanimity]

### 创始人认知水平和对问题本质的判断能力如何？ [id:cognitive_judgment]

#### 创始人及团队决定创立这家公司的核心逻辑是什么？基于什么判断？最本质的逻辑是什么？ [id:founding_logic]
#### 核心创始人对公司所处行业未来发展趋势的判断是什么？基于什么逻辑得出该判断？ [id:industry_trend]
#### 创始人之前做过哪些重大决策和项目？但是决策的逻辑和方法是什么？ [id:decision_methodology]
#### 创始人对这家公司最终的愿景是什么？ [id:ultimate_vision]
#### 创始人及核心团队如何评估市场？如发现市场发生变化如何快速调整和适应？ [id:market_evaluation]

## 6. 创始团队长期潜力如何？ [id:long_term_potential]

### 公司的长期愿景和使命是否清晰并具有雄心？ [id:vision_ambition]
### 创始团队间股权和利益分配机制如何？是否合理？是否满足创始团队间的预期？公司的核心激励策略是否能真正激励大家？ [id:equity_incentive]

#### 公司目前每年工资开销多少？ [id:salary_expense]
#### 核心创始团队目前工资和激励情况如何？ [id:core_team_comp]
#### 销售团队的销售绩效和激励是如何制定的？ [id:sales_incentives]
#### 研发团队是否涉及的相关的业绩考核指标？ [id:rd_metrics]
#### 公司是否有员工持股计划？员工激励方案大概是怎么样的？ [id:esop]

### 公司人才制度如何？ [id:talent_strategy]

#### 公司通过何种办法招揽和寻找最优质的人才？如何不断培养公司的人才？如何留住公司核心人才？ [id:talent_management]

### 公司决策机制如何？ [id:decision_making]

#### 公司的重大决策如何制定？是否有完善的考虑机制和决策流程？ [id:decision_process]

### 公司如何处理内部矛盾和冲突？ [id:conflict_resolution_system]

#### 当公司面临重大公司矛盾和冲突时如何解决？是否有系统的解决方案和流程？如何保证公平公正和实事求是的解决问题？ [id:internal_conflict_system]
""".strip()

    """# 二、公司创始人和团队 [id:company_founder_and_team]"""
    vision_and_values: VisionAndValuesView = Field(
        default_factory=VisionAndValuesView,
        json_schema_extra={"markdown_title": "1. 公司是否具有清晰且共享的愿景及价值观？"}
    )
    team_structure_and_collaboration: TeamStructureAndCollaborationView = Field(
        default_factory=TeamStructureAndCollaborationView,
        json_schema_extra={"markdown_title": "2. 团队构成是否完整？（主要了解团队是否完整，相互之间是否互补）"}
    )
    core_competencies: CoreCompetenciesView = Field(
        default_factory=CoreCompetenciesView,
        json_schema_extra={"markdown_title": "3. 创始人及核心团队综合能力情况如何？"}
    )
    founder_market_fit: FounderMarketFitView = Field(
        default_factory=FounderMarketFitView,
        json_schema_extra={"markdown_title": "4. 创始人和市场契合情况如何？"}
    )
    founder_personal_traits: FounderPersonalTraitsView = Field(
        default_factory=FounderPersonalTraitsView,
        json_schema_extra={"markdown_title": "5. 创始人核心品质如何？"}
    )
    long_term_potential: LongTermPotentialView = Field(
        default_factory=LongTermPotentialView,
        json_schema_extra={"markdown_title": "6. 创始团队长期潜力如何？"}
    )