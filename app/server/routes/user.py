from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.models.user import (
    UserSchema,
    UpdateUserModel
)

from server.database import (
    retrieve_users,
    retrieve_user,
    add_user,
    update_user, 
    delete_user
)

from server.models.model import (
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()

@router.post("/", response_description="User added to the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully")

@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel):
    data = {k: v for k, v in req.dict().items() if v is not None}
    updated_user =  await update_user(id, data)
    if updated_user:
        return ResponseModel(
            "User with id: {} updated successfully.".format(id),
            "User updated successfully"
        )