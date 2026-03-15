from fastapi import FastAPI, Query

from src.commandmesh.models.route import RouteRequest, RouteResponse
from src.commandmesh.services.audit import get_audit_logs
from src.commandmesh.services.routing import process_route_request


app = FastAPI(title="CommandMesh")


@app.get("/")
def root():
    return {
        "message": "CommandMesh API is running",
        "docs": "/docs",
        "health": "/health",
        "audit_logs": "/audit/logs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "CommandMesh"
    }


@app.get("/audit/logs")
def read_audit_logs(limit: int = Query(default=10, ge=1, le=100)):
    return {
        "count": len(get_audit_logs(limit)),
        "logs": get_audit_logs(limit)
    }


@app.post("/route", response_model=RouteResponse)
def route_request(request: RouteRequest):
    result = process_route_request(request)
    return RouteResponse(**result)