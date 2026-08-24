# Meeting Summarizer

Transcribes meeting audio and generates a structured, action-oriented summary: key decisions, action items (with owner/due date when mentioned), and open questions — plus the full transcript.

## Architecture

```
 Audio file
     |
     v
 transcribe.py   -- faster-whisper (local, no API key, no network call)
     |  raw transcript text
     v
 summarize.py    -- Gemini API, structured JSON prompt (prompts/summary_prompt.txt)
     |  MeetingSummary (validated by pydantic)
     v
 storage.py      -- SQLite (meetings.db)
     |
     v
 pipeline.py     -- chains everything into one process_meeting() call
```

Each stage is a plain Python function with a typed input/output. `transcribe()` doesn't know `summarize()` exists, and neither knows how the result gets used — that separation is what makes it possible to swap pieces (e.g. a hosted ASR API instead of local Whisper, or a different LLM) without touching the rest of the code.

## Setup

```bash
git clone <this-repo>
cd meeting-summarizer
pip install -r requirements.txt
```

Get a free Gemini API key from [aistudio.google.com](https://aistudio.google.com) (no credit card required) and set it as an environment variable:

```bash
export GOOGLE_API_KEY=your_key_here
```

**Note on first run:** faster-whisper downloads model weights (~150MB) the first time it's used. This happens automatically but makes the first transcription slower than later ones.

## Usage

```python
from src.pipeline import process_meeting

transcript, summary = process_meeting("meeting_audio.mp3")
print(summary.model_dump_json(indent=2))
```

This single function call transcribes the audio, generates a structured summary, and saves the result to a local SQLite database (`meetings.db`).

### Tests

```bash
python tests/test_summarize.py
```

Tests cover JSON-parsing and schema-validation logic without needing an API key, so this can be verified with zero setup.

## Design decisions

- **Local Whisper (faster-whisper) instead of a hosted ASR API.** No API key needed to get started, no per-minute cost while iterating, and audio never leaves the machine — relevant since real meeting recordings are often confidential. Trade-off: hosted APIs may edge out local Whisper on noisy audio and support streaming; swapping is a small, isolated change since the rest of the app only depends on `transcribe()`'s function signature.
- **Gemini instead of a paid LLM API.** Free tier with generous limits and no credit card required, which mattered given the project timeline.
- **Structured JSON output, validated with pydantic**, rather than a free-text summary. This makes the output usable programmatically instead of just readable. If the model returns malformed JSON, `summarize.py` retries once with an explicit correction message before failing — a small reliability improvement over hoping for well-formed output on the first try.
- **SQLite over a full database server.** Zero setup, single file, so this can be cloned and run in minutes without provisioning anything.
- **The prompt lives in its own file** (`prompts/summary_prompt.txt`), not hardcoded in Python, so it can be reviewed and iterated on independently of code changes.

## What I'd add with more time

- A web frontend (Streamlit) for uploading audio and viewing results visually — the pipeline is already structured so a UI just calls `process_meeting()` directly, no core logic changes needed
- Speaker diarization ("who said what")
- Chunking/streaming support for very long audio files
- A proper eval set (sample transcripts + expected action items) to measure summary quality quantitatively instead of eyeballing it
- Fallback support for a hosted ASR API for cases where local Whisper accuracy isn't sufficient (e.g. very noisy recordings)

## Evaluation checklist

- [x] ASR integration — local Whisper (`src/transcribe.py`)
- [x] Backend to store & process data — SQLite (`src/storage.py`)
- [x] LLM for summary generation — Gemini API, structured output (`src/summarize.py`)
- [x] Tests — runnable without an API key
- [ ] Frontend — planned as next step
