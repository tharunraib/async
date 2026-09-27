from fastapi import FastAPI
from app.routes import incidents, retrieval, clusters, preflight, audit

app = FastAPI(title="Root Cause", version="0.1.0")

app.include_router(incidents.router, prefix="/api")
app.include_router(retrieval.router, prefix="/api")
app.include_router(clusters.router, prefix="/api")
app.include_router(preflight.router, prefix="/api")
app.include_router(audit.router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok", "service": "root-cause"}
