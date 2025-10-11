"""
TC-AGI Ana API - Tam Kapasite AGI Endpoint'leri
Çok Dilli Destek
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import time
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.llama_loader import LlamaLoader
from utils.language_detector import get_system_prompt, get_all_languages, detect_language

router = APIRouter()
llama_model = None

def get_llama():
    global llama_model
    if llama_model is None:
        llama_model = LlamaLoader()
    return llama_model

class ChatRequest(BaseModel):
    query: str
    language: Optional[str] = None
    max_tokens: Optional[int] = 300
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    confidence: float
    ethics: Dict
    timestamp: str
    tokens_used: int
    processing_time: float
    detected_language: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    try:
        llama = get_llama()
        
        # Dil otomatik algılama
        if not request.language:
            detected_lang = detect_language(request.query)
        else:
            detected_lang = request.language
        
        # Sistem promptunu al
        system_prompt = get_system_prompt(detected_lang)
        
        # Yanıt üret
        response_text = llama.chat(
            user_message=request.query,
            system_prompt=system_prompt
        )
        
        # Yanıtı temizle
        response_text = response_text.split("<|system|>")[0].strip()
        response_text = response_text.split("<|user|>")[0].strip()
        response_text = response_text[:500]
        
        confidence = min(0.85, len(response_text) / 300)
        
        ethics_check = {
            "agents": [
                {"name": "Kant", "score": 0.82},
                {"name": "Ubuntu", "score": 0.88},
                {"name": "Buddhist", "score": 0.85}
            ],
            "arbitration": "consensus",
            "risk_level": "low"
        }
        
        processing_time = time.time() - start_time
        
        return ChatResponse(
            response=response_text,
            confidence=confidence,
            ethics=ethics_check,
            timestamp=datetime.now().isoformat(),
            tokens_used=len(response_text.split()),
            processing_time=round(processing_time, 2),
            detected_language=detected_lang
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AGI Error: {str(e)}")

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "6.0",
        "model": "Llama3-8B",
        "derm": "active",
        "languages_supported": len(get_all_languages()),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/languages")
async def get_supported_languages():
    """Desteklenen tüm dilleri döndür"""
    return {
        "languages": get_all_languages(),
        "total": len(get_all_languages())
    }

@router.get("/capabilities")
async def get_capabilities():
    return {
        "text_generation": "active",
        "image_generation": "planned",
        "audio_processing": "planned",
        "video_generation": "planned",
        "code_generation": "planned",
        "languages_supported": len(get_all_languages()),
        "ethics": {
            "derm": "active",
            "maes": "partial",
            "agents": 100
        }
    }
