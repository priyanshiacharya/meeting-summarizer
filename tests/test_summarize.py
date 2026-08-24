import sys
sys.path.insert(0, "/content")

from src.summarize import _extract_json
from src.models import MeetingSummary

def test_extract_json_plain():
    raw = '{"title": "Sync", "key_decisions": [], "action_items": [], "open_questions": [], "summary": "A quick sync."}'
    data = _extract_json(raw)
    assert data["title"] == "Sync"

def test_extract_json_with_fences():
    raw = '```json\n{"title": "Sync", "key_decisions": [], "action_items": [], "open_questions": [], "summary": "A quick sync."}\n```'
    data = _extract_json(raw)
    assert data["summary"] == "A quick sync."

def test_schema_valid():
    data = {
        "title": "Weekly Planning",
        "key_decisions": ["Ship v2"],
        "action_items": [{"task": "Update roadmap", "owner": "Priya", "due_date": "Friday"}],
        "open_questions": [],
        "summary": "Team agreed to ship v2.",
    }
    summary = MeetingSummary(**data)
    assert summary.action_items[0].owner == "Priya"

if __name__ == "__main__":
    test_extract_json_plain()
    test_extract_json_with_fences()
    test_schema_valid()
    print("All tests passed.")
