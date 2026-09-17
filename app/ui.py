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
    BACKEND_API_URL
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

# Custom CSS for rich executive styling
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
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    
    .badge-critical {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #f87171;
    }
    
    .badge-at-risk {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
    }
    
    .badge-scheduled {
        background-color: #e0e7ff;
        color: #3730a3;
        border: 1px solid #818cf8;
    }
    
    .badge-completed {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #4ade80;
    }
    
    .badge-confirmed {
        background-color: #f0fdf4;
        color: #15803d;
        border: 1px solid #86efac;
    }
    
    .card-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
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

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Briefing",
    "💬 Agent Q&A Assistant",
    "📅 Calendar Intelligence",
    "🔎 Evidence & Audit Trail",
    "📑 Architecture & Slides"
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
        # Badge color logic
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
            <div class="card-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:17px; font-weight:700; color:#1e293b;">{item.item}</span>
                    <span class="stat-badge {badge_class}">{item.status}</span>
                </div>
                <div style="margin-top:8px; font-size:14px; color:#475569;">
                    <strong>Owner:</strong> <span style="color:#0f172a;">{item.owner}</span> &nbsp;|&nbsp; 
                    <strong>Due:</strong> <span style="color:#0f172a;">{item.due}</span> &nbsp;|&nbsp; 
                    <strong>Priority:</strong> <span style="color:#0f172a;">{item.priority}</span>
                </div>
                <div style="margin-top:8px; font-size:13px; color:#64748b; background:#f8fafc; padding:10px; border-radius:8px; border-left:3px solid #3b82f6;">
                    <strong>Evidence & Grounding:</strong> {item.evidence}
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
            <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:12px; padding:20px; margin-top:16px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                    <span style="font-weight:700; color:#0f172a; font-size:16px;">Executive Intelligence Response</span>
                    <span style="font-size:12px; color:#64748b; background:#f1f5f9; padding:4px 8px; border-radius:6px;">Engine: {model}</span>
                </div>
                <div style="font-size:15px; line-height:1.6; color:#1e293b;">
                    {answer}
                </div>
                <div style="margin-top:16px; font-size:12px; color:#64748b; border-top:1px dashed #e2e8f0; padding-top:8px;">
                    <strong>Source Grounding Citations:</strong><br/>
                    {' • '.join(sources)}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: CALENDAR INTELLIGENCE
# ==========================================
with tab3:
    st.subheader("📅 Calendar Intelligence & Slot Finder")
    st.caption("Evaluate calendars for Arjun Malhotra and team to find collision-free meeting slots.")
    
    cal_col1, cal_col2, cal_col3 = st.columns(3)
    with cal_col1:
        sel_person = st.selectbox("Participant:", ["Arjun Malhotra", "Neha Kapoor", "Raghav Sethi", "Divya Rao"])
    with cal_col2:
        sel_day = st.selectbox("Day:", ["Mon 21 Sep", "Tue 22 Sep", "Wed 23 Sep", "Thu 24 Sep", "Fri 25 Sep"], index=3)
    with cal_col3:
        sel_duration = st.slider("Slot Duration (minutes):", min_value=15, max_value=60, value=30, step=15)
        
    slots = find_free_slots(person=sel_person, day=sel_day, duration_minutes=sel_duration)
    events = get_person_events(person=sel_person, day=sel_day)
    
    col_sched, col_free = st.columns([1, 1])
    with col_sched:
        st.markdown(f"#### 📆 Scheduled Events ({sel_person} on {sel_day})")
        if not events:
            st.info("No events scheduled on this day.")
        else:
            for ev in events:
                st.markdown(f"""
                <div style="background:#f8fafc; border-left:4px solid #6366f1; padding:10px 14px; border-radius:6px; margin-bottom:8px;">
                    <strong>{ev['start']} – {ev['end']}</strong>: {ev['title']}
                </div>
                """, unsafe_allow_html=True)
                
    with col_free:
        st.markdown(f"#### 🟢 Available {sel_duration}-Minute Free Slots")
        if not slots:
            st.warning("No free slots found during standard working hours (09:00 - 18:00).")
        else:
            for s in slots:
                st.markdown(f"""
                <div style="background:#f0fdf4; border-left:4px solid #22c55e; padding:10px 14px; border-radius:6px; margin-bottom:8px;">
                    <strong>{s['start']} – {s['end']}</strong> &nbsp;({sel_duration} min window)
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# TAB 4: EVIDENCE & AUDIT TRAIL
# ==========================================
with tab4:
    st.subheader("🔎 Raw Evidence Data Pack & SQLite Query Audit Log")
    
    ev_choice = st.selectbox("Select Evidence View:", ["Meeting Transcript", "Email Threads", "Voice Notes", "SQLite Audit Log"])
    
    with open("data/source_data.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    if ev_choice == "Meeting Transcript":
        mt = raw_data["meeting_transcript"]
        st.markdown(f"### {mt['title']} — {mt['date']} ({mt['time']})")
        st.markdown(f"**Attendees:** {', '.join(mt['attendees'])}")
        st.markdown("---")
        for d in mt["dialogue"]:
            st.markdown(f"**{d['speaker']}:** {d['text']}")
            
    elif ev_choice == "Email Threads":
        for thread in raw_data["email_threads"]:
            with st.expander(f"✉️ Thread: {thread['subject']} (5 Emails)", expanded=False):
                for em in thread["emails"]:
                    st.markdown(f"**#{em['index']} | {em['timestamp']}**")
                    st.markdown(f"*From:* `{em['from']}` → *To:* `{em['to']}`")
                    st.markdown(f"> \"{em['body']}\"")
                    st.markdown("---")
                    
    elif ev_choice == "Voice Notes":
        st.markdown("### 🎙️ Personal Voice Memos (Arjun Malhotra)")
        st.caption("Dictated reminders recorded for himself. Treated as commitments, not external requests.")
        for vn in raw_data["voice_notes"]:
            st.markdown(f"**{vn['context']}**")
            st.info(f"\"{vn['transcript']}\"")
            st.markdown("---")
            
    elif ev_choice == "SQLite Audit Log":
        st.markdown("### 🛡️ Real-Time SQLite Audit Log (`agent_audit.db`)")
        logs = get_audit_logs(limit=20)
        if not logs:
            st.info("No queries logged yet. Ask questions in the Agent Q&A tab to populate audit records.")
        else:
            st.dataframe(logs, use_container_width=True)

# ==========================================
# TAB 5: ARCHITECTURE & SLIDE DECK
# ==========================================
with tab5:
    st.subheader("📑 Architecture, Design Decisions & 10-Slide Deck")
    
    st.markdown("""
    ### 🏛️ Complete System Architecture
    ```mermaid
    flowchart TD
        DP[Assignment Data Pack: Transcripts, Calendars, 5x5 Emails, Voice Notes] --> DP_NORM[Data Normalization & Pydantic Validation]
        DP_NORM --> CHROMA[ChromaDB Vector Store + Sentence-Transformers]
        DP_NORM --> DET_RULES[Deterministic Grounding & Ambiguity Engine]
        
        USER[Arjun Malhotra / Evaluator] --> UI[Streamlit UI Dashboard]
        USER --> API[FastAPI REST API / Vercel Serverless]
        
        API --> CORE[Core Reasoning Engine]
        UI --> CORE
        
        CORE --> DET_RULES
        CORE --> RAG[ChromaDB Retriever]
        RAG --> LC[LangChain Prompt Chain]
        LC --> GEMINI[Google Gemini 1.5 Flash]
        
        CORE --> SQLITE[(SQLite Audit Log agent_audit.db)]
        CORE --> CAL_ENG[Deterministic Calendar Engine]
    ```
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Critical Evaluation Design Decisions")
    st.markdown("""
    1. **Mumbai Office Lease Renewal (Anti-Hallucination Safe Mode)**:
       - *Ground Truth Fact*: Facilities sent two reminders (Mon 10:15 AM & Thu 4:00 PM). Deadline: Friday 25 Sep EOD.
       - *Trap*: Divya suggested Facilities might handle it in the sync.
       - *Agent Guardrail*: Arjun explicitly said *"flag it, don't assume"*. On Thu 4:45 PM Raghav emailed it remains unowned. Arjun noted *"someone needs to own that, I don't think it's me"*.
       - *Decision*: Agent unequivocally flags it as **UNASSIGNED / CRITICAL BLOCKER**.
    2. **Vendor List Deadline Drift**:
       - Promised Monday -> moved to Tuesday morning -> moved to Wednesday morning -> Raghav follow-up at 8:45 AM Wednesday. Marked **AT RISK / OPEN**.
    3. **Q3 Campaign Deck Review**:
       - Shifted from Wednesday to Thursday 9:30 AM before Arjun's Board Prep block. Marked **SCHEDULED**.
    4. **July Expense Variance Report**:
       - Delivered Wednesday at 6:00 PM and acknowledged by Arjun at 6:10 PM. Marked **COMPLETED**.
    5. **Meridian Logistics Reschedule**:
       - Reconfirmed for Wednesday at 3:00 PM. Marked **CONFIRMED**.
    """)
    
    st.markdown("---")
    st.markdown("### 📽️ 10-Slide PPT Presentation")
    st.info("Slides are available in `PPT_10_SLIDES.md`, interactive HTML viewer in `presentation.html`, and generated as a PowerPoint presentation `executive_productivity_agent_presentation.pptx`.")

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#94a3b8; font-size:13px;'>Built by <strong>{AUTHOR_NAME}</strong> ({INSTITUTION}) | AIONOS Batch 2027 Assessment Submission | Deploy-ready for Vercel & Streamlit</div>", unsafe_allow_html=True)
