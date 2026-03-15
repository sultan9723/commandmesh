from enum import Enum
from pydantic import BaseModel, Field


class SensitivityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RouteRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt to route")
    sensitivity: SensitivityLevel = SensitivityLevel.low
    user_role: str = Field(default="developer", min_length=1)


class RouteResponse(BaseModel):
    prompt: str
    user_role: str
    sensitivity: str
    selected_model: str | None = None
    reason: str
    status: str
    allowed: bool