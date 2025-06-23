from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get all projects"""
    projects = db.query(Project).all()
    return projects

@router.post("/", response_model=ProjectResponse)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Create new project"""
    project = Project(**project_in.dict(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project 