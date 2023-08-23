from fastapi import FastAPI

from server.routes.channel import router as ChannelRouter

app = FastAPI()

app.include_router(ChannelRouter, tags=["Channel"], prefix="/channel")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}