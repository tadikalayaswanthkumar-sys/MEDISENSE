from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def read_root():
    return {"message": "Welcome to MediSense AI API", "status": "online"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "service": "MediSense AI Backend"}
