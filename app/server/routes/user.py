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
    delete_user,
    retrieve_channels_of_user
)

from server.models.model import (
    ErrorResponseModel,
    ResponseModel
)

router = APIRouter()

@router.get("/{user_id}/channels", response_description="Channels of user retrieved successfully")
async def get_user_data(user_id: str):
    user = await retrieve_user(user_id)
    if not user:
        return ResponseModel("User with user id: {user_id} does not exist.")
    channels = await retrieve_channels_of_user(user_id)
    if channels:
        return ResponseModel(channels, "Channels of user with user id: {user_id}, retrieved successfully")
    return ResponseModel(channels, "Empty list returned")

@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")

@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ResponseModel(404, "User does not exist.")

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
    
@router.delete("/{id}")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )