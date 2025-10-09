import os, json, datetime, traceback
from pathlib import Path
import numpy as np

ROOT = Path("tc-agi-backend")
LOGS = ROOT/"logs"
ETH = ROOT/"ethics"
LOGS.mkdir(parents=True, exist_ok=True)
ETH.mkdir(parents=True, exist_ok=True)

REPORT = {
    "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
    "status": "INIT",
    "steps": []
}
def step(name, ok=True, info=""):
    REPORT["steps"].append({"step": name, "ok": ok, "info": info})

def save():
    (LOGS/"derm_report.json").write_text(json.dumps(REPORT, ensure_ascii=False, indent=2), encoding="utf-8")

try:
    # 1) Modeli yükle (Türkçe + çok dilli uygun)
    from sentence_transformers import SentenceTransformer, util
    try_names = [
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]
    model = None
    for name in try_names:
        try:
            model = SentenceTransformer(name)
            step("embedder.load", True, f"loaded={name}")
            break
        except Exception as e:
            step("embedder.load_attempt", False, f"{name} -> {e}")
    if model is None:
        raise RuntimeError("Embedding modeli yüklenemedi.")
    
    # 2) Etik ilkeler (çekirdek uzay)
    principles = {
        "kant": "Kantçı etik: Evrensel yasa ilkesi, kişiyi araç değil amaç olarak görmek, koşulsuz ödev.",
        "util": "Faydacılık: Toplam mutluluğu artıran eylem en doğrusudur; sonuçlara göre değerlendirme.",
        "virtue": "Erdem etiği: İyi karakter ve erdemli alışkanlıklar; ölçülülük, cesaret, adalet.",
        "ubuntu": "Ubuntu: Ben biz olduğumuz için varım; topluluk, şefkat ve karşılıklı bağlılık.",
        "care": "Bakım etiği: İlişkilerde özen, empati ve sorumluluk; bağlam duyarlı yaklaşım."
    }
    keys = list(principles.keys())
    texts = [principles[k] for k in keys]
    P = model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)
    step("ethics.space", True, f"principles={len(principles)} dim={P.shape[-1] if hasattr(P,'shape') else 'unk'}")

    # 3) FAISS ile indeksle
    try:
        import faiss
        P_np = P.cpu().numpy()
        index = faiss.IndexFlatIP(P_np.shape[1])     # kozine benzeri: normalize + iç çarpım
        index.add(P_np)
        faiss.write_index(index, str(LOGS/"derm_index.faiss"))
        (LOGS/"derm_index_map.json").write_text(json.dumps(keys, ensure_ascii=False, indent=2), encoding="utf-8")
        step("faiss.index", True, f"stored={str(LOGS/'derm_index.faiss')}")
    except Exception as e:
        step("faiss.index", False, f"FAISS yazılamadı: {e}")

    # 4) Mini MAES ajanları (her ilkeye göre skorlayıcı)
    # Basit mekanizma: örnek yanıtı embed et, her ilke ile kozine benzerliğini [0,1] aralığına ölçekle.
    sample_answer = (
        "Kullanıcı verisini işlerken açık rıza alınmalı, veri en aza indirilmeli, "
        "amaç dışı kullanım engellenmeli ve topluluk yararı birey haklarını gölgelememelidir."
    )
    A = model.encode(sample_answer, convert_to_tensor=True, normalize_embeddings=True)
    scores = util.cos_sim(A, P).cpu().numpy().reshape(-1)  # [-1..1] civarı
    # [0,1] ölçek
    s01 = (scores + 1.0) / 2.0
    agent_reports = []
    for k, s in zip(keys, s01):
        agent_reports.append({
            "agent": k,
            "ethics_score": float(round(float(s), 4)),
            "rationale": f"Örnek yanıtın '{k}' ilkesine semantik yakınlığı yüksek bulundu." if s>0.6 else
                         f"Örnek yanıtın '{k}' ilkesiyle benzerliği sınırlı görünüyor."
        })
    REPORT["agent_reports"] = agent_reports
    REPORT["status"] = "OK"
    step("maes.sim", True, f"agents={len(agent_reports)}")

    # 5) Özet metin ve kayıtlar
    summary = {
        "sample_answer": sample_answer,
        "top_agent": keys[int(np.argmax(s01))],
        "scores": {k: float(round(float(v),4)) for k,v in zip(keys, s01)}
    }
    (LOGS/"derm_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    step("artifacts", True, "logs/derm_report.json, logs/derm_summary.json, logs/derm_index.faiss")

    save()
    print("✅ DERM/MAES etik çekirdek kuruldu.")
    print("   • Rapor: tc-agi-backend/logs/derm_report.json")
    print("   • Özet: tc-agi-backend/logs/derm_summary.json")
    if (LOGS/"derm_index.faiss").exists():
        print("   • FAISS indeks: tc-agi-backend/logs/derm_index.faiss")

except Exception as e:
    REPORT["status"] = "FAILED"
    step("exception", False, f"{type(e).__name__}: {e}")
    save()
    print("❌ Hata:", type(e).__name__, e)
    traceback.print_exc()
    raise
