from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_channel,
    delete_channel,
    retrieve_channel,
    retrieve_channels,
    update_channel,
    add_members
)
from server.models.channel import (
    ChannelSchema,
    UpdateChannelModel,
    MembersSchema
)

from server.models.model import (
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()

@router.post("/", response_description="Channel data added into the database")
async def add_channel_data(channel: ChannelSchema = Body(...)):
    channel = jsonable_encoder(channel)
    new_channel = await add_channel(channel)
    if new_channel:
        return ResponseModel(new_channel, "Channel added successfully.")
    return ResponseModel(404, "Could not create channel")#I want to add a proper error message here, from DB funciton it should populate.

@router.get("/", response_description="Channels retrieved")
async def get_channels():
    channels = await retrieve_channels()
    if channels:
        return ResponseModel(channels, "Channels data retrieved successfully")
    return ResponseModel(channels, "Empty list returned") 


@router.get("/{id}", response_description="Channel data retrieved")
async def get_channel_data(id):
    channel = await retrieve_channel(id)
    if channel:
        return ResponseModel(channel, "Channel data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Channel doesn't exist.")

@router.put("/{id}")
async def update_channel_data(id: str, req: UpdateChannelModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_channel = await update_channel(id, req)
    if updated_channel:
        return ResponseModel(
            "Channel with ID: {} name update is successful".format(id),
            "Channel updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the channel data.",
    )

@router.delete("/{id}", response_description="Channel data deleted from the database")
async def delete_channel_data(id: str):
    deleted_channel = await delete_channel(id)
    if deleted_channel:
        return ResponseModel(
            "Channel with ID: {} removed".format(id), "Channel deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Channel with id {0} doesn't exist".format(id)
    )

@router.post("/{id}/members", response_description="Members added to channel")
async def add_members_to_channel(id:str, members: MembersSchema = Body(...)):
    members = jsonable_encoder(members)
    updated_channel = await add_members(id, members)
    if updated_channel:
        return ResponseModel(
            "Channel with ID: {} name update is successful".format(id),
            "Channel updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the channel data.",
    )
