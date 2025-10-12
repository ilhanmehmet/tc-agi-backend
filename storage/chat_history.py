import json
from datetime import datetime
from typing import List, Dict

class ChatHistory:
    def __init__(self):
        self.sessions = {}
    
    def add_message(self, session_id: str, role: str, content: str, metadata: dict = None):
        """Chat mesajı ekle"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.sessions[session_id].append(message)
        
        # Son 50 mesajı tut (hafıza tasarrufu)
        if len(self.sessions[session_id]) > 50:
            self.sessions[session_id] = self.sessions[session_id][-50:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Session geçmişini getir"""
        return self.sessions.get(session_id, [])
    
    def clear_session(self, session_id: str):
        """Session'ı temizle"""
        if session_id in self.sessions:
            del self.sessions[session_id]

# Global instance
chat_history = ChatHistory()
