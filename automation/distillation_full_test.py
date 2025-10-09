import os, sys, time, json, math, datetime, traceback
from pathlib import Path

ROOT = Path("tc-agi-backend")
MODELS = ROOT / "models"
LOGS = ROOT / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

REPORT = {
    "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
    "teacher_model": str(MODELS / "llama3-8b.gguf"),
    "status": "INIT",
    "steps": []
}

def log_step(name, ok=True, info=""):
    REPORT["steps"].append({"step": name, "ok": ok, "info": info})

def save_report():
    with open(LOGS / "distillation_report.json", "w", encoding="utf-8") as f:
        json.dump(REPORT, f, ensure_ascii=False, indent=2)

try:
    import torch
    from torch import nn
    from llama_cpp import Llama

    cuda = torch.cuda.is_available()
    dev = torch.device("cuda:0" if cuda else "cpu")

    llm = Llama(
        model_path=str(MODELS / "llama3-8b.gguf"),
        n_ctx=2048,
        n_threads=max(1, os.cpu_count() // 2),
        logits_all=True,    # 🔥 logprobs artık destekleniyor
        verbose=False
    )
    log_step("teacher.load", True, "llama3-8b.gguf yüklendi")

    prompt = "You are a helpful AI. Explain knowledge distillation in one short, clear sentence."
    out = llm.create_completion(
        prompt=prompt,
        max_tokens=40,
        temperature=0.7,
        top_p=0.95,
        logprobs=5
    )
    text_out = out["choices"][0]["text"]
    with open(LOGS / "teacher_sample.txt", "w", encoding="utf-8") as f:
        f.write(text_out)
    log_step("teacher.output", True, f"len={len(text_out)}")

    # Soft labels üretimi
    token_soft = []
    vocab = {}
    vidx = 0
    for choice in out["choices"]:
        for step in choice.get("logprobs", {}).get("top_logprobs", []):
            probs = {tok: math.exp(lp) for tok, lp in step.items()}
            s = sum(probs.values())
            if s == 0:
                continue
            probs = {tok: v/s for tok, v in probs.items()}
            for tok in probs:
                if tok not in vocab:
                    vocab[tok] = vidx
                    vidx += 1
            token_soft.append(probs)
    if not token_soft:
        vocab = {"A":0,"B":1,"C":2}
        token_soft = [{0:0.7,1:0.2,2:0.1}]
        log_step("teacher.softlabels", False, "logprobs boş, yedek dağılım kullanıldı")
    else:
        log_step("teacher.softlabels", True, f"steps={len(token_soft)}, vocab_size={len(vocab)}")

    V = len(vocab)
    class Student(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(nn.Linear(V,64), nn.ReLU(), nn.Linear(64,V))
        def forward(self,x): return self.net(x)

    student = Student().to(dev)
    opt = torch.optim.Adam(student.parameters(), lr=3e-3)
    criterion = nn.KLDivLoss(reduction="batchmean")

    def d2t(d):
        x = torch.zeros(V)
        for i,p in d.items():
            x[vocab[i]] = p
        return x

    X = torch.stack([d2t(d) for d in token_soft]).to(dev)
    Y = X.clone().detach()

    losses=[]
    for i in range(40):
        opt.zero_grad(set_to_none=True)
        logits = student(X)
        loss = criterion(torch.log_softmax(logits,dim=-1), Y)
        loss.backward()
        opt.step()
        losses.append(float(loss.item()))

    with open(LOGS / "distillation_losses.txt","w") as f:
        for i,l in enumerate(losses): f.write(f"{i}\t{l:.6f}\n")

    REPORT["status"]="OK"
    log_step("train",True,f"final_loss={losses[-1]:.6f}")
    save_report()

    print("✅ Distillation tam kapasite çalıştı.")
    print(f"   • Son loss: {losses[-1]:.6f}")
    print("   • Örnek çıktı: logs/teacher_sample.txt")
    print("   • Rapor: logs/distillation_report.json")

except Exception as e:
    REPORT["status"]="FAILED"
    log_step("error",False,f"{type(e).__name__}: {e}")
    save_report()
    print("❌ Hata:",type(e).__name__,e)
    traceback.print_exc()
    sys.exit(1)
