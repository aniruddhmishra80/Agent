from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import json

from .config import (
    AUTHOR_NAME,
    INSTITUTION,
    COHORT,
    ASSIGNMENT_TITLE,
    TARGET_USER,
    SCENARIO_WEEK,
    DATA_PATH
)
from .models import (
    BriefingResponse,
    CommitmentItem,
    QueryRequest,
    QueryResponse,
    FreeSlotResponse,
    FreeSlotItem
)
from .core import (
    get_executive_brief,
    get_commitments,
    ask_agent,
    get_audit_logs
)
from .calendar_engine import (
    find_free_slots,
    get_person_events,
    load_calendar_data
)

app = FastAPI(
    title="Executive Productivity Agent API",
    description=f"{ASSIGNMENT_TITLE} for {COHORT}. Developed by {AUTHOR_NAME} ({INSTITUTION}).",
    version="1.0.0"
)

# Enable CORS for frontend and cross-origin tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "project": ASSIGNMENT_TITLE,
        "author": AUTHOR_NAME,
        "institution": INSTITUTION,
        "cohort": COHORT,
        "user": TARGET_USER,
        "scenario_week": SCENARIO_WEEK,
        "docs_url": "/docs",
        "endpoints": {
            "health": "/api/health",
            "brief": "/api/brief",
            "commitments": "/api/commitments",
            "query": "POST /api/query",
            "free_slots": "/api/calendar/free-slots",
            "evidence": "/api/evidence",
            "audit_log": "/api/audit-log"
        }
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "agent": "Executive Productivity Agent",
        "author": AUTHOR_NAME,
        "ready_for_eval": True
    }

@app.get("/api/brief", response_model=BriefingResponse)
def get_brief():
    """Returns a synthesized executive briefing for Arjun Malhotra."""
    return get_executive_brief()

@app.get("/api/commitments", response_model=List[CommitmentItem])
def list_commitments(status: Optional[str] = None):
    """Returns the ledger of commitments, optionally filtered by status."""
    items = get_commitments()
    if status:
        items = [i for i in items if status.lower() in i.status.lower()]
    return items

@app.post("/api/query", response_model=QueryResponse)
def process_query(req: QueryRequest):
    """Answers executive questions grounded strictly in the scenario dataset."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return ask_agent(query=req.query, mode=req.mode or "hybrid")

@app.get("/api/calendar/free-slots", response_model=FreeSlotResponse)
def get_free_slots(
    person: str = Query("Arjun Malhotra", description="Person name"),
    day: str = Query("Thu 24 Sep", description="Day string (e.g. 'Thu 24 Sep')"),
    duration_minutes: int = Query(30, description="Meeting slot duration in minutes")
):
    """Calculates open meeting windows for a person on a specific day."""
    slots = find_free_slots(person=person, day=day, duration_minutes=duration_minutes)
    events = get_person_events(person=person, day=day)
    return FreeSlotResponse(
        person=person,
        day=day,
        duration_minutes=duration_minutes,
        available_slots=[FreeSlotItem(**s) for s in slots],
        calendar_events=events
    )

@app.get("/api/evidence")
def get_evidence(category: Optional[str] = None):
    """Fetches raw source evidence for auditing and verification."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if category:
        return {category: data.get(category)}
    return data

@app.get("/api/audit-log")
def audit_log(limit: int = 25):
    """Retrieves SQLite query logs."""
    return get_audit_logs(limit=limit)
