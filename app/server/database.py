import motor.motor_asyncio
from bson.objectid import ObjectId
from server.connection import get_connection_string

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = get_connection_string()
# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
database = client['nav_chat_data']

channels_collection = database.get_collection("channels")
users_collection = database.get_collection("users")


#Fields:

user_fields = ["name", "email", "picture_url", "channels"]

# helpers

def channel_helper(channel) -> dict:
    return {
        "id": str(channel["_id"]),
        "name": channel["name"],
        "description": channel["description"],
        "creator_id": channel["creator_id"],
        "members": channel["members"],
    }

def user_helper(user) -> dict:
    result = {"id": str(user["_id"])}
    for field in user_fields:
        result[field] = user[field]
    return result


##CHANNEL FUNCTIONS

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
    return False


##USER FUNCTIONS

#Retrieve all users
async def retrieve_users():
    users = []
    for user in users_collection.find():
        users.append(user_helper(user))
    return users

#Add NEW user
async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

#Retrieve user
async def retrieve_user(id: str) -> dict:
    user = users_collection.find_one({"_id": ObjectId(id)})
    return user_helper(user)

#Update user
async def update_user(id: str, input_data: dict):
    if len(input_data) < 1:
        return False
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        data = user_helper(user)
        for input_field in input_data:
            if input_field in user_fields:
                data[input_field] = input_data[input_field]
        updated_user = await users_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_user:
            return True
    return False

async def delete_user(id: str):
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False