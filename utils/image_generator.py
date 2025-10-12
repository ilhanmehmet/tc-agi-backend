import requests
import base64
import os
from typing import Optional

HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN", "")
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def generate_image(prompt: str) -> Optional[str]:
    """Görüntü üret ve base64 döndür"""
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            image_bytes = response.content
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:image/png;base64,{base64_image}"
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
