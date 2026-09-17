# 3-Minute Video Walkthrough Script & Technical Defense Guide

**Project:** Executive Productivity Agent (AIONOS Batch 2027)  
**Candidate:** Aniruddh Mishra (Bennett University)  
**Target User:** Arjun Malhotra, VP Sales (Veridian Corp)  

---

## 🎬 3-Minute Video Walkthrough Script

### Video Submission Checklist:
- **Length:** 2 to 3 minutes.
- **Recording Tool:** Windows Game Bar (`Win + Alt + R`), OBS Studio, or Loom.
- **Upload Target:** Google Drive (Set link permission to **"Anyone with the link can view"**).

---

### Step-by-Step Recording Plan

#### **[0:00 – 0:35] Scene 1: Introduction & Executive Briefing**
- **Action on Screen:** Open the Streamlit Dashboard (`http://localhost:8501`). Tab 1 ("📊 Executive Briefing") is displayed.
- **What to Say:**
  > *"Hello everyone. My name is Aniruddh Mishra from Bennett University, Batch 2027. Today, I am demonstrating the Executive Productivity Agent built for Arjun Malhotra, VP Sales at Veridian Corp, for AIONOS Assignment 1.*
  >
  > *In high-paced sales leadership, commitments and deadlines constantly drift across meeting transcripts, emails, and voice notes. Here in our Executive Briefing tab, you can immediately see all five tracked deliverables synthesized in real-time. Notice our top KPI metrics: 1 Critical Blocker, 1 At-Risk task, 2 Scheduled, and 1 Completed item."*

---

#### **[0:35 – 1:20] Scene 2: The Critical Ambiguity Test (Mumbai Lease)**
- **Action on Screen:** Click on Tab 2 ("💬 Agent Q&A Assistant"). Click the prompt chip: `Who owns the Mumbai lease renewal?`. Show the response.
- **What to Say:**
  > *"Now, let's demonstrate the agent's strict anti-hallucination guardrail. In our scenario, the Mumbai office lease renewal is due this Friday, September 25th. During the Monday sync, Divya casually guessed that Facilities might handle it.*
  >
  > *A naive AI would hallucinate Facilities as the owner. But our agent specifically notes that Arjun commanded 'flag it, don't assume', and Raghav confirmed on Thursday that it remains unowned. Therefore, as you can see on screen, our agent correctly flags ownership as UNASSIGNED / CRITICAL BLOCKER, preventing costly executive assumptions."*

---

#### **[1:20 – 1:55] Scene 3: Deadline Drift & Completed Deliverables**
- **Action on Screen:** Click the prompt chip: `What is the latest status of the vendor list?`. Then click: `What happened with the expense variance report?`.
- **What to Say:**
  > *"Next, we test dynamic deadline drift with the Vendor List. Arjun originally promised Raghav the list by Tuesday end-of-day, but slipped it to Wednesday morning. Raghav checked in at 8:45 AM Wednesday. Because no email shows it being sent, our agent flags it as AT RISK and Overdue.*
  >
  > *Conversely, for the July Expense Variance Report, Divya delivered it Wednesday at 6:00 PM and Arjun acknowledged receipt at 6:10 PM, so it is accurately classified as COMPLETED."*

---

#### **[1:55 – 2:30] Scene 4: Calendar Intelligence & Focus Protection**
- **Action on Screen:** Switch to Tab 3 ("📅 Calendar Intelligence"). Select `Arjun Malhotra`, `Thu 24 Sep`, duration `30 minutes`.
- **What to Say:**
  > *"Now let's examine our Calendar Intelligence Engine. If Arjun needs to schedule a 30-minute meeting on Thursday, the engine protects his Board Prep Session from 9 to 10 AM, accounts for Neha's 9:30 AM Campaign Deck Review, and isolates available slots throughout the day with zero schedule collisions."*

---

#### **[2:30 – 3:00] Scene 5: Auditability, Architecture & Wrap-up**
- **Action on Screen:** Click Tab 4 ("🔎 Evidence & Audit Trail") and show the SQLite Audit Log. Show the FastAPI `/docs` page or Terminal running uvicorn.
- **What to Say:**
  > *"Finally, enterprise systems require total accountability. Every query, response, and model engine is permanently recorded in our SQLite audit log. The entire solution is deploy-ready on Vercel via FastAPI serverless functions, and backed by ChromaDB and LangChain.*
  >
  > *Thank you for your time, and I look forward to walking through the architecture in the technical interview round!"*

---

## 🛡️ Technical Defense & Interview Preparation

### Question 1: Why did your agent declare the Mumbai lease owner as "UNASSIGNED" instead of "Facilities"?
**Answer:**
> *"In the Monday Leadership Sync, Divya stated: 'I think that’s supposed to be Facilities, but I haven't seen anyone pick it up.' Arjun immediately intervened: 'Okay, flag it, don't assume.' Later in the week, Raghav sent a follow-up email on Thursday at 4:45 PM explicitly stating: 'This is now one day out and still unowned — can you confirm who’s handling it?' Furthermore, Arjun's personal voice note confirms 'someone needs to own that, I don't think it's me.' Grounding an agent in truth means refusing to invent an owner when the source data proves nobody has accepted ownership."*

### Question 2: How does your architecture guarantee zero hallucinations?
**Answer:**
> *"We implement a dual-layer strategy: High-stakes corporate compliance and contractual deliverables pass through a deterministic precedence engine with explicit source validation. For open-ended natural language queries, we use LangChain RAG with dense ChromaDB retrieval, passing only retrieved source chunks into Google Gemini 1.5 Flash with temperature set to 0.0 and system instructions forbidding factual extrapolation."*

### Question 3: How is this system made deploy-ready for Vercel?
**Answer:**
> *"We structured the backend with a standardized Vercel Python serverless configuration in `vercel.json` pointing to `api/index.py`. The FastAPI application exposes modular REST endpoints (`/api/brief`, `/api/query`, `/api/calendar/free-slots`) that scale statelessly on edge infrastructure."*
