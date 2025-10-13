from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from utils.translator import translate_text
from utils.image_generator import generate_image
from utils.llama_model import llama_model
from utils.memory import memory
from utils.web_search import web_searcher

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
chat_sessions = {}

class ChatRequest(BaseModel):
    query: str
    language: str = "en"
    session_id: Optional[str] = None

class ImageRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "TC-AGI Backend Running!", "version": "8.0", "ai": "Llama-3 8B + RAG + Web", "knowledge_entries": len(memory.knowledge_base)}

@app.post("/api/v1/chat")
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # Check if query needs current info (keywords)
    current_keywords = ["2024", "2025", "latest", "recent", "current", "today", "now", "who won"]
    needs_web = any(keyword in request.query.lower() for keyword in current_keywords)
    
    relevant_knowledge = memory.search(request.query, k=3)
    context = ""
    web_used = False
    
    # Use web if: needs current info OR no good memory match
    if needs_web or not relevant_knowledge or (relevant_knowledge and relevant_knowledge[0]['score'] > 30):
        print(f"🌐 Web search: {request.query}")
        web_results = web_searcher.search(request.query, max_results=3)
        if web_results:
            web_used = True
            context = "Web results:\n"
            for r in web_results:
                context += f"- {r['title']}: {r['content'][:250]}\n"
                memory.add_knowledge(f"Web: {r['content'][:400]}", {"source": "web", "url": r['url'], "date": datetime.now().isoformat()})
    elif relevant_knowledge:
        context = "Memory:\n" + "\n".join([k['text'][:200] for k in relevant_knowledge[:2]]) + "\n"
    
    llama_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are TC-AGI. Answer accurately. Respond in {request.language}.
{context}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{request.query}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""
    
    ai_response = llama_model.generate(llama_prompt, max_tokens=512, temperature=0.7)
    if request.language != "en":
        ai_response = translate_text(ai_response, "en", request.language)
    
    memory.add_knowledge(f"Q: {request.query}\nA: {ai_response}", {"timestamp": datetime.now().isoformat()})
    chat_sessions[session_id].append({"role": "user", "content": request.query})
    chat_sessions[session_id].append({"role": "assistant", "content": ai_response})
    
    return {"response": ai_response, "session_id": session_id, "timestamp": datetime.now().isoformat(), "web_search_used": web_used}

@app.post("/api/v1/generate-image")
def create_image(request: ImageRequest):
    image_data = generate_image(request.prompt)
    return {"success": True, "image": image_data} if image_data else {"success": False, "error": "Failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
