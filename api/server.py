from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess, datetime, os, json

app = FastAPI(title="TC-AGI Core Service", version="1.0")
app.mount("/logs", StaticFiles(directory="tc-agi-backend/logs"), name="logs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


LOGDIR = "tc-agi-backend/logs"
os.makedirs(LOGDIR, exist_ok=True)

def run_ethics_check():
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logpath = os.path.join(LOGDIR, f"ethics_run_{ts}.log")
    with open(logpath, "w", encoding="utf-8") as f:
        f.write(f"[{ts}] Etik denetim başlatıldı\n")
        try:
            subprocess.run(
                ["python", "tc-agi-backend/ethics/derm_init_test.py"],
                stdout=f, stderr=f, check=False
            )
            f.write(f"[{ts}] Denetim tamamlandı\n")
        except Exception as e:
            f.write(f"[{ts}] HATA: {e}\n")

sched = BackgroundScheduler()
sched.add_job(run_ethics_check, "interval", minutes=15)
sched.add_job(lambda: subprocess.run(["python", "tc-agi-backend/automation/daily_report.py"]), "interval", hours=24)
sched.start()

@app.get("/")
@app.get("/status")
def status():
    return {"status": "ok"}

def root():
    return {"TC-AGI": "running", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/logs")
def list_logs():
    files = sorted(os.listdir(LOGDIR))[-10:]
    return {"recent_logs": files}

@app.get("/check")
def manual_check():
    run_ethics_check()
    return {"status": "manual ethics check triggered"}

@app.on_event("shutdown")
def shutdown():
    sched.shutdown()
