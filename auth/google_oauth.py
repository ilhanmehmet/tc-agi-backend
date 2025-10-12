from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt
import uuid

SECRET_KEY = "tc-agi-secret-key-change-in-production"
ALGORITHM = "HS256"

class AuthManager:
    def __init__(self):
        self.users = {}  # user_id: {email, name, picture}
    
    def create_token(self, user_data: dict) -> str:
        """JWT token oluştur"""
        user_id = str(uuid.uuid4())
        self.users[user_id] = user_data
        
        payload = {
            "user_id": user_id,
            "email": user_data.get("email"),
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    def verify_token(self, token: str) -> dict:
        """Token doğrula"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            return self.users.get(user_id)
        except:
            raise HTTPException(status_code=401, detail="Invalid token")

auth_manager = AuthManager()
