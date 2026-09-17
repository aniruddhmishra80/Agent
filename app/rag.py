import json
import os
from typing import List, Dict, Any, Tuple
from pathlib import Path
from .config import DATA_PATH, CHROMA_DIR

# Global vector store cache
_vector_store = None
_all_documents = []

def extract_corpus() -> List[Dict[str, Any]]:
    """Extract granular, searchable documents from source_data.json."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    docs = []
    
    # 1. Meeting Transcript segments
    transcript = data.get("meeting_transcript", {})
    t_title = transcript.get("title", "Leadership Sync")
    t_date = transcript.get("date", "Monday 21 September 2026")
    t_time = transcript.get("time", "9:00-9:35 AM")
    for idx, d in enumerate(transcript.get("dialogue", [])):
        docs.append({
            "id": f"transcript_{idx}",
            "source": f"Transcript: {t_title} ({t_date} {t_time})",
            "type": "meeting_transcript",
            "speaker": d["speaker"],
            "text": f"[{t_title} - {t_date} {t_time}] {d['speaker']}: \"{d['text']}\""
        })
        
    # 2. Email Threads
    for thread in data.get("email_threads", []):
        subject = thread.get("subject", "General")
        for em in thread.get("emails", []):
            docs.append({
                "id": f"email_{subject}_{em.get('index', 0)}",
                "source": f"Email Thread: '{subject}' ({em.get('timestamp')})",
                "type": "email",
                "subject": subject,
                "from": em.get("from"),
                "to": em.get("to"),
                "text": f"[Email: {subject}] From: {em.get('from')} To: {em.get('to')} Date: {em.get('timestamp')} Body: \"{em.get('body')}\""
            })
            
    # 3. Voice Notes
    for vn in data.get("voice_notes", []):
        docs.append({
            "id": vn.get("id"),
            "source": f"Voice Note: {vn.get('context')}",
            "type": "voice_note",
            "speaker": vn.get("speaker"),
            "text": f"[Personal Voice Memo - {vn.get('context')}] {vn.get('speaker')}: \"{vn.get('transcript')}\""
        })
        
    # 4. Calendars
    for person, events in data.get("calendars", {}).items():
        for ev in events:
            docs.append({
                "id": f"cal_{person}_{ev['date']}_{ev['start']}",
                "source": f"Calendar: {person} ({ev['date']})",
                "type": "calendar",
                "person": person,
                "text": f"[Calendar: {person}] Date: {ev['date']} Time: {ev['start']}-{ev['end']} Event: \"{ev['title']}\""
            })
            
    return docs

def get_chroma_vector_store():
    """Initializes or loads persistent ChromaDB vector store with sentence-transformers."""
    global _vector_store, _all_documents
    if _vector_store is not None:
        return _vector_store

    docs = extract_corpus()
    _all_documents = docs
    
    try:
        from langchain_chroma import Chroma
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        persist_dir = str(CHROMA_DIR)
        os.makedirs(persist_dir, exist_ok=True)
        
        texts = [d["text"] for d in docs]
        metadatas = [{"source": d["source"], "type": d["type"], "id": d["id"]} for d in docs]
        
        # Load or create
        _vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            persist_directory=persist_dir,
            collection_name="executive_data_pack"
        )
        return _vector_store
    except Exception as e:
        print(f"[RAG WARNING] Chroma/SentenceTransformer initialization fallback: {e}")
        return None

def search_documents(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Searches documents using ChromaDB if available, or keyword matching fallback."""
    vstore = get_chroma_vector_store()
    
    if vstore is not None:
        try:
            results = vstore.similarity_search_with_score(query, k=top_k)
            ret = []
            for doc, score in results:
                ret.append({
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            return ret
        except Exception as err:
            print(f"[RAG Search Error] Falling back to text search: {err}")
            
    # Deterministic high-precision fallback
    docs = extract_corpus()
    query_terms = query.lower().split()
    scored = []
    for d in docs:
        t_low = d["text"].lower()
        score = sum(3 if term in t_low else 0 for term in query_terms)
        if any(term in d["source"].lower() for term in query_terms):
            score += 2
        if score > 0:
            scored.append((score, d))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"text": d["text"], "metadata": {"source": d["source"], "type": d["type"], "id": d["id"]}, "score": 1.0} for _, d in scored[:top_k]]
