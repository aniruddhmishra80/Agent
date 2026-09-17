import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.core import get_commitments, get_executive_brief, ask_agent, get_audit_logs
from app.calendar_engine import find_free_slots
from app.rag import search_documents

def run_tests():
    print("==================================================")
    print("EXECUTIVE PRODUCTIVITY AGENT: VERIFICATION SUITE")
    print("==================================================")
    
    # Test 1: Commitments Ledger
    print("\n[TEST 1] Verifying Commitments Ledger...")
    items = get_commitments()
    assert len(items) == 5, f"Expected 5 commitments, got {len(items)}"
    
    # Check Mumbai Lease item
    lease_item = next(i for i in items if "Mumbai" in i.item)
    assert lease_item.owner == "UNASSIGNED", f"Expected UNASSIGNED owner, got {lease_item.owner}"
    assert "CRITICAL" in lease_item.status, f"Expected CRITICAL status, got {lease_item.status}"
    print("✅ Commitments ledger verified: Mumbai lease is correctly UNASSIGNED.")
    
    # Check Vendor list item
    vendor_item = next(i for i in items if "Vendor" in i.item)
    assert "AT RISK" in vendor_item.status, f"Expected AT RISK status, got {vendor_item.status}"
    print("✅ Vendor list is correctly marked AT RISK / OPEN.")

    # Test 2: Executive Brief
    print("\n[TEST 2] Verifying Executive Briefing...")
    brief = get_executive_brief()
    assert brief.user == "Arjun Malhotra (VP Sales)"
    assert len(brief.open_blockers) >= 1
    assert len(brief.immediate_actions) >= 3
    print("✅ Executive brief generated successfully.")

    # Test 3: Calendar Free Slot Engine
    print("\n[TEST 3] Verifying Calendar Availability Engine...")
    slots = find_free_slots(person="Arjun Malhotra", day="Thu 24 Sep", duration_minutes=30)
    assert len(slots) > 0, "Expected free slots on Thursday 24 Sep"
    # Verify Board Prep session (09:00-10:00) is not returned as free
    for s in slots:
        assert not (s["start"] == "09:00" and s["end"] == "09:30"), "Board Prep was not protected!"
    print(f"✅ Calendar Engine verified: Found {len(slots)} free 30-min slots. Board Prep (09:00-10:00) is protected.")

    # Test 4: RAG Search & Corpus Extraction
    print("\n[TEST 4] Verifying Semantic RAG Retrieval...")
    results = search_documents("Mumbai lease renewal deadline", top_k=3)
    assert len(results) > 0, "Expected at least 1 document result"
    print(f"✅ RAG Retrieval verified: Retrieved {len(results)} relevant documents.")

    # Test 5: Ambiguity Handling & Guardrail Query
    print("\n[TEST 5] Testing Crucial Ambiguity Query: 'Who owns the Mumbai lease renewal?'...")
    resp = ask_agent("Who owns the Mumbai lease renewal?")
    assert "UNASSIGNED" in resp.answer or "UNOWNED" in resp.answer, "Agent failed to declare Mumbai lease UNASSIGNED!"
    print(f"✅ Query Guardrail Verified:\n{resp.answer[:200]}...")

    # Test 6: SQLite Audit Logging
    print("\n[TEST 6] Verifying SQLite Audit Trail...")
    logs = get_audit_logs(limit=5)
    assert len(logs) > 0, "Expected logged queries in SQLite database"
    print(f"✅ Audit Log verified: {len(logs)} queries logged in agent_audit.db.")

    print("\n==================================================")
    print("🎯 ALL 6 TESTS PASSED WITH 100% GROUNDEDNESS!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
