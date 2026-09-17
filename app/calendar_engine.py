import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from .config import DATA_PATH

def load_calendar_data() -> Dict[str, Any]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("calendars", {})

def parse_time(time_str: str) -> datetime:
    return datetime.strptime(time_str.strip(), "%H:%M")

def format_time(dt: datetime) -> str:
    return dt.strftime("%H:%M")

def normalize_day(day_query: str) -> str:
    dq = day_query.lower().strip()
    if "mon" in dq or "21" in dq:
        return "Mon 21 Sep"
    if "tue" in dq or "22" in dq:
        return "Tue 22 Sep"
    if "wed" in dq or "23" in dq:
        return "Wed 23 Sep"
    if "thu" in dq or "24" in dq:
        return "Thu 24 Sep"
    if "fri" in dq or "25" in dq:
        return "Fri 25 Sep"
    return day_query

def get_person_events(person: str = "Arjun Malhotra", day: str = "Thu 24 Sep") -> List[Dict[str, Any]]:
    calendars = load_calendar_data()
    person_calendar = calendars.get(person, [])
    day_normalized = normalize_day(day)
    return [e for e in person_calendar if e["date"] == day_normalized]

def find_free_slots(
    person: str = "Arjun Malhotra",
    day: str = "Thu 24 Sep",
    duration_minutes: int = 30,
    work_start: str = "09:00",
    work_end: str = "18:00"
) -> List[Dict[str, Any]]:
    """
    Computes available slots of length `duration_minutes` within work_start and work_end
    excluding all scheduled meetings and blocked periods for the specified person.
    """
    events = get_person_events(person, day)
    
    # Sort events by start time
    sorted_events = sorted(events, key=lambda x: parse_time(x["start"]))
    
    start_boundary = parse_time(work_start)
    end_boundary = parse_time(work_end)
    slot_delta = timedelta(minutes=duration_minutes)
    
    available_slots = []
    current_cursor = start_boundary
    
    for event in sorted_events:
        ev_start = parse_time(event["start"])
        ev_end = parse_time(event["end"])
        
        # While there's room before the next meeting
        while current_cursor + slot_delta <= ev_start:
            slot_end = current_cursor + slot_delta
            available_slots.append({
                "day": normalize_day(day),
                "start": format_time(current_cursor),
                "end": format_time(slot_end),
                "duration_minutes": duration_minutes
            })
            # Advance in increments of duration or 30 mins
            current_cursor = slot_end
            
        if ev_end > current_cursor:
            current_cursor = ev_end
            
    # Remaining time after last event up to work_end
    while current_cursor + slot_delta <= end_boundary:
        slot_end = current_cursor + slot_delta
        available_slots.append({
            "day": normalize_day(day),
            "start": format_time(current_cursor),
            "end": format_time(slot_end),
            "duration_minutes": duration_minutes
        })
        current_cursor = slot_end
        
    return available_slots

def check_multi_person_availability(
    people: List[str],
    day: str = "Thu 24 Sep",
    duration_minutes: int = 30
) -> List[Dict[str, Any]]:
    """Find slots where ALL listed participants are free."""
    all_events = []
    day_norm = normalize_day(day)
    calendars = load_calendar_data()
    
    for p in people:
        p_events = [e for e in calendars.get(p, []) if e["date"] == day_norm]
        for e in p_events:
            all_events.append((parse_time(e["start"]), parse_time(e["end"]), f"{p}: {e['title']}"))
            
    all_events.sort(key=lambda x: x[0])
    
    cur = parse_time("09:00")
    end = parse_time("18:00")
    delta = timedelta(minutes=duration_minutes)
    free = []
    
    for ev_start, ev_end, _ in all_events:
        while cur + delta <= ev_start:
            free.append({
                "day": day_norm,
                "start": format_time(cur),
                "end": format_time(cur + delta),
                "duration_minutes": duration_minutes
            })
            cur += delta
        if ev_end > cur:
            cur = ev_end
            
    while cur + delta <= end:
        free.append({
            "day": day_norm,
            "start": format_time(cur),
            "end": format_time(cur + delta),
            "duration_minutes": duration_minutes
        })
        cur += delta
        
    return free
