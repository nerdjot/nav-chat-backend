from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    picture_url: str = Field(...)
    channels: List[str] = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "name": "Navjot Singh",
                "email": "navjot@gmail.com",
                "picture_url": "https://www.gravatar.com/avatar/2c7d99fe281ecd3bcd65ab915bac6dd5",
                "channels": ["1", "2", "3"]
            }
        }

class UpdateUserModel(BaseModel):
    name: Optional[str] = Field(None, description="users name")
    email: Optional[EmailStr] = Field(None)
    picture_url: Optional[str] = Field(None)
    channels: Optional[str] = Field(None)
    class Config:
        schema_extra = {
            "example": {
                "name": "Navjot Singh",
                "email": "navjot@gmail.com",
                "picture_url": "https://www.gravatar.com/avatar/2c7d99fe281ecd3bcd65ab915bac6dd5",
                "channels": ["1", "2", "3"]
            }
        }