from fastapi import FastAPI

app = FastAPI(
    title="Cloud Native Multi-Tenant SaaS",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Cloud Native Multi-Tenant SaaS API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
