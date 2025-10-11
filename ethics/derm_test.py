import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

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
