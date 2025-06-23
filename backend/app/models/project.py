from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    budget = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(50))
    owner_id = Column(Integer, ForeignKey("users.id"))
    rfp_id = Column(Integer, ForeignKey("rfps.id"), unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_projects")
    rfp = relationship("RFP", foreign_keys=[rfp_id], back_populates="project", uselist=False)
    assigned_users = relationship("User", secondary="project_user_association", back_populates="assigned_projects")

    def __repr__(self):
        return f"<Project {self.name}>" 