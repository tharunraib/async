from datetime import datetime
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    external_id: str
    title: str
    body: str
    component: str | None = None
    symptom: str | None = None
    dependency: str | None = None
    owner: str | None = None
    occurred_at: datetime

class SearchRequest(BaseModel):
    query: str
    limit: int = Field(default=8, ge=1, le=50)

class PreflightRequest(BaseModel):
    change_title: str
    components: list[str]
    description: str

class PolicyDecision(BaseModel):
    allowed: bool
    reason: str
