from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routers import ai_analytics

app = FastAPI(
    title="AI Analytics Service",
    description="AI-powered analytics service for SchoolOS",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_analytics.router, prefix="/api/v1", tags=["ai-analytics"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-analytics-service"}

@app.get("/")
async def root():
    return {"message": "AI Analytics Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8017) 