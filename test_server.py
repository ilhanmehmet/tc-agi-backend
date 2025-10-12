from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
    return {
        "response": "Merhaba! Ben TC-AGI. Backend çalışıyor ama model henüz yüklenmedi.",
        "confidence": 0.5,
        "ethics": {"arbitration": "test"},
        "timestamp": "2025-10-12T00:00:00",
        "tokens_used": 10,
        "processing_time": 0.1,
        "detected_language": "tr"
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
