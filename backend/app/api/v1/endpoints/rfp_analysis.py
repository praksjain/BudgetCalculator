from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.models.rfp import RFP
from app.models.rfp_analysis import RFPAnalysis, AnalysisTask, AnalysisSubtask
from app.schemas.rfp_analysis import (
    RFPAnalysisResponse, 
    DocumentAnalysisRequest,
    AnalysisTaskResponse,
    AnalysisSubtaskResponse
)
from app.services.document_analysis import document_analysis_service

router = APIRouter()

@router.post("/{rfp_id}/analyze")
async def analyze_rfp_document(
    rfp_id: int,
    background_tasks: BackgroundTasks,
    request: DocumentAnalysisRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Analyze RFP document using selected AI model and technology stack"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if not rfp.document_path:
        raise HTTPException(status_code=400, detail="No document uploaded for this RFP")
    
    try:
        # Run analysis using the simplified method with configuration
        analysis = await document_analysis_service.analyze_rfp_document(
            db=db, 
            rfp_id=rfp_id,
            model=request.model,
            application_type=request.application_type,
            technology_config=request.technology_config,
            rate_card=request.rate_card
        )
        
        return {
            "message": "Analysis completed successfully", 
            "analysis_id": analysis.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/{rfp_id}/analysis", response_model=RFPAnalysisResponse)
def get_rfp_analysis(
    rfp_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get RFP analysis results"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get analysis
    analysis = db.query(RFPAnalysis).filter(RFPAnalysis.rfp_id == rfp_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this RFP")
    
    return analysis

@router.get("/{rfp_id}/analysis/tasks", response_model=List[AnalysisTaskResponse])
def get_analysis_tasks(
    rfp_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get analysis tasks for an RFP"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get analysis
    analysis = db.query(RFPAnalysis).filter(RFPAnalysis.rfp_id == rfp_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this RFP")
    
    # Get tasks
    tasks = db.query(AnalysisTask).filter(
        AnalysisTask.analysis_id == analysis.id
    ).order_by(AnalysisTask.order_index).all()
    
    return tasks

@router.get("/tasks/{task_id}/subtasks", response_model=List[AnalysisSubtaskResponse])
def get_task_subtasks(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get subtasks for a specific task"""
    
    # Get task and verify access
    task = db.query(AnalysisTask).filter(AnalysisTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if user has access to the RFP
    rfp = db.query(RFP).join(RFPAnalysis).filter(
        RFPAnalysis.id == task.analysis_id
    ).first()
    
    if not rfp or rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get subtasks
    subtasks = db.query(AnalysisSubtask).filter(
        AnalysisSubtask.task_id == task_id
    ).order_by(AnalysisSubtask.order_index).all()
    
    return subtasks

@router.delete("/{rfp_id}/analysis")
def delete_rfp_analysis(
    rfp_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Delete RFP analysis"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get and delete analysis
    analysis = db.query(RFPAnalysis).filter(RFPAnalysis.rfp_id == rfp_id).first()
    if analysis:
        db.delete(analysis)
        db.commit()
        return {"message": "Analysis deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="No analysis found for this RFP")

@router.post("/{rfp_id}/generate-task-breakdown")
async def generate_task_breakdown(
    rfp_id: int,
    force_regenerate: bool = False,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate detailed task breakdown for an RFP"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if analysis exists
    analysis = db.query(RFPAnalysis).filter(RFPAnalysis.rfp_id == rfp_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found. Please analyze the RFP first.")
    
    try:
        # Check if tasks already exist
        existing_tasks_count = db.query(AnalysisTask).filter(
            AnalysisTask.analysis_id == analysis.id
        ).count()
        
        # Generate task breakdown
        task_breakdown = await document_analysis_service.generate_task_breakdown(db, rfp_id, force_regenerate)
        
        message = "Task breakdown generated successfully"
        if existing_tasks_count > 0 and not force_regenerate:
            message = "Task breakdown already exists, returning existing data"
        elif force_regenerate:
            message = "Task breakdown regenerated successfully"
        
        return {
            "message": message,
            "task_breakdown": task_breakdown,
            "has_existing_tasks": existing_tasks_count > 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task breakdown generation failed: {str(e)}")

@router.get("/{rfp_id}/export-tasks-excel")
async def export_tasks_to_excel(
    rfp_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Export analysis tasks to Excel format"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    
    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if analysis exists
    analysis = db.query(RFPAnalysis).filter(RFPAnalysis.rfp_id == rfp_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this RFP")
    
    # Check if tasks exist
    tasks_count = db.query(AnalysisTask).filter(
        AnalysisTask.analysis_id == analysis.id
    ).count()
    
    if tasks_count == 0:
        raise HTTPException(status_code=404, detail="No tasks found for export. Please generate task breakdown first.")
    
    try:
        # Generate Excel file
        excel_buffer = document_analysis_service.export_tasks_to_excel(db, rfp_id)
        
        # Create filename
        safe_title = "".join(c for c in rfp.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title}_Task_Breakdown.xlsx"
        
        # Return file as streaming response
        return StreamingResponse(
            excel_buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel export failed: {str(e)}")

@router.get("/analysis/status/{rfp_id}")
def get_analysis_status(
    rfp_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Check if analysis exists for an RFP"""
    
    # Check if RFP exists and user has access
    rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")

    if rfp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if analysis exists
    analysis = db.query(RFPAnalysis).filter(RFPAnalysis.rfp_id == rfp_id).first()
    
    return {
        "has_analysis": analysis is not None,
        "has_document": rfp.document_path is not None,
        "can_analyze": rfp.document_path is not None,
        "analysis_id": analysis.id if analysis else None
    } 