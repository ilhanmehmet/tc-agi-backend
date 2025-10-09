import json, datetime, statistics, os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

LOGS = Path("tc-agi-backend/logs")
REPORTS = LOGS / "reports"
REPORTS.mkdir(exist_ok=True)

def generate_report():
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = REPORTS / f"ethics_report_{now}.pdf"
    styles = getSampleStyleSheet()
    story = []

    def add(text, style="Normal"):
        story.append(Paragraph(text, styles[style]))
        story.append(Spacer(1, 12))

    add(f"<b>TC-AGI Günlük Etik Raporu</b>", "Title")
    add(f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    add("<b>Distillation ve Etik Değerlendirme Özeti</b>", "Heading2")

    # distillation raporu
    distillation_file = LOGS / "damıtma_raporu.json"
    if distillation_file.exists():
        add("Damıtma raporu bulundu.", "Heading3")
        with open(distillation_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        add(json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "<br/>"))
    else:
        add("Damıtma raporu bulunamadı.")

    # etik özet
    ethics_file = LOGS / "derm_summary.json"
    if ethics_file.exists():
        add("<b>Etik Skorlar</b>", "Heading3")
        with open(ethics_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        scores = data.get("scores", {})
        for k, v in scores.items():
            add(f"{k}: {v:.3f}")
        avg = statistics.mean(scores.values()) if scores else 0
        add(f"<b>Ortalama etik skoru:</b> {avg:.3f}")
    else:
        add("Etik özet dosyası bulunamadı.")

    doc = SimpleDocTemplate(str(report_path), pagesize=A4)
    doc.build(story)
    print(f"✅ Günlük rapor oluşturuldu: {report_path}")

if __name__ == "__main__":
    generate_report()
