from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from utils.translator import translate_text
from utils.image_generator import generate_image
from utils.llama_model import llama_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_sessions = {}

class ChatRequest(BaseModel):
    query: str
    language: str = "en"
    session_id: Optional[str] = None

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "TC-AGI Backend Running!", "version": "7.0", "ai": "Llama-3 8B Active"}

@app.post("/api/v1/chat")
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # Build conversation context
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_sessions[session_id][-5:]])
    
    # Create Llama-3 prompt
    llama_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are TC-AGI, an advanced multilingual AI assistant. You are helpful, accurate, and ethical. Respond in {request.language} language.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{request.query}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""
    
    # Generate response with Llama-3
    ai_response = llama_model.generate(llama_prompt, max_tokens=512, temperature=0.7)
    
    # Translate if needed
    if request.language != "en":
        ai_response = translate_text(ai_response, "en", request.language)
    
    # Save to session
    chat_sessions[session_id].append({"role": "user", "content": request.query})
    chat_sessions[session_id].append({"role": "assistant", "content": ai_response})
    
    return {
        "response": ai_response,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/generate-image")
def create_image(request: ImageRequest):
    image_data = generate_image(request.prompt)
    if image_data:
        return {"success": True, "image": image_data}
    return {"success": False, "error": "Image generation failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
