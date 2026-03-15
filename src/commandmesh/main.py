from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from src.commandmesh.services.routing import choose_model


app = FastAPI(title="CommandMesh")


class RouteRequest(BaseModel):
    prompt: str
    sensitivity: Optional[str] = "low"
    user_role: Optional[str] = "developer"


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


@app.post("/route")
def route_request(request: RouteRequest):
    decision = choose_model(request.sensitivity)

    return {
        "prompt": request.prompt,
        "user_role": request.user_role,
        "sensitivity": request.sensitivity,
        "selected_model": decision["selected_model"],
        "reason": decision["reason"],
        "status": "routed"
    }