from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CommitmentItem(BaseModel):
    id: str = Field(..., description="Unique commitment identifier")
    item: str = Field(..., description="Commitment or deliverable description")
    owner: str = Field(..., description="Confirmed owner or UNASSIGNED")
    due: str = Field(..., description="Deadline or scheduled date/time")
    status: str = Field(..., description="Status badge: COMPLETED, CONFIRMED, AT RISK / OPEN, SCHEDULED, CRITICAL / UNOWNED")
    priority: str = Field(..., description="HIGH, MEDIUM, or CRITICAL")
    evidence: str = Field(..., description="Grounded justification from emails, meetings, or transcripts")
    source_type: str = Field(..., description="email, transcript, calendar, voice_note")

class BriefingResponse(BaseModel):
    user: str
    scenario_week: str
    generated_at: str
    summary: str
    commitments: List[CommitmentItem]
    open_blockers: List[str]
    immediate_actions: List[str]

class QueryRequest(BaseModel):
    query: str = Field(..., example="Who owns the Mumbai lease renewal?")
    mode: Optional[str] = Field("hybrid", description="hybrid, rag, or deterministic")

class QueryResponse(BaseModel):
    query: str
    answer: str
    status: str
    confidence: float
    evidence_sources: List[str]
    model_used: str

class FreeSlotRequest(BaseModel):
    day: str = Field("24 Sep", example="24 Sep")
    duration_minutes: int = Field(30, example=30)
    person: str = Field("Arjun Malhotra", example="Arjun Malhotra")

class FreeSlotItem(BaseModel):
    day: str
    start: str
    end: str
    duration_minutes: int

class FreeSlotResponse(BaseModel):
    person: str
    day: str
    duration_minutes: int
    available_slots: List[FreeSlotItem]
    calendar_events: List[Dict[str, Any]]

class AuditLogItem(BaseModel):
    id: int
    query: str
    answer: str
    model_used: str
    created_at: str
