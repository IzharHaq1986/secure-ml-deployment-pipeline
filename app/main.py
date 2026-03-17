from fastapi import FastAPI

app = FastAPI(
    title="Secure ML Deployment Pipeline",
    description="Minimal FastAPI service for secure ML deployment demonstration.",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    """
    Health endpoint used for local validation, container smoke tests,
    and deployment checks.
    """
    return {"status": "ok"}
