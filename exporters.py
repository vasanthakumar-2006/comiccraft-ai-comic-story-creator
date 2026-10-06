from fpdf import FPDF
from pathlib import Path
from datetime import datetime
import re

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def save_pdf(panels, character):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", character or "comic")[:30]
    filename = f"comic_{safe}_{stamp}.pdf"
    path = EXPORT_DIR / filename
    pdf = FPDF()
    for i, panel in enumerate(panels):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 12, f"Panel {i+1}: {panel['title']}")
        image_path = BASE_DIR / panel["image"].lstrip("/")
        # URL begins static/...; remove prefix for filesystem path
        image_path = BASE_DIR / panel["image"].replace("/static/", "static/")
        if image_path.exists():
            pdf.image(str(image_path), x=15, y=40, w=180)
        pdf.set_y(150)
        pdf.set_font("Helvetica", "", 12)
        for label, key in [("Scene", "scene"), ("Narration", "narration"), ("Dialogue", "dialogue")]:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, label, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 11)
            text = str(panel.get(key, "")).encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 7, text)
            pdf.ln(2)
    pdf.output(str(path))
    return filename
