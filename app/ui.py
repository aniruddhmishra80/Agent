import sys
from pathlib import Path

# Ensure repository root is on sys.path for Streamlit Cloud & remote containers
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import json
import requests
from datetime import datetime

from app.config import (
    AUTHOR_NAME,
    INSTITUTION,
    COHORT,
    ASSIGNMENT_TITLE,
    TARGET_USER,
    SCENARIO_WEEK,
    BACKEND_API_URL,
    DATA_PATH
)
from app.core import (
    get_executive_brief,
    get_commitments,
    ask_agent,
    get_audit_logs
)
from app.calendar_engine import find_free_slots, get_person_events, load_calendar_data

# Streamlit Page Config
st.set_page_config(
    page_title="Executive Productivity Agent | AIONOS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich executive styling (Theme-proof with explicit contrast)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 4px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 15px;
        margin-bottom: 12px;
    }
    
    .stat-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-right: 8px;
    }
    
    .badge-critical {
        background-color: #7f1d1d;
        color: #fecaca;
        border: 1px solid #ef4444;
    }
    
    .badge-at-risk {
        background-color: #78350f;
        color: #fde68a;
        border: 1px solid #f59e0b;
    }
    
    .badge-scheduled {
        background-color: #312e81;
        color: #c7d2fe;
        border: 1px solid #6366f1;
    }
    
    .badge-completed {
        background-color: #14532d;
        color: #bbf7d0;
        border: 1px solid #22c55e;
    }
    
    .badge-confirmed {
        background-color: #064e3b;
        color: #a7f3d0;
        border: 1px solid #10b981;
    }
    
    /* Theme-proof Dark Card for High Contrast */
    .dark-card {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    .slot-card {
        background-color: #0b1329 !important;
        border: 1px solid #1e3a8a !important;
        border-left: 5px solid #10b981 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        color: #ffffff !important;
        transition: transform 0.15s ease;
    }
    
    .slot-card:hover {
        transform: translateY(-2px);
        border-color: #38bdf8 !important;
    }
    
    .event-card {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
        border-left: 5px solid #818cf8 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/artificial-intelligence.png", width=64)
    st.markdown("### **Executive Agent Hub**")
    st.markdown(f"**User:** `{TARGET_USER}`")
    st.markdown(f"**Period:** `{SCENARIO_WEEK}`")
    st.markdown(f"**Candidate:** `{AUTHOR_NAME}`")
    st.markdown(f"**Batch:** `{COHORT}`")
    st.markdown("---")
    
    st.markdown("#### 🛡️ Anti-Hallucination Guardrails")
    st.info("✅ Strictly Grounded in Data Pack\n\n✅ Mumbai Lease marked **UNASSIGNED**\n\n✅ Zero Phantom Deadlines\n\n✅ Complete Audit Trail")
    
    st.markdown("---")
    backend_mode = st.radio("Execution Backend", ["Integrated Core (Direct)", "FastAPI REST Client"], index=0)
    st.caption("Deploy ready for Vercel & Streamlit Cloud")

# Header Banner
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">⚡ Executive Productivity Agent</div>
    <div class="hero-subtitle">Intelligent Commitment Tracker, Calendar Intelligence & Decision Support for {TARGET_USER}</div>
    <div>
        <span class="stat-badge" style="background:#1e293b; color:#38bdf8; border:1px solid #0284c7;">AIONOS Batch 2027</span>
        <span class="stat-badge" style="background:#1e293b; color:#a78bfa; border:1px solid #7c3aed;">Bennett University - {AUTHOR_NAME}</span>
        <span class="stat-badge" style="background:#1e293b; color:#34d399; border:1px solid #059669;">Scenario: 21-25 Sep 2026</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs (Removed Architecture & Presentation tab as requested)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Briefing",
    "💬 Agent Q&A Assistant",
    "📅 Calendar Intelligence",
    "🔎 Evidence & Audit Trail"
])

# ==========================================
# TAB 1: EXECUTIVE BRIEFING
# ==========================================
with tab1:
    st.subheader("🎯 Executive Situation & Commitment Ledger")
    brief = get_executive_brief()
    
    # Top KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Total Tracked", value="5 Items")
    with col2:
        st.metric(label="Critical Blockers", value="1 Item", delta="-1 Unowned", delta_color="inverse")
    with col3:
        st.metric(label="At Risk / Overdue", value="1 Item", delta="-1 Attention", delta_color="inverse")
    with col4:
        st.metric(label="Scheduled", value="2 Items", delta="On Track")
    with col5:
        st.metric(label="Completed", value="1 Item", delta="Done")
        
    st.markdown("---")
    
    # Urgent Callouts
    c_left, c_right = st.columns([3, 2])
    with c_left:
        st.markdown("#### 🚨 Immediate Executive Actions")
        for act in brief.immediate_actions:
            if "ACTION REQUIRED" in act:
                st.error(act)
            elif "PREPARE" in act:
                st.warning(act)
            else:
                st.success(act)
                
    with c_right:
        st.markdown("#### ⚠️ Open Blockers")
        for blk in brief.open_blockers:
            st.warning(f"**•** {blk}")
            
    st.markdown("### 📋 Commitment & Deliverable Ledger")
    
    # Filter controls
    f_col1, f_col2 = st.columns([2, 2])
    with f_col1:
        status_filter = st.selectbox(
            "Filter by Status:",
            ["All Deliverables", "CRITICAL / UNOWNED", "AT RISK / OPEN", "SCHEDULED", "CONFIRMED", "COMPLETED"]
        )
        
    items = brief.commitments
    if status_filter != "All Deliverables":
        items = [i for i in items if status_filter in i.status]
        
    for item in items:
        badge_class = "badge-scheduled"
        if "CRITICAL" in item.status:
            badge_class = "badge-critical"
        elif "AT RISK" in item.status:
            badge_class = "badge-at-risk"
        elif "COMPLETED" in item.status:
            badge_class = "badge-completed"
        elif "CONFIRMED" in item.status:
            badge_class = "badge-confirmed"
            
        with st.container():
            st.markdown(f"""
            <div class="dark-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:17px; font-weight:700; color:#ffffff;">{item.item}</span>
                    <span class="stat-badge {badge_class}">{item.status}</span>
                </div>
                <div style="margin-top:10px; font-size:14px; color:#cbd5e1;">
                    <strong style="color:#94a3b8;">Owner:</strong> <span style="color:#38bdf8; font-weight:600;">{item.owner}</span> &nbsp;|&nbsp; 
                    <strong style="color:#94a3b8;">Due:</strong> <span style="color:#f8fafc; font-weight:600;">{item.due}</span> &nbsp;|&nbsp; 
                    <strong style="color:#94a3b8;">Priority:</strong> <span style="color:#f8fafc; font-weight:600;">{item.priority}</span>
                </div>
                <div style="margin-top:10px; font-size:13px; color:#94a3b8; background:#1e293b; padding:12px; border-radius:8px; border-left:3px solid #38bdf8;">
                    <strong style="color:#38bdf8;">Evidence & Grounding:</strong> {item.evidence}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 2: AGENT Q&A ASSISTANT
# ==========================================
with tab2:
    st.subheader("💬 AI Executive Assistant (Source Grounded)")
    st.caption("Ask questions about Arjun's commitments, meeting actions, deadlines, calendar slots, and critical unowned items.")
    
    # Pre-built Prompt Chips
    st.markdown("**⚡ Sample Executive Queries:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    sample_q = None
    with q_col1:
        if st.button("🏢 Who owns the Mumbai lease renewal?"):
            sample_q = "Who owns the Mumbai lease renewal?"
        if st.button("📋 What is the latest status of the vendor list?"):
            sample_q = "What is the latest status of the vendor list?"
    with q_col2:
        if st.button("📊 When is the campaign deck review?"):
            sample_q = "When is the campaign deck review?"
        if st.button("📞 Is the Meridian client call confirmed?"):
            sample_q = "Is the Meridian client call confirmed?"
    with q_col3:
        if st.button("💰 What happened with the expense variance report?"):
            sample_q = "What happened with the expense variance report?"
        if st.button("📅 Find free 30-minute slots on Thursday."):
            sample_q = "Find free 30-minute slots on Thursday."
            
    # Input box
    user_query = st.text_input("Enter your executive question:", value=sample_q if sample_q else "")
    
    if st.button("Ask Executive Agent", type="primary") or sample_q:
        if user_query:
            with st.spinner("Analyzing ground truth scenario data..."):
                if backend_mode == "FastAPI REST Client":
                    try:
                        res = requests.post(
                            f"{BACKEND_API_URL}/api/query",
                            json={"query": user_query, "mode": "hybrid"},
                            timeout=8
                        )
                        data = res.json()
                        answer = data["answer"]
                        model = data["model_used"]
                        sources = data.get("evidence_sources", [])
                    except Exception as err:
                        st.warning(f"FastAPI not reached ({err}). Falling back to local integrated engine.")
                        resp = ask_agent(user_query)
                        answer = resp.answer
                        model = resp.model_used
                        sources = resp.evidence_sources
                else:
                    resp = ask_agent(user_query)
                    answer = resp.answer
                    model = resp.model_used
                    sources = resp.evidence_sources
                    
            st.markdown(f"""
            <div class="dark-card" style="border:1px solid #0284c7 !important;">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="font-weight:700; color:#38bdf8; font-size:16px;">Executive Intelligence Response</span>
                    <span style="font-size:12px; color:#94a3b8; background:#1e293b; padding:4px 10px; border-radius:6px; border:1px solid #334155;">Engine: {model}</span>
                </div>
                <div style="font-size:15px; line-height:1.6; color:#f8fafc;">
                    {answer}
                </div>
                <div style="margin-top:16px; font-size:12px; color:#94a3b8; border-top:1px dashed #334155; padding-top:10px;">
                    <strong style="color:#38bdf8;">Source Grounding Citations:</strong><br/>
                    {' • '.join(sources)}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: CALENDAR INTELLIGENCE (ENHANCED & HIGH CONTRAST)
# ==========================================
with tab3:
    st.subheader("📅 Calendar Intelligence & Meeting Slot Discovery")
    st.caption("Deterministic time analysis across executive calendars. Zero collisions, protected focus blocks.")
    
    # Controls row
    cal_col1, cal_col2, cal_col3 = st.columns(3)
    with cal_col1:
        sel_person = st.selectbox("Select Participant:", ["Arjun Malhotra", "Neha Kapoor", "Raghav Sethi", "Divya Rao"])
    with cal_col2:
        sel_day = st.selectbox("Select Scenario Day:", ["Mon 21 Sep", "Tue 22 Sep", "Wed 23 Sep", "Thu 24 Sep", "Fri 25 Sep"], index=3)
    with cal_col3:
        sel_duration = st.slider("Required Slot Length (Minutes):", min_value=15, max_value=60, value=30, step=15)
        
    slots = find_free_slots(person=sel_person, day=sel_day, duration_minutes=sel_duration)
    events = get_person_events(person=sel_person, day=sel_day)
    
    # Overview Stat Badges
    st.markdown(f"""
    <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:14px 20px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span style="color:#94a3b8; font-size:13px; font-weight:600;">ACTIVE SCHEDULE:</span> 
            <strong style="color:#ffffff; font-size:15px; margin-left:6px;">{sel_person}</strong> 
            <span style="color:#64748b; margin:0 8px;">|</span>
            <span style="color:#38bdf8; font-weight:600;">{sel_day} (09:00 – 18:00)</span>
        </div>
        <div>
            <span style="background:#0f172a; color:#818cf8; border:1px solid #6366f1; padding:4px 12px; border-radius:15px; font-size:13px; font-weight:700; margin-right:8px;">
                📅 {len(events)} Scheduled Events
            </span>
            <span style="background:#064e3b; color:#34d399; border:1px solid #10b981; padding:4px 12px; border-radius:15px; font-size:13px; font-weight:700;">
                🟢 {len(slots)} Free Windows Found
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_sched, col_free = st.columns([1, 1])
    
    # Left Column: Scheduled Events
    with col_sched:
        st.markdown(f"#### 🔒 Scheduled & Protected Events ({len(events)})")
        if not events:
            st.info(f"No events scheduled for {sel_person} on {sel_day}.")
        else:
            for ev in events:
                is_blocked = "block" in ev['title'].lower() or "prep" in ev['title'].lower() or "sync" in ev['title'].lower()
                border_color = "#f59e0b" if is_blocked else "#818cf8"
                badge_text = "🔒 Focus / Blocked" if is_blocked else "👥 Meeting"
                badge_bg = "rgba(245, 158, 11, 0.15)" if is_blocked else "rgba(129, 140, 248, 0.15)"
                badge_color = "#fcd34d" if is_blocked else "#c7d2fe"
                
                st.markdown(f"""
                <div class="event-card" style="border-left: 5px solid {border_color} !important;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:16px; font-weight:700; color:#ffffff;">{ev['title']}</span>
                        <span style="background:{badge_bg}; color:{badge_color}; border:1px solid {border_color}; padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700;">
                            {badge_text}
                        </span>
                    </div>
                    <div style="margin-top:8px; display:flex; align-items:center; gap:8px;">
                        <span style="background:#1e293b; color:#38bdf8; padding:4px 10px; border-radius:6px; font-family:monospace; font-weight:700; font-size:13px;">
                            ⏰ {ev['start']} – {ev['end']}
                        </span>
                        <span style="color:#94a3b8; font-size:13px;">
                            Duration: {int((datetime.strptime(ev['end'], '%H:%M') - datetime.strptime(ev['start'], '%H:%M')).total_seconds() / 60)} mins
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    # Right Column: Available Free Slots (HIGH CONTRAST & CLEARLY VISIBLE)
    with col_free:
        st.markdown(f"#### 🟢 Available {sel_duration}-Minute Slots ({len(slots)})")
        if not slots:
            st.error(f"No available {sel_duration}-minute slots found between 09:00 and 18:00.")
        else:
            # Slot filter chips
            filter_mode = st.radio(
                "Filter Slots:",
                ["All Open Slots", "Morning (09:00 - 13:00)", "Afternoon (13:00 - 18:00)"],
                horizontal=True
            )
            
            filtered_slots = slots
            if filter_mode == "Morning (09:00 - 13:00)":
                filtered_slots = [s for s in slots if s['start'] < "13:00"]
            elif filter_mode == "Afternoon (13:00 - 18:00)":
                filtered_slots = [s for s in slots if s['start'] >= "13:00"]
                
            if not filtered_slots:
                st.warning(f"No open slots in the selected {filter_mode} window.")
            else:
                for idx, s in enumerate(filtered_slots, 1):
                    st.markdown(f"""
                    <div class="slot-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="display:flex; align-items:center; gap:10px;">
                                <span style="background:#064e3b; color:#34d399; font-weight:800; padding:4px 10px; border-radius:6px; font-size:13px;">
                                    #{idx}
                                </span>
                                <span style="font-size:17px; font-weight:800; color:#38bdf8; letter-spacing:0.5px; font-family:monospace;">
                                    ⏰ {s['start']} – {s['end']}
                                </span>
                            </div>
                            <span style="background:#064e3b; color:#34d399; border:1px solid #10b981; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:700;">
                                ✓ Available
                            </span>
                        </div>
                        <div style="margin-top:8px; font-size:13px; color:#cbd5e1; display:flex; justify-content:space-between;">
                            <span>Window Length: <strong style="color:#ffffff;">{sel_duration} minutes</strong></span>
                            <span style="color:#10b981; font-weight:600;">✓ Conflict-Free</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
# TAB 4: EVIDENCE & AUDIT TRAIL
# ==========================================
with tab4:
    st.subheader("🔎 Raw Evidence Data Pack & SQLite Query Audit Log")
    
    ev_choice = st.selectbox("Select Evidence View:", ["Meeting Transcript", "Email Threads", "Voice Notes", "SQLite Audit Log"])
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    if ev_choice == "Meeting Transcript":
        mt = raw_data["meeting_transcript"]
        st.markdown(f"### {mt['title']} — {mt['date']} ({mt['time']})")
        st.markdown(f"**Attendees:** {', '.join(mt['attendees'])}")
        st.markdown("---")
        for d in mt["dialogue"]:
            st.markdown(f"""
            <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; padding:12px 16px; margin-bottom:8px; color:#ffffff;">
                <strong style="color:#38bdf8;">{d['speaker']}:</strong> <span style="color:#f8fafc;">"{d['text']}"</span>
            </div>
            """, unsafe_allow_html=True)
            
    elif ev_choice == "Email Threads":
        for thread in raw_data["email_threads"]:
            with st.expander(f"✉️ Thread: {thread['subject']} (5 Emails)", expanded=False):
                for em in thread["emails"]:
                    st.markdown(f"""
                    <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; padding:14px; margin-bottom:10px; color:#ffffff;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                            <span style="color:#38bdf8; font-weight:700;">#{em['index']} | {em['timestamp']}</span>
                            <span style="color:#94a3b8; font-size:12px;">From: {em['from']} → To: {em['to']}</span>
                        </div>
                        <div style="color:#f8fafc; font-size:14px; line-height:1.5;">
                            "{em['body']}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
    elif ev_choice == "Voice Notes":
        st.markdown("### 🎙️ Personal Voice Memos (Arjun Malhotra)")
        st.caption("Dictated reminders recorded for himself. Treated as commitments, not external requests.")
        for vn in raw_data["voice_notes"]:
            st.markdown(f"""
            <div style="background:#0f172a; border:1px solid #334155; border-left:4px solid #a855f7; border-radius:8px; padding:16px; margin-bottom:12px; color:#ffffff;">
                <div style="color:#c084fc; font-weight:700; font-size:15px; margin-bottom:6px;">🎙️ {vn['context']}</div>
                <div style="color:#f8fafc; font-size:14px; font-style:italic;">"{vn['transcript']}"</div>
            </div>
            """, unsafe_allow_html=True)
            
    elif ev_choice == "SQLite Audit Log":
        st.markdown("### 🛡️ Real-Time SQLite Audit Log (`agent_audit.db`)")
        logs = get_audit_logs(limit=20)
        if not logs:
            st.info("No queries logged yet. Ask questions in the Agent Q&A tab to populate audit records.")
        else:
            st.dataframe(logs, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#94a3b8; font-size:13px;'>Built by <strong>{AUTHOR_NAME}</strong> ({INSTITUTION}) | AIONOS Batch 2027 Assessment Submission | Deploy-ready for Vercel & Streamlit</div>", unsafe_allow_html=True)
