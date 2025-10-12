from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.translator import translate_text
from utils.language_detector import detect_language
from storage.chat_history import chat_history
import uvicorn
from datetime import datetime
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "TC-AGI Backend Running!", "version": "6.1"}

@app.get("/api/v1/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/chat")
def chat(data: dict):
    query = data.get("query", "")
    user_lang = data.get("language", "tr")
    session_id = data.get("session_id") or str(uuid.uuid4())
    
    # Kullanıcı mesajını kaydet
    chat_history.add_message(session_id, "user", query, {"language": user_lang})
    
    # Dil algıla
    detected_lang = detect_language(query)
    
    # Yanıt oluştur
    response_en = f"Hello! I received your message: {query}. Backend is working but model not loaded yet."
    response = translate_text(response_en, "en", user_lang)
    
    # AI yanıtını kaydet
    chat_history.add_message(session_id, "assistant", response, {"language": user_lang})
    
    return {
        "response": response,
        "session_id": session_id,
        "confidence_index": 0.5,
        "ethics": {
            "agents": [{"name": "Kant", "score": 0.78}, {"name": "Ubuntu", "score": 0.82}],
            "arbitration": "consensus"
        },
        "timestamp": datetime.now().isoformat(),
        "detected_language": detected_lang,
        "user_language": user_lang
    }

@app.get("/api/v1/history/{session_id}")
def get_history(session_id: str):
    """Chat geçmişini getir"""
    history = chat_history.get_history(session_id)
    return {"session_id": session_id, "messages": history}

@app.delete("/api/v1/history/{session_id}")
def delete_history(session_id: str):
    """Chat geçmişini sil"""
    chat_history.clear_session(session_id)
    return {"status": "deleted", "session_id": session_id}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
