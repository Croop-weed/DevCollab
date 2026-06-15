from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.api.v1 import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up DevCollab...")
    yield
    print("Shutting down...")

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(user.router,prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    print("----------------------------------------")
    print(f"🔥 APPLICATION STARTED: {settings.APP_NAME}")
    print(f"🌐 DATABASE CONNECTED: {settings.DATABASE_URL}")
    print("----------------------------------------")

@app.get("/health")
async def health():
    return {"status": "online"}

