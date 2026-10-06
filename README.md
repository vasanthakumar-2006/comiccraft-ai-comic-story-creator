<<<<<<< HEAD
# ComicCraft — AI Comic Story Creator

A FastAPI web app that creates a five-panel comic story with Gemini text generation, illustrated panel cards, a preview page, and PDF export.

## Features
- Story prompt, character, setting, tone, and art-style inputs
- Five-panel story generation using Gemini when `GEMINI_API_KEY` is configured
- Demo story mode when no API key is configured
- Generated illustrative panel cards (starter visuals; not AI-generated artwork)
- Comic preview and PDF download

## Run locally (Windows)
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. In terminal run:
   ```bash
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Gemini API key. The app can also run in demo mode without a key.
5. Run:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Visit http://127.0.0.1:8000

## Deploy
Push the project to GitHub, then create a Render Web Service from the repository.
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add `GEMINI_API_KEY` in Render Environment settings.
- Use a persistent disk or external object storage if generated files must survive redeploys. Configure suitable limits and monitor API usage before sharing publicly.

## Note
This starter version creates designed panel illustrations locally using Pillow. It does not yet call Stable Diffusion for AI artwork. Add a hosted image-generation service/GPU integration to enable true AI-generated images. Do not commit API keys or `.env` to GitHub.
=======
# ComicCraft
>>>>>>> 37dfa066ac3b3d9d6950f16dc5bf5daf55b9f595
