from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.translator import translate_text
from utils.language_detector import detect_language
import uvicorn
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "TC-AGI Backend Running!", "version": "6.0"}

@app.get("/api/v1/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/chat")
def chat(data: dict):
    query = data.get("query", "")
    user_lang = data.get("language", "tr")
    
    # Dil algıla
    detected_lang = detect_language(query)
    
    # Yanıt oluştur (şimdilik basit)
    response_en = f"Hello! I received your message: {query}. Backend is working but model not loaded yet."
    
    # Kullanıcının diline çevir
    response = translate_text(response_en, "en", user_lang)
    
    return {
        "response": response,
        "confidence_index": 0.5,
        "ethics": {
            "agents": [{"name": "Kant", "score": 0.78}, {"name": "Ubuntu", "score": 0.82}],
            "arbitration": "consensus"
        },
        "timestamp": datetime.now().isoformat(),
        "detected_language": detected_lang,
        "user_language": user_lang,
        "tokens_used": 10,
        "processing_time": 0.1
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
