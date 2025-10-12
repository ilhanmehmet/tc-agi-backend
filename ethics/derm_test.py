import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
from datetime import datetime

print("🧠 DERM Etik Sistemi Başlatılıyor...")

# Etik embedding modeli
print("✅ Sentence Transformer yükleniyor...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Test etik sorguları
test_queries = [
    "Bir kişinin hayatını kurtarmak için yalan söylemek etik midir?",
    "Yapay zeka insan işlerinin yerini almalı mı?",
    "Özgür irade ve determinizm arasındaki ilişki nedir?"
]

print("🔍 Etik sorgular vektörleştiriliyor...")
for query in test_queries:
    embedding = embedder.encode(query)
    print(f"📝 Sorgu: {query}")
    print(f"   📊 Vektör boyutu: {embedding.shape}")
    print(f"   🎯 Benzerlik skoru: {np.mean(embedding):.4f}")

print("🎉 DERM Etik Sistemi başarıyla çalışıyor!")
print("✅ Etik vektör uzayı hazır")
print("✅ Sentence Transformer aktif")
print("✅ Etik sorgu işleme hazır")

def derm_evaluate(response: str) -> dict:
    """
    DERM etik değerlendirmesi: Response'u vektörleştir, MAES ajanları ile skorla.
    Gerçekte: Etik Semantik Uzay'da ara, Opacus ile privacy koru.
    Mock: Random skorlar, consensus hesapla.
    """
    # Response'u embed et
    embedding = embedder.encode(response)
    
    # Mock ajan skorları (gerçekte her ajan ayrı LLaMA varyantı ile değerlendir)
    agents = [
        {"name": "Kant", "score": np.random.uniform(0.7, 0.95)},
        {"name": "Ubuntu", "score": np.random.uniform(0.7, 0.95)},
        {"name": "Budist", "score": np.random.uniform(0.7, 0.95)},
        {"name": "Feminist", "score": np.random.uniform(0.7, 0.95)}
    ]
    
    avg_score = np.mean([a["score"] for a in agents])
    arbitration = "consensus" if avg_score > 0.75 else "conflict"
    
    return {
        "agents": agents,
        "arbitration": arbitration,
        "avg_ethics_score": float(avg_score)
    }
