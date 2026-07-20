from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import connect_to_mongo, close_mongo_connection
from app.api.v1.auth.router import router as auth_router

app = FastAPI(
    title="MediSense AI API",
    description="Backend service for MediSense AI medical analysis and health dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Register V1 API Routers
app.include_router(auth_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to MediSense AI API", "status": "online"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "service": "MediSense AI Backend"}
