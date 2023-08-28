from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class ChannelSchema(BaseModel):
    name: str = Field(...) #... means that the field is required
    description: str = Field(...)
    creator_id: str = Field(...)
    members: List[str] = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "name": "Friends",
                "description": "Yaaran naal bahaaraan!",
                "creator_id": "1",
                "members": ['1', '2', '3']
            }
        }

class UpdateChannelModel(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    creator_id: Optional[str] = Field(None)
    members: Optional[List[str]] = Field(None)
    class Config:
        schema_extra = {
            "example": {
                "name": "Friends",
                "description": "jYaaran naal bahaaraan!",
                "creator_id": "1",
                "members": ['1', '2', '3']
            }
        }