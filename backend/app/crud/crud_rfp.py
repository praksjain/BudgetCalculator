from typing import Any, Dict, Optional, Union
import os
import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.base import CRUDBase
from app.models.rfp import RFP, Project
from app.models.user import User
from app.schemas.rfp import RFPCreate, RFPUpdate, ProjectCreate, ProjectUpdate

class CRUDRFP(CRUDBase[RFP, RFPCreate, RFPUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: RFPCreate, owner_id: int
    ) -> RFP:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, created_by_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_owner(self, db: Session, *, rfp: RFP, user: User) -> bool:
        return rfp.created_by_id == user.id

    async def save_document(self, file: UploadFile) -> str:
        """
        Save uploaded document and return the file path
        """
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file.filename}")
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        return file_path

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create_with_rfp(
        self, db: Session, *, obj_in: ProjectCreate, rfp_id: int
    ) -> Project:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, rfp_id=rfp_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_rfp(self, db: Session, *, rfp_id: int) -> Optional[Project]:
        return db.query(self.model).filter(self.model.rfp_id == rfp_id).first()

rfp = CRUDRFP(RFP)
project = CRUDProject(Project) 