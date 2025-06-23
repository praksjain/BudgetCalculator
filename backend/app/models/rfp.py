from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class RFP(Base):
    __tablename__ = "rfps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    client_name = Column(String(255), nullable=False)
    submission_deadline = Column(DateTime, nullable=False)
    budget_range = Column(String(100))
    status = Column(String(50), default="draft")
    document_path = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="rfps")
    project = relationship("Project", back_populates="rfp", uselist=False)
    analysis = relationship("RFPAnalysis", back_populates="rfp", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RFP {self.title}>" 