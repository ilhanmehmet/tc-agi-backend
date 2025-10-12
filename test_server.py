from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.translator import translate_text
from utils.language_detector import detect_language
from storage.chat_history import chat_history
from auth.google_oauth import auth_manager
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
    return {"status": "TC-AGI Backend Running!", "version": "6.2"}

@app.post("/api/v1/auth/login")
def login(data: dict):
    """Kullanıcı login (Google OAuth simülasyonu)"""
    email = data.get("email")
    name = data.get("name", "User")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email required")
    
    token = auth_manager.create_token({"email": email, "name": name})
    return {"token": token, "user": {"email": email, "name": name}}

@app.post("/api/v1/chat")
def chat(data: dict, authorization: str = Header(None)):
    """Chat endpoint - opsiyonel auth"""
    query = data.get("query", "")
    user_lang = data.get("language", "tr")
    session_id = data.get("session_id") or str(uuid.uuid4())
    
    # Token varsa doğrula
    user = None
    if authorization:
        token = authorization.replace("Bearer ", "")
        user = auth_manager.verify_token(token)
    
    # Kullanıcı mesajını kaydet
    chat_history.add_message(session_id, "user", query, {"language": user_lang, "user": user})
    
    # Dil algıla ve yanıt oluştur
    detected_lang = detect_language(query)
    greeting = f"Hello {user['name']}!" if user else "Hello!"
    response_en = f"{greeting} I received your message: {query}. Backend is working but model not loaded yet."
    response = translate_text(response_en, "en", user_lang)
    
    # AI yanıtını kaydet
    chat_history.add_message(session_id, "assistant", response, {"language": user_lang})
    
    return {
        "response": response,
        "session_id": session_id,
        "user": user,
        "confidence_index": 0.5,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/history/{session_id}")
def get_history(session_id: str):
    history = chat_history.get_history(session_id)
    return {"session_id": session_id, "messages": history}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
