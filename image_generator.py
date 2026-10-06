from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap, hashlib

BASE_DIR = Path(__file__).resolve().parent.parent
PANEL_DIR = BASE_DIR / "static" / "panels"
PANEL_DIR.mkdir(parents=True, exist_ok=True)

def _font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()

def generate_panel_image(panel: dict, index: int, token: str):
    """Create a local illustrated card as a dependable starter visual."""
    digest = hashlib.md5(f"{token}-{index}".encode()).hexdigest()[:10]
    path = PANEL_DIR / f"{digest}.png"
    if path.exists():
        return f"/static/panels/{path.name}"

    w, h = 960, 600
    img = Image.new("RGB", (w, h), (226, 238, 255))
    draw = ImageDraw.Draw(img)
    # soft sky and ground
    for y in range(h):
        t = y / h
        c = (int(115+95*t), int(180-25*t), int(245-70*t))
        draw.line((0, y, w, y), fill=c)
    draw.ellipse((720, 55, 830, 165), fill=(255, 224, 120))
    draw.rectangle((0, 440, w, h), fill=(83, 158, 112))
    # decorative hills
    draw.ellipse((-130, 350, 480, 600), fill=(69, 139, 99))
    draw.ellipse((350, 370, 1080, 650), fill=(53, 125, 88))
    # friendly character icon
    draw.ellipse((390, 190, 570, 370), fill=(255, 221, 175), outline=(50, 58, 85), width=8)
    draw.ellipse((435, 250, 455, 270), fill=(40, 45, 60))
    draw.ellipse((505, 250, 525, 270), fill=(40, 45, 60))
    draw.arc((445, 270, 515, 330), 0, 180, fill=(145, 65, 65), width=7)
    draw.rounded_rectangle((420, 350, 540, 475), radius=35, fill=(92, 105, 205), outline=(50, 58, 85), width=7)
    # caption card
    draw.rounded_rectangle((35, 28, 925, 145), radius=24, fill=(255,255,255), outline=(40,50,75), width=5)
    title = str(panel.get("title", f"Panel {index}"))
    draw.text((62, 45), f"PANEL {index}: {title[:45]}", font=_font( thirty:=30, True), fill=(35,45,75))
    scene = str(panel.get("scene", ""))[:130]
    lines = textwrap.wrap(scene, width=76)[:2]
    for j, line in enumerate(lines):
        draw.text((64, 91 + j*25), line, font=_font(19), fill=(55,65,85))
    img.save(path, "PNG")
    return f"/static/panels/{path.name}"
