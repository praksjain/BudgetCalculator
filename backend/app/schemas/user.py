from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, Union

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Literal["director", "delivery_manager", "project_manager", "custom"] = "project_manager"
    is_active: Optional[bool] = True
    custom_permissions: Optional[str] = None

    class Config:
        use_enum_values = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        use_enum_values = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
        use_enum_values = True

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[Union[str, int]] = None 