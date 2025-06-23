from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Subtask schemas
class AnalysisSubtaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    estimated_hours: Optional[float] = None
    estimated_cost: Optional[float] = None
    comments: Optional[str] = None
    order_index: int = 0
    is_critical: bool = False

class AnalysisSubtaskCreate(AnalysisSubtaskBase):
    pass

class AnalysisSubtaskUpdate(AnalysisSubtaskBase):
    title: Optional[str] = None

class AnalysisSubtaskResponse(AnalysisSubtaskBase):
    id: int
    task_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Task schemas
class AnalysisTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    module: Optional[str] = None
    priority: str = "medium"
    estimated_hours: Optional[float] = None
    estimated_cost: Optional[float] = None
    complexity: Optional[str] = None
    order_index: int = 0

class AnalysisTaskCreate(AnalysisTaskBase):
    subtasks: Optional[List[AnalysisSubtaskCreate]] = []

class AnalysisTaskUpdate(AnalysisTaskBase):
    title: Optional[str] = None

class AnalysisTaskResponse(AnalysisTaskBase):
    id: int
    analysis_id: int
    subtasks: List[AnalysisSubtaskResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# RFP Analysis schemas
class RFPAnalysisBase(BaseModel):
    summary: Optional[str] = None
    scope: Optional[str] = None
    requirements: Optional[str] = None
    deliverables: Optional[str] = None
    timeline: Optional[str] = None
    complexity_level: Optional[str] = None
    technology_stack: Optional[str] = None
    risks: Optional[str] = None
    total_estimated_hours: Optional[float] = None
    total_estimated_cost: Optional[float] = None
    confidence_level: Optional[float] = None

class RFPAnalysisCreate(RFPAnalysisBase):
    rfp_id: int
    tasks: Optional[List[AnalysisTaskCreate]] = []

class RFPAnalysisUpdate(RFPAnalysisBase):
    pass

class RFPAnalysisResponse(RFPAnalysisBase):
    id: int
    rfp_id: int
    tasks: List[AnalysisTaskResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Technology Configuration schemas
class TechnologyConfig(BaseModel):
    frontend: Optional[str] = "react"
    backend: Optional[str] = "python"
    database: Optional[str] = "postgresql"
    cloud: Optional[str] = "aws"

class RateCard(BaseModel):
    senior_developer: Optional[float] = 90.0
    mid_developer: Optional[float] = 75.0
    junior_developer: Optional[float] = 55.0
    tech_lead: Optional[float] = 110.0
    project_manager: Optional[float] = 85.0
    business_analyst: Optional[float] = 70.0
    ui_ux_designer: Optional[float] = 80.0
    qa_engineer: Optional[float] = 65.0
    devops_engineer: Optional[float] = 95.0
    blockchain_developer: Optional[float] = 120.0
    smart_contract_auditor: Optional[float] = 150.0

# Analysis Request schema for document analysis
class DocumentAnalysisRequest(BaseModel):
    rfp_id: int
    model: Optional[str] = "gpt-3.5-turbo"  # AI model selection
    application_type: Optional[str] = "web"  # mobile, web, both
    technology_config: Optional[TechnologyConfig] = TechnologyConfig()
    rate_card: Optional[RateCard] = RateCard() 