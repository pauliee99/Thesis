# main.py

from fastapi import FastAPI
from app.api import events, users, auth
from app.core import config

app = FastAPI()

# Include routers
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Additional configuration settings
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
