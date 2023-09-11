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

channel_fields = ["name", "description", "creator_id", "members", "messages"]
user_fields = ["name", "email", "picture_url", "channels"]

# helpers

def channel_helper(channel) -> dict:
    result = {"id": str(channel["_id"])}
    for field in channel_fields:
        result[field] = channel[field]
    return result

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

async def retrieve_channels_of_user(user_id: str):
    channels = []
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        for channelId in user["channels"]:
            channel = await retrieve_channel(channelId)
            channels.append(channel)
    return channels

# Add a new channel into to the database
async def add_channel(channel_data: dict) -> dict:
    #storing out the members array
    members = {"members":channel_data["members"]}

    #adding empty fields needed for channel creation.
    channel_data['messages'] = []
    channel_data['members'] = []
    creator_id = channel_data["creator_id"]
    creator = await retrieve_user(creator_id)
    print("creator", creator)
    if not creator:
        return
    channel = await channels_collection.insert_one(channel_data)
    new_channel = await channels_collection.find_one({"_id": channel.inserted_id})
    if new_channel:
        await add_members(channel.inserted_id, members)
    else:
        return
    new_channel = await channels_collection.find_one({"_id": channel.inserted_id})
    return channel_helper(new_channel)


# Retrieve a channel with a matching ID
async def retrieve_channel(id: str) -> dict:
    channel = await channels_collection.find_one({"_id": ObjectId(id)})
    if channel:
        return channel_helper(channel)
    
# Update a channel with a matching ID
async def update_channel(id: str, input_data: dict):
    # Return false if an empty request body is sent.
    if len(input_data) < 1:
        return False
    channel = await channels_collection.find_one({"_id": ObjectId(id)})
    if channel:
        data = channel_helper(channel)
        del data["id"]
        for input_field in input_data:
            if input_field in channel_fields:
                data[input_field] = input_data[input_field]
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

async def add_members(channel_id: str, members):
    #add members array to channel collection
    #add channel_id to channels array of users in user collection.

    #find channel first:
    members = members["members"]
    channel = await channels_collection.find_one({"_id": ObjectId(channel_id)})
    true_members = []
    new_members = []
    if channel:
        for member_id in members:
            #find if user exist, only add users that exist
            user = await users_collection.find_one({"_id": ObjectId(member_id)})
            if user:
                true_members.append(member_id)
                #check if channel is not already added.
                if channel_id not in user["channels"]:
                    new_channels = list(set(user["channels"] + [channel_id]))
                    await update_user(member_id, {"channels": new_channels})
        print("members", channel["members"])
        new_members = list(set(list(channel["members"] + true_members)))
        print("new_members", new_members)
        await update_channel(channel_id, {"members":new_members})
        return True
    return False


##USER FUNCTIONS

#Retrieve all users
async def retrieve_users():
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

#Add NEW user
async def add_user(user_data: dict) -> dict:
    user_data["channels"] = []
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

#Retrieve user
async def retrieve_user(id: str) -> dict:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

#Update user
async def update_user(id: str, input_data: dict):
    if len(input_data) < 1:
        return False
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        data = user_helper(user)
        del data["id"]
        for input_field in input_data:
            if input_field in user_fields:
                data[input_field] = input_data[input_field]
        updated_user = await users_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
    return False

async def delete_user(id: str):
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

async def retrieve_messages(channel_id:str):
    messages =[]
    channel = await channels_collection.find_one({"_id": ObjectId(channel_id)})
    if channel:
        messages_obj = channel["messages"]
        for message_obj in messages_obj:
            messages.append(message_helper(messages_obj))
    return messages


async def add_message(channel_id: str, message_data: dict):
    message_data['message_id'] = str(ObjectId())
    result = channels_collection.update_one(
        { 'channel_id': channel_id },
        { '$push': { 'messages': message_data } }
    )
    
    if result.matched_count == 0:
        print(f"No document found with channel_id: {channel_id}")
    else:
        print(f"Successfully added message to channel with channel_id: {channel_id}")