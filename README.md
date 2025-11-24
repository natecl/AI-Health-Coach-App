# AI Health Coach App

Minimal Flask backend + static frontend MVP to ask a health coach question and receive a concise, actionable reply.

## Quick start
- Backend: `python -m venv .venv && source .venv/bin/activate` then `pip install -r Backend/requirements.txt` and `python Backend/main.py`
- Optional AI: set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`, default `gpt-4o-mini`) before starting the server
- Frontend: in another shell `cd Frontend && python -m http.server 5173` then open http://localhost:5173
- Try a message (e.g., stress, sleep, nutrition). If no API key is set, the server uses a rule-based fallback.
