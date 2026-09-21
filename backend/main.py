from fastapi import FastAPI

from database.connection import engine, Base
from database import models

app = FastAPI(
    title="Cloud-Native Multi-Tenant SaaS",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Cloud-Native Multi-Tenant SaaS API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "saas-backend"
    }
