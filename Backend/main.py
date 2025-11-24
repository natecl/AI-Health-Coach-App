"""Minimal Flask backend for the AI Health Coach MVP."""

import os
from typing import Optional

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def ask_openai(user_message: str) -> Optional[str]:
    """Send the user's message to OpenAI if the SDK + API key are available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a supportive health coach. Keep replies under 80 words "
                        "and give 1-2 actionable suggestions."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            max_tokens=240,
        )
        return completion.choices[0].message.content
    except Exception as exc:  # pragma: no cover - defensive guardrail
        print(f"OpenAI error: {exc}")
        return None


def fallback_coach_reply(user_message: str) -> str:
    """Basic rule-based response if OpenAI is unavailable."""
    message = user_message.lower()
    tips = []
    if "sleep" in message:
        tips.append("Aim for 7-9 hours; set a consistent bedtime and avoid screens 60 minutes prior.")
    if "stress" in message:
        tips.append("Try 5 minutes of box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s.")
    if "diet" in message or "eat" in message:
        tips.append("Add one serving of veggies to your next meal and hydrate with a full glass of water.")
    if not tips:
        tips.append("Take a brisk 10-minute walk today and drink water steadily across the afternoon.")

    return f"I hear you. {tips[0]}"


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


@app.route("/api/coach", methods=["POST"])
def coach():
    data = request.get_json(force=True, silent=True) or {}
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    ai_reply = ask_openai(user_message)
    reply = ai_reply or fallback_coach_reply(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
