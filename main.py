from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import logging

# TC-AGI Phoenix Core'u import et
try:
    from main_phoenix import PhoenixCore
    from api.agi_api import router as agi_router
    PHOENIX_AVAILABLE = True
except ImportError as e:
    print(f"Phoenix Core import hatası: {e}")
    PHOENIX_AVAILABLE = False

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API uygulamasını oluştur
app = FastAPI(title="TC-AGI Phoenix API", version="2.0.0")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Phoenix Core initialization
phoenix_core = None
if PHOENIX_AVAILABLE:
    try:
        phoenix_core = PhoenixCore()
        logger.info("TC-AGI Phoenix Core başlatıldı")
    except Exception as e:
        logger.error(f"Phoenix Core başlatma hatası: {e}")
        PHOENIX_AVAILABLE = False

# API Router'larını ekle
if PHOENIX_AVAILABLE:
    app.include_router(agi_router, prefix="/api/v1")

# Request modelleri
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class GenerateImageRequest(BaseModel):
    prompt: str
    size: str = "256x256"

# API Endpoints
@app.get("/")
async def root():
    status = "TC-AGI Phoenix Core Aktif" if PHOENIX_AVAILABLE else "TC-AGI Phoenix Core Kullanılamıyor"
    return {
        "message": f"TC-AGI Phoenix API - {status}",
        "version": "2.0.0",
        "phoenix_available": PHOENIX_AVAILABLE
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "environment": "production",
        "phoenix_core": "active" if PHOENIX_AVAILABLE else "inactive"
    }

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    if not PHOENIX_AVAILABLE:
        raise HTTPException(status_code=503, detail="Phoenix Core şu anda kullanılamıyor")
    
    try:
        # Phoenix Core ile işle
        response = await phoenix_core.process_message(request.message, request.session_id)
        return {
            "response": response,
            "session_id": request.session_id,
            "timestamp": "2024-01-01T00:00:00Z"  # Gerçek timestamp eklenebilir
        }
    except Exception as e:
        logger.error(f"Chat hatası: {e}")
        raise HTTPException(status_code=500, detail=f"İşlem hatası: {str(e)}")

@app.get("/api/v1/history/{session_id}")
async def get_history(session_id: str):
    if not PHOENIX_AVAILABLE:
        raise HTTPException(status_code=503, detail="Phoenix Core şu anda kullanılamıyor")
    
    try:
        # Geçmişi getir (basit implementasyon)
        return {
            "session_id": session_id,
            "messages": [
                {
                    "role": "system",
                    "content": "TC-AGI Phoenix Core aktif",
                    "timestamp": "2024-01-01T00:00:00Z"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geçmiş getirme hatası: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
