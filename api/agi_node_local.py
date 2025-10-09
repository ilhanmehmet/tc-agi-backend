import os, time
from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "tc-agi-backend/models/llama3-8b.gguf")

# Modeli yükle
print("⏳ Model yükleniyor:", MODEL_PATH)
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    logits_all=True,
    n_threads=os.cpu_count() or 4,
    verbose=False
)
print("✅ Model hazır.")

app = FastAPI(title="GRSQM Local AGI Node", version="1.0")

class GenIn(BaseModel):
    prompt: str
    max_tokens: int | None = 256
    temperature: float | None = 0.7
    top_p: float | None = 0.95

@app.get("/health")
def health():
    return {"ok": True, "model": os.path.basename(MODEL_PATH)}

@app.post("/v1/generate")
def generate(payload: GenIn):
    t0 = time.time()
    out = llm.create_completion(
        prompt=payload.prompt,
        max_tokens=payload.max_tokens or 256,
        temperature=payload.temperature or 0.7,
        top_p=payload.top_p or 0.95
    )
    text = out["choices"][0]["text"]
    return {
        "ok": True,
        "latency_ms": int((time.time()-t0)*1000),
        "text": text.strip()
    }
