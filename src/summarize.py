import json
import os
from google import genai
from pydantic import ValidationError
from src.models import MeetingSummary

def _extract_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)

def summarize(transcript: str) -> MeetingSummary:
    with open("prompts/summary_prompt.txt") as f:
        template = f.read()
    prompt = template.replace("{transcript}", transcript)

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    for attempt in range(2):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        raw_text = response.text

        try:
            data = _extract_json(raw_text)
            return MeetingSummary(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == 0:
                prompt = prompt + f"\n\nYour previous response was invalid ({e}). Respond again with ONLY valid JSON, no markdown fences."
                continue
            raise ValueError(f"Model failed to produce valid summary JSON: {e}")
