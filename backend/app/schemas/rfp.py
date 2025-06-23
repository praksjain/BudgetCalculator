from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class RFPBase(BaseModel):
    title: str
    description: Optional[str] = None
    client_name: str
    submission_deadline: datetime
    budget_range: Optional[str] = None
    status: str = "draft"
    document_path: Optional[str] = None

class RFPCreate(RFPBase):
    pass

class RFPUpdate(RFPBase):
    title: Optional[str] = None
    client_name: Optional[str] = None
    submission_deadline: Optional[datetime] = None

class RFPResponse(RFPBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RFPInDBBase(RFPBase):
    id: int
    document_path: Optional[str] = None
    version: int = 1
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RFP(RFPInDBBase):
    pass

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    required_developers: Optional[int] = None
    required_test_engineers: Optional[int] = None
    required_project_managers: Optional[int] = None
    other_roles: Optional[Dict[str, Any]] = None
    resource_costs: Optional[Dict[str, Any]] = None
    infrastructure_costs: Optional[Dict[str, Any]] = None
    license_fees: Optional[Dict[str, Any]] = None
    overhead_costs: Optional[float] = None
    profit_margin: Optional[float] = None
    currency: str = "USD"

class ProjectCreate(ProjectBase):
    rfp_id: int

class ProjectUpdate(ProjectBase):
    pass

class ProjectInDBBase(ProjectBase):
    id: int
    rfp_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass 