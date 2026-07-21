from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import connect_to_postgres, close_postgres_connection
from app.api.v1.auth.router import router as auth_router
from app.api.v1.medical_reports.router import router as reports_router
from app.api.v1.medication.router import router as medication_router
from app.api.v1.dashboard.router import router as dashboard_router

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
    await connect_to_postgres()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_postgres_connection()

# Register V1 API Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(medication_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to MediSense AI API", "status": "online"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "service": "MediSense AI Backend"}
