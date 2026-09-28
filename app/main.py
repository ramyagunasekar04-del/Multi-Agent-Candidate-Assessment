from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Multi-Agent Candidate Assessment System",
    version="1.0.0",
    description="AI-powered multi-agent candidate assessment platform"
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Multi-Agent Candidate Assessment System",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }