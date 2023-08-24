from fastapi import FastAPI

from server.routes.channel import router as ChannelRouter
from server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(ChannelRouter, tags=["Channel"], prefix="/channel")
app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}