import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

class MemorySystem:
    def __init__(self):
        print("Loading multilingual embedding model...")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.knowledge_base = []
        self.load_index()
        print("✅ Memory system ready!")
    
    def add_knowledge(self, text: str, metadata: dict = None):
        """Add knowledge to memory"""
        embedding = self.encoder.encode([text])[0]
        self.index.add(np.array([embedding]))
        self.knowledge_base.append({"text": text, "metadata": metadata})
        self.save_index()
    
    def search(self, query: str, k: int = 3):
        """Search similar knowledge"""
        if len(self.knowledge_base) == 0:
            return []
        
        query_embedding = self.encoder.encode([query])[0]
        k = min(k, len(self.knowledge_base))  # Don't search for more than we have
        distances, indices = self.index.search(np.array([query_embedding]), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.knowledge_base):
                results.append({
                    "text": self.knowledge_base[idx]["text"],
                    "score": float(distances[0][i]),
                    "metadata": self.knowledge_base[idx].get("metadata")
                })
        return results
    
    def save_index(self):
        """Save index to disk"""
        os.makedirs("data/vector_db", exist_ok=True)
        faiss.write_index(self.index, "data/vector_db/faiss.index")
        with open("data/vector_db/knowledge.pkl", "wb") as f:
            pickle.dump(self.knowledge_base, f)
    
    def load_index(self):
        """Load index from disk"""
        if os.path.exists("data/vector_db/faiss.index"):
            self.index = faiss.read_index("data/vector_db/faiss.index")
            with open("data/vector_db/knowledge.pkl", "rb") as f:
                self.knowledge_base = pickle.load(f)
            print(f"Loaded {len(self.knowledge_base)} knowledge entries")

# Global instance
memory = MemorySystem()
