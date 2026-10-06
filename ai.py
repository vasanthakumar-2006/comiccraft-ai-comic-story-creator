import os
import json
from google import genai
from google.genai import types

def create_panels(prompt: str, character: str, setting: str, tone: str, art_style: str):
    """Generate a structured five-panel comic with Gemini. Uses a demo fallback without a key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return demo_panels(prompt, character, setting, tone, art_style)

    client = genai.Client(api_key=api_key)
    instruction = f"""
Create a family-friendly five-panel comic story based on the user's idea.
Return ONLY valid JSON: an array of exactly 5 objects. Each object must contain:
"title", "scene", "narration", "dialogue", "image_prompt".
Keep each field concise and suitable for a comic panel.
Character: {character}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
Story idea: {prompt}
"""
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=instruction,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.8),
    )
    data = json.loads(response.text)
    if not isinstance(data, list) or len(data) != 5:
        raise ValueError("Gemini did not return exactly five panels.")
    return data

def demo_panels(prompt, character, setting, tone, art_style):
    """Offline-friendly sample output so the site can be tested before adding an API key."""
    beats = [
        ("A New Beginning", f"{character} starts a new adventure in {setting}."),
        ("A Curious Discovery", f"Something unexpected catches {character}'s attention."),
        ("A Little Challenge", f"{character} faces a small challenge and pauses to think."),
        ("A Clever Idea", f"With courage and kindness, {character} finds a way forward."),
        ("A Happy Ending", f"{character} celebrates the adventure and looks ahead.")
    ]
    return [{
        "title": title,
        "scene": scene,
        "narration": f"Story idea: {prompt}. {scene}",
        "dialogue": "“We can do this, one step at a time!”",
        "image_prompt": f"{art_style} illustration, {scene}, {tone} mood, colorful, family-friendly"
    } for title, scene in beats]
