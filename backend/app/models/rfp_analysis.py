from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class RFPAnalysis(Base):
    __tablename__ = "rfp_analyses"

    id = Column(Integer, primary_key=True, index=True)
    rfp_id = Column(Integer, ForeignKey("rfps.id"), unique=True, nullable=False)
    
    # OpenAI Analysis Results
    summary = Column(Text)  # Gist of the RFP
    scope = Column(Text)  # Project scope
    requirements = Column(Text)  # Key requirements
    deliverables = Column(Text)  # Expected deliverables
    timeline = Column(Text)  # Estimated timeline (can be longer AI-generated content)
    complexity_level = Column(String(100))  # Low, Medium, High (increased length for more detailed complexity descriptions)
    technology_stack = Column(Text)  # Suggested tech stack
    risks = Column(Text)  # Identified risks
    
    # Analysis metadata
    total_estimated_hours = Column(Float)
    total_estimated_cost = Column(Float)
    confidence_level = Column(Float)  # 0-1 confidence in the analysis
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rfp = relationship("RFP", back_populates="analysis")
    tasks = relationship("AnalysisTask", back_populates="analysis", cascade="all, delete-orphan")

class AnalysisTask(Base):
    __tablename__ = "analysis_tasks"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("rfp_analyses.id"), nullable=False)
    
    # Task details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # Frontend, Backend, Database, Testing, etc.
    module = Column(String(100))  # Module name for grouping tasks
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    
    # Estimates
    estimated_hours = Column(Float)
    estimated_cost = Column(Float)
    complexity = Column(String(20))  # simple, moderate, complex
    
    # Task metadata
    order_index = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analysis = relationship("RFPAnalysis", back_populates="tasks")
    subtasks = relationship("AnalysisSubtask", back_populates="task", cascade="all, delete-orphan")

class AnalysisSubtask(Base):
    __tablename__ = "analysis_subtasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("analysis_tasks.id"), nullable=False)
    
    # Subtask details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    estimated_hours = Column(Float)
    estimated_cost = Column(Float)
    
    # Comments/Notes
    comments = Column(Text)
    
    # Subtask metadata
    order_index = Column(Integer, default=0)
    is_critical = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    task = relationship("AnalysisTask", back_populates="subtasks") 