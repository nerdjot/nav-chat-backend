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
    name: Optional[str]
    description: Optional[str]
    creator_id: Optional[str]
    members: Optional[List[str]]
    class Config:
        schema_extra = {
            "example": {
                "name": "Friends",
                "description": "jYaaran naal bahaaraan!",
                "creator_id": "1",
                "members": ['1', '2', '3']
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}