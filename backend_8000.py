from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI(title="TC-AGI", version="6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str
    language: str = "tr"

@app.get("/")
async def root():
    return {"message": "TC-AGI Backend Aktif", "port": 8000}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.post("/query")
async def query(request: Query):
    return {
        "response": f"TC-AGI: '{request.query}' sorgunuz işlendi (Port 8000)",
        "confidence": 0.85,
        "ethics": {"agents": [], "arbitration": "consensus"},
        "timestamp": str(datetime.now())
    }

if __name__ == "__main__":
    print("🚀 TC-AGI Backend Port 8000'de başlıyor...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
