from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import asyncio
from api.routers import stories

prefix = "/v1"

# Setup FastAPI app
app = FastAPI(
    title="API Server",
    description="API Server",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Startup tasks
    pass

# Routes
@app.get("/")
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }

# Additional routers here
app.include_router(stories.router, prefix=prefix)