from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.commandmesh.services.routing import choose_model


app = FastAPI(title="CommandMesh")


class SensitivityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RouteRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt to route")
    sensitivity: SensitivityLevel = SensitivityLevel.low
    user_role: Optional[str] = Field(default="developer", min_length=1)


class RouteResponse(BaseModel):
    prompt: str
    user_role: str
    sensitivity: str
    selected_model: str
    reason: str
    status: str


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
    decision = choose_model(request.sensitivity.value)

    return RouteResponse(
        prompt=request.prompt,
        user_role=request.user_role or "developer",
        sensitivity=request.sensitivity.value,
        selected_model=decision["selected_model"],
        reason=decision["reason"],
        status="routed"
    )