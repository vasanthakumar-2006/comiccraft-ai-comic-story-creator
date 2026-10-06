from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.ai import create_panels
from app.image_generator import generate_panel_image
from app.exporters import save_pdf
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@router.post("/generate", response_class=HTMLResponse)
async def generate(request: Request,
                   prompt: str = Form(...),
                   character: str = Form("Hero"),
                   setting: str = Form("Fantasy forest"),
                   tone: str = Form("Funny"),
                   art_style: str = Form("Comic book")):
    if len(prompt.strip()) < 5:
        raise HTTPException(status_code=400, detail="Please enter a story idea with at least 5 characters.")
    try:
        panels = create_panels(prompt.strip(), character.strip() or "Hero", setting, tone, art_style)
        token = uuid.uuid4().hex
        for i, panel in enumerate(panels, 1):
            panel["image"] = generate_panel_image(panel, i, token)
        pdf_name = save_pdf(panels, character)
        return templates.TemplateResponse(request=request, name="comic_preview.html",
            context={"panels": panels, "character": character, "pdf_name": pdf_name})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {exc}")

@router.get("/download/{filename}")
async def download(filename: str):
    safe_name = Path(filename).name
    path = BASE_DIR / "static" / "exports" / safe_name
    if not path.exists() or not safe_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(path, media_type="application/pdf", filename=safe_name)

@router.get("/health")
async def health():
    return {"status": "ok", "app": "ComicCraft"}
