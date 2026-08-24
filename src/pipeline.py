from src.transcribe import transcribe
from src.summarize import summarize
from src.storage import init_db, save_meeting

def process_meeting(audio_path: str, save: bool = True):
    print(f"[1/2] Transcribing {audio_path} ...")
    transcript_text = transcribe(audio_path)

    print("[2/2] Generating summary ...")
    summary = summarize(transcript_text)

    if save:
        init_db()
        meeting_id = save_meeting(audio_path, transcript_text, summary)
        print(f"Saved as meeting #{meeting_id}")

    return transcript_text, summary
