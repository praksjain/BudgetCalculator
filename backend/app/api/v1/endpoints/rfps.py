from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api import deps
from app.models.user import User
from app.models.rfp import RFP
from app.schemas.rfp import RFPCreate, RFPResponse, RFPUpdate
from app.core.config import settings
import os
import shutil
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[RFPResponse])
def get_rfps(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all RFPs"""
    rfps = db.query(RFP).offset(skip).limit(limit).all()
    return rfps

@router.post("/", response_model=RFPResponse)
def create_rfp(
    *,
    db: Session = Depends(deps.get_db),
    rfp_in: RFPCreate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Create new RFP"""
    rfp = RFP(**rfp_in.dict(), owner_id=current_user.id)
    db.add(rfp)
    db.commit()
    db.refresh(rfp)
    return rfp

@router.get("/{rfp_id}", response_model=RFPResponse)
def get_rfp(
    rfp_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get RFP by ID"""
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    return rfp

@router.put("/{rfp_id}", response_model=RFPResponse)
def update_rfp(
    *,
    db: Session = Depends(deps.get_db),
    rfp_id: int,
    rfp_in: RFPUpdate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Update RFP"""
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    for field, value in rfp_in.dict(exclude_unset=True).items():
        setattr(rfp, field, value)
    
    db.add(rfp)
    db.commit()
    db.refresh(rfp)
    return rfp

@router.delete("/{rfp_id}")
def delete_rfp(
    *,
    db: Session = Depends(deps.get_db),
    rfp_id: int,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Delete RFP"""
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(rfp)
    db.commit()
    return {"status": "success"}

@router.post("/{rfp_id}/upload")
async def upload_rfp_document(
    rfp_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Upload RFP document"""
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.UPLOAD_DIR, str(rfp_id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update RFP with file path
    rfp.document_path = file_path
    db.add(rfp)
    db.commit()
    
    return {"filename": file.filename, "path": file_path} 