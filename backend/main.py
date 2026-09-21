from fastapi import FastAPI

from database.connection import engine, Base
from database import models

from tenant.routes import router as tenant_router
from project.routes import router as project_router
from task.routes import router as task_router


app = FastAPI(
    title="Cloud-Native Multi-Tenant SaaS",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register API routers
app.include_router(tenant_router)
app.include_router(project_router)
app.include_router(task_router)


@app.get("/")
def root():
    return {
        "message": "Cloud-Native Multi-Tenant SaaS API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
