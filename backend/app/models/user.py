from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, nullable=False, default="project_manager")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Additional fields for custom roles
    custom_permissions = Column(String)
    
    # Relationships
    owned_projects = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    rfps = relationship("RFP", back_populates="owner", foreign_keys="RFP.owner_id")
    assigned_projects = relationship("Project", secondary="project_user_association", back_populates="assigned_users") 