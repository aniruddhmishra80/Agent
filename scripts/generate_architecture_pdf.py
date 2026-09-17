import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = BASE_DIR / "Executive_Productivity_Agent_Architecture.pdf"
ALT_OUTPUT_PDF = BASE_DIR / "ARCHITECTURE.pdf"

def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_navy = colors.HexColor("#0f172a")
    c_slate = colors.HexColor("#1e293b")
    c_cyan = colors.HexColor("#0284c7")
    c_light_bg = colors.HexColor("#f8fafc")
    c_border = colors.HexColor("#cbd5e1")
    c_red_text = colors.HexColor("#991b1b")
    c_red_bg = colors.HexColor("#fee2e2")
    c_green_text = colors.HexColor("#166534")
    c_green_bg = colors.HexColor("#dcfce7")
    c_amber_text = colors.HexColor("#92400e")
    c_amber_bg = colors.HexColor("#fef3c7")
    c_indigo_text = colors.HexColor("#3730a3")
    c_indigo_bg = colors.HexColor("#e0e7ff")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.white
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#94a3b8")
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#e2e8f0")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_navy,
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_slate,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        leftIndent=14,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0369a1")
    )

    story = []

    # 1. Header Banner Box
    header_data = [
        [
            Paragraph("AIONOS BATCH 2027 • ASSIGNMENT 1 TECHNICAL SPECIFICATION", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#38bdf8"))),
        ],
        [
            Paragraph("Executive Productivity Agent — System Architecture", title_style),
        ],
        [
            Paragraph("Autonomous Context Synthesis, Dynamic Drift Tracking & Strict Anti-Hallucination Architecture", subtitle_style),
        ],
        [
            Paragraph("<b>Candidate:</b> Aniruddh Mishra &nbsp;|&nbsp; <b>Institution:</b> Bennett University (B.Tech CSE) &nbsp;|&nbsp; <b>Target:</b> Arjun Malhotra (VP Sales) &nbsp;|&nbsp; <b>Horizon:</b> 21–25 Sep 2026", meta_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[540])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_navy),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # 2. Executive Summary
    story.append(Paragraph("1. Executive Summary & Design Philosophy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_cyan, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph(
        "The <b>Executive Productivity Agent</b> is an enterprise AI assistant designed for Arjun Malhotra, VP of Sales at Veridian Corp. "
        "Sales leaders operate under immense information fragmentation: commitments slip casually across email chains, meeting agreements evolve unrecorded, "
        "and critical administrative tasks float unassigned across departmental boundaries. "
        "Generic generative AI platforms are fundamentally unsuited for this workload because LLMs hallucinate ownership, assume authority where none exists, "
        "and fabricate status progress. To solve this, our architecture enforces a strict <b>Dual-Engine Hybrid Topology</b>:",
        body_style
    ))
    story.append(Paragraph("• <b>Deterministic Precedence Engine:</b> Guarantees mathematical and logical certainty over contractual obligations, explicit deadlines, and unowned tasks (e.g. Mumbai lease renewal). Zero hallucinations permitted.", bullet_style))
    story.append(Paragraph("• <b>Grounded Semantic RAG Engine:</b> Employs LangChain, ChromaDB dense vector indexing, Sentence-Transformers, and Google Gemini 1.5/3.6 Flash (temperature=0.0) with strict source attribution.", bullet_style))
    story.append(Spacer(1, 6))

    # 3. Component Architecture Breakdown
    story.append(Paragraph("2. End-to-End System Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_cyan, spaceBefore=2, spaceAfter=6))
    
    arch_table_data = [
        [
            Paragraph("<b>Ingestion & Normalization Layer</b>", h2_style),
            Paragraph("<b>Intelligence & Reasoning Layer</b>", h2_style),
            Paragraph("<b>Serving & Governance Layer</b>", h2_style)
        ],
        [
            Paragraph("• <b>Meeting Transcript:</b> 4-attendee Leadership Sync dialogue extraction.<br/>• <b>Calendars:</b> 4 distinct schedules (Arjun, Neha, Raghav, Divya).<br/>• <b>Email Inboxes:</b> 5 threads × 5 messages (25 total emails).<br/>• <b>Voice Notes:</b> 2 personal audio memos treated as internal commitments.<br/>• <b>Pydantic Validation:</b> Strict schema enforcement.", body_style),
            Paragraph("• <b>ChromaDB Vector Store:</b> Dense embeddings (<font face='Courier'>all-MiniLM-L6-v2</font>).<br/>• <b>Deterministic Guardrail Engine:</b> Precedence rules for unassigned items.<br/>• <b>Calendar Interval Calculator:</b> Mathematical focus window protector.<br/>• <b>LangChain Orchestrator:</b> Google Gemini 1.5/3.6 Flash zero-shot chain.", body_style),
            Paragraph("• <b>FastAPI REST API:</b> Endpoints for briefing, querying, and slot search.<br/>• <b>Streamlit Executive UI:</b> High-contrast dashboard with live filters.<br/>• <b>Vercel Serverless:</b> Stateless edge deployment (<font face='Courier'>api/index.py</font>).<br/>• <b>SQLite Audit Trail:</b> Query, model, and timestamp logs (<font face='Courier'>agent_audit.db</font>).", body_style)
        ]
    ]
    arch_table = Table(arch_table_data, colWidths=[180, 180, 180])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_light_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 8))

    # 4. Commitments Matrix Table
    story.append(Paragraph("3. Executive Deliverable & Commitment Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_cyan, spaceBefore=2, spaceAfter=6))
    
    commitments_data = [
        [
            Paragraph("<b>ID</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Deliverable</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Owner</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Deadline</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Status Badge</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Priority</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
        ],
        [
            Paragraph("COM-01", body_style),
            Paragraph("Updated Vendor List", body_style),
            Paragraph("Arjun Malhotra", body_style),
            Paragraph("Wed 23 Sep morning", body_style),
            Paragraph("<font color='#92400e'><b>AT RISK / OPEN</b></font>", body_style),
            Paragraph("HIGH", body_style),
        ],
        [
            Paragraph("COM-02", body_style),
            Paragraph("Q3 Campaign Deck Review", body_style),
            Paragraph("Arjun & Neha Kapoor", body_style),
            Paragraph("Thu 24 Sep, 9:30 AM", body_style),
            Paragraph("<font color='#3730a3'><b>SCHEDULED</b></font>", body_style),
            Paragraph("HIGH", body_style),
        ],
        [
            Paragraph("COM-03", body_style),
            Paragraph("July Expense Variance Report", body_style),
            Paragraph("Divya Rao", body_style),
            Paragraph("Wed 23 Sep evening", body_style),
            Paragraph("<font color='#166534'><b>COMPLETED</b></font>", body_style),
            Paragraph("MEDIUM", body_style),
        ],
        [
            Paragraph("COM-04", body_style),
            Paragraph("Meridian Logistics Call", body_style),
            Paragraph("Arjun & Priya Nair", body_style),
            Paragraph("Wed 23 Sep, 3:00 PM", body_style),
            Paragraph("<font color='#15803d'><b>CONFIRMED</b></font>", body_style),
            Paragraph("HIGH", body_style),
        ],
        [
            Paragraph("COM-05", body_style),
            Paragraph("Mumbai Office Lease Renewal", body_style),
            Paragraph("<b>UNASSIGNED</b>", body_style),
            Paragraph("Fri 25 Sep, End of Day", body_style),
            Paragraph("<font color='#991b1b'><b>CRITICAL / UNOWNED</b></font>", body_style),
            Paragraph("CRITICAL", body_style),
        ],
    ]
    com_table = Table(commitments_data, colWidths=[55, 140, 105, 95, 95, 50])
    com_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_navy),
        ('BOX', (0, 0), (-1, -1), 1, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(com_table)

    story.append(PageBreak())

    # 5. Case Studies Deep Dive
    story.append(Paragraph("4. Guardrail Logic & Evaluation Case Studies", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_cyan, spaceBefore=2, spaceAfter=6))

    # Case Study 1
    story.append(Paragraph("Case Study A: Safe Ambiguity Handling (The Mumbai Lease Renewal)", h2_style))
    story.append(Paragraph(
        "<b>The Ground Truth Scenario:</b> Facilities sent two all-staff alerts stating an authorized signature is due by Friday 25 Sep end-of-day. "
        "In the Monday sync, Divya speculated: <i>'I think that’s supposed to be Facilities, but I haven’t seen anyone pick it up.'</i><br/>"
        "<b>Executive Intervention:</b> Arjun explicitly ordered: <i>'Okay, flag it, don’t assume.'</i><br/>"
        "<b>Corroborating Facts:</b><br/>"
        "• On Wednesday 9:30 AM, Divya clarified via email that it sits with Facilities typically, but neither picked it up.<br/>"
        "• On Thursday 4:45 PM, Raghav confirmed: <i>'This is now one day out and still unowned — can you confirm who’s handling it?'</i><br/>"
        "• In Voice Note 1, Arjun noted: <i>'Someone needs to own that, I don’t think it’s me.'</i><br/>"
        "<b>Engineering Decision:</b> The agent strictly returns <b>UNASSIGNED / CRITICAL BLOCKER</b> and refuses to hallucinate Facilities as the owner. "
        "This protects leadership from assuming an urgent lease contract is managed when it is stalled.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Case Study 2
    story.append(Paragraph("Case Study B: Dynamic Deadline Drift (The Updated Vendor List)", h2_style))
    story.append(Paragraph(
        "<b>Timeline of Drift:</b><br/>"
        "1. <i>Monday 9:00 AM (Sync):</i> Arjun commits to sending Raghav the updated vendor list by end of day Tuesday.<br/>"
        "2. <i>Monday 5:40 PM (Email):</i> Arjun delays: <i>'Running behind, will send first thing tomorrow morning instead.'</i><br/>"
        "3. <i>Tuesday 6:30 PM (Email):</i> Arjun delays again: <i>'Sorry, got pulled into board prep — will send by tomorrow (Wednesday) morning for sure.'</i><br/>"
        "4. <i>Wednesday 8:45 AM (Email):</i> Raghav follows up: <i>'Just checking — still good for this morning?'</i><br/>"
        "<b>Engineering Decision:</b> Because no subsequent email records the file being sent, the agent classifies status as <b>AT RISK / OPEN (Overdue)</b> and raises an immediate action alert on Arjun's briefing.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 6. Calendar Engine
    story.append(Paragraph("5. Deterministic Calendar Intelligence Engine", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_cyan, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph(
        "LLMs frequently miscalculate time ranges when given multiple busy blocks. Our system computes availability mathematically "
        "via interval subtraction over working hours [09:00, 18:00]:",
        body_style
    ))
    story.append(Paragraph("<font face='Courier' color='#0284c7'><b>Available_Slots = [09:00, 18:00] \\ ⋃ (Event_Start_i, Event_End_i)</b></font>", body_style))
    story.append(Paragraph(
        "<b>Protected Focus Windows on Thursday 24 Sep:</b><br/>"
        "• <b>Board Prep Session (09:00 – 10:00 AM):</b> Inviolable focus block; protected from meeting booking.<br/>"
        "• <b>Neha's Campaign Deck Review (09:30 AM):</b> Scheduled to brief Arjun ahead of Board Prep.<br/>"
        "• <b>Hiring Panel (16:00 – 17:00 PM):</b> Blocked for interviewing sales candidates.<br/>"
        "• <b>Computed Free Windows:</b> Correctly isolates 14 collision-free 30-minute meeting slots between 10:00 and 16:00 and between 17:00 and 18:00.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # 7. Deployment & Compliance
    story.append(Paragraph("6. Governance, Observability & Cloud Deployment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_cyan, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph(
        "• <b>SQLite Audit Persistence (<font face='Courier'>agent_audit.db</font>):</b> Every incoming question, generated answer, engine type, and timestamp is stored permanently for corporate auditing.<br/>"
        "• <b>Vercel Serverless Architecture:</b> Configured via <font face='Courier'>vercel.json</font> and <font face='Courier'>api/index.py</font> with a lightweight package bundle (~38 MB) adhering to Vercel's 500 MB ceiling.<br/>"
        "• <b>Streamlit Community Cloud & Render:</b> High-contrast dashboard with zero-lag responsiveness deployed from GitHub.<br/>"
        "• <b>Zero Outbound Mutation Policy:</b> The agent drafts decisions and advises the VP of Sales, but requires explicit human confirmation before sending emails or updating Google/Outlook calendars.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Footer note
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph(
        "<i>Submitted for AIONOS Batch 2027 by Aniruddh Mishra (Bennett University) | Repository: github.com/aniruddhmishra80/Agent</i>",
        ParagraphStyle('Foot', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748b"), alignment=1)
    ))

    doc.build(story)
    print(f"[SUCCESS] Architecture PDF generated: {OUTPUT_PDF}")

    # Also save a copy as ARCHITECTURE.pdf
    import shutil
    shutil.copyfile(str(OUTPUT_PDF), str(ALT_OUTPUT_PDF))
    print(f"[SUCCESS] Copied to: {ALT_OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
