from fastapi import FastAPI

from src.commandmesh.models.route import RouteRequest, RouteResponse
from src.commandmesh.services.routing import process_route_request


app = FastAPI(title="CommandMesh")


@app.get("/")
def root():
    return {
        "message": "CommandMesh API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "CommandMesh"
    }


@app.post("/route", response_model=RouteResponse)
def route_request(request: RouteRequest):
    result = process_route_request(request)
    return RouteResponse(**result)