from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI(title="TC-AGI Production", version="6.0")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend build dosyalarını servis et
app.mount("/static", StaticFiles(directory="../tc-agi-web/build/static"), name="static")
app.mount("/assets", StaticFiles(directory="../tc-agi-web/build/assets"), name="assets")

@app.get("/")
async def serve_frontend():
    return FileResponse("../tc-agi-web/build/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "6.0", "environment": "production"}

# Mevcut API endpoint'lerini buraya ekleyeceğiz

if __name__ == "__main__":
    print("🚀 TC-AGI Production Server Başlatılıyor...")
    print("📍 URL: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
