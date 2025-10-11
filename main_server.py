"""
TC-AGI Backend Ana Sunucu - v6.0
Llama3-8B + DERM + Multimodal Hazır
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.agi_api import router as agi_router

app = FastAPI(
    title="TC-AGI Backend",
    description="Reflektif Evrensel AGI Platformu - Full Capacity",
    version="6.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agi_router, prefix="/api/v1", tags=["AGI Core"])

@app.get("/")
async def root():
    return {
        "name": "TC-AGI Backend",
        "version": "6.0",
        "status": "operational",
        "model": "Llama3-8B",
        "endpoints": {
            "chat": "/api/v1/chat",
            "health": "/api/v1/health"
        }
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TC-AGI BACKEND BASLATILIYOR...")
    print("=" * 60)
    print("📡 Model: Llama3-8B (4.9GB)")
    print("🔒 DERM Etik Sistemi: Aktif")
    print("🌐 Port: 8080")
    print("📍 URL: http://localhost:8080")
    print("📚 Docs: http://localhost:8080/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
