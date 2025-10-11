from llama_cpp import Llama
import os

class LlamaLoader:
    def __init__(self, model_path="models/llama3-8b.gguf"):
        print("🧠 Llama3-8B yükleniyor...")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model bulunamadı: {model_path}")
        self.llm = Llama(model_path=model_path, n_ctx=4096, n_threads=4, n_gpu_layers=0, verbose=False)
        print("✅ Llama3-8B yüklendi!")
    
    def chat(self, user_message: str, system_prompt: str = "Sen yardımcı bir asistansın."):
        prompt = f"{system_prompt}\n\nSoru: {user_message}\n\nYanıt:"
        response = self.llm(prompt, max_tokens=400, temperature=0.7, stop=["</s>", "Soru:", "\n\n"])
        return response['choices'][0]['text'].strip()
