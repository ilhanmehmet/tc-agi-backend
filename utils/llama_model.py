from llama_cpp import Llama
import os

class LlamaModel:
    def __init__(self):
        self.llm = None
        self.load_model()
    
    def load_model(self):
        """Load Llama-3 model"""
        try:
            model_path = "models/llama-3-8b-instruct-q4.gguf"
            if not os.path.exists(model_path):
                print(f"Model not found: {model_path}")
                return
            
            print("Loading Llama-3 8B model...")
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=4,
                verbose=False
            )
            print("✅ Llama-3 model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.llm = None
    
    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        """Generate response from Llama-3"""
        if not self.llm:
            return "Model not loaded. Please check backend logs."
        
        try:
            response = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["User:", "\n\nUser:", "<|eot_id|>"]
            )
            return response['choices'][0]['text'].strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Global instance
llama_model = LlamaModel()
