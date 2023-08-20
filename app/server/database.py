import motor.motor_asyncio
from bson.objectid import ObjectId
 
# Provide the mongodb atlas url to connect python to mongodb using pymongo


# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
database = client['nav_chat_data']

channels_collection = database.get_collection("channels")

# helpers


def channel_helper(channel) -> dict:
    return {
        "id": str(channel["_id"]),
        "name": channel["name"],
        "description": channel["description"],
        "creator_id": channel["creator_id"],
        "members": channel["members"],
    }


# Retrieve all channels present in the database
async def retrieve_channels():
    channels = []
    async for channel in channels_collection.find():
        channels.append(channel_helper(channel))
    return channels

# Add a new channel into to the database
async def add_channel(channel_data: dict) -> dict:
    channel = await channels_collection.insert_one(channel_data)
    new_channel = await channels_collection.find_one({"_id": channel.inserted_id})
    return channel_helper(new_channel)


# Retrieve a channel with a matching ID
async def retrieve_channel(id: str) -> dict:
    channel = await channels_collection.find_one({"_id": ObjectId(id)})
    if channel:
        return channel_helper(channel)
    
# Update a channel with a matching ID
async def update_channel(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    channel = await channels_collection.find_one({"_id": ObjectId(id)})
    if channel:
        updated_channel = await channels_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_channel:
            return True
        return False
    
# Delete a channel from the database
async def delete_channel(id: str):
    channel = await channels_collection.find_one({"_id": ObjectId(id)})
    if channel:
        await channels_collection.delete_one({"_id": ObjectId(id)})
        return True
