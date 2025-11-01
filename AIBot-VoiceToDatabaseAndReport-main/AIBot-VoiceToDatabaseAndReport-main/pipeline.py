from transcribe import transcribe_audio
from generate_report import generate_report
from storage import init_db, save_report
from notifications import send_telegram_message
from pathlib import Path
import shutil
import json

def process_audio_to_report(audio_path: str, fallback_agent_name: str = ""):
    """
    Full pipeline for a single file:
    1. Transcribe audio to text
    2. Generate structured report from transcript (JSON + human-readable)
    3. Save JSON to SQLite database with timestamp
    4. Send human-readable report via Telegram with report ID
    """
    # 1️⃣ Transcribe audio
    print(f"[1/2] Transcribing audio: {audio_path}")
    transcript = transcribe_audio(audio_path)
    print("\n[Transcript Output]\n", transcript)

    # 2️⃣ Generate structured report
    print("\n[2/2] Generating structured report...")
    report = generate_report(transcript, fallback_agent_name=fallback_agent_name)

    # 3️⃣ Save JSON to database and get unique report ID
    report_id = save_report(report["json_output"])
    print(f"\nReport saved to database with ID #{report_id}.")

    # 4️⃣ Send human-readable report via Telegram
    telegram_text = f"Report #{report_id}:\n\n{report['text_report']}"
    send_telegram_message(telegram_text)
    print("Report sent via Telegram.")

    return report_id, report

def process_batch(folder_path: str, fallback_agent_name: str = ""):
    """
    Process all .mp3 files in a folder and move them to 'processed' folder after completion.
    """
    folder = Path(folder_path)
    processed_folder = folder / "processed"
    processed_folder.mkdir(exist_ok=True)

    audio_files = list(folder.glob("*.mp3"))

    if not audio_files:
        print("No .mp3 files found in folder:", folder)
        return

    for audio_file in audio_files:
        print("\n===============================")
        print(f"Processing file: {audio_file.name}")
        try:
            process_audio_to_report(str(audio_file), fallback_agent_name=fallback_agent_name)
            # Move file to processed folder
            shutil.move(str(audio_file), processed_folder / audio_file.name)
            print(f"Moved {audio_file.name} to {processed_folder}")
        except Exception as e:
            print(f"Error processing {audio_file.name}: {e}")
        print("===============================\n")


if __name__ == "__main__":
    # Initialize DB
    init_db()

    # Folder with multiple agent audio recordings
    audio_folder = "agent_recordings"  # change to your folder path
    process_batch(audio_folder, fallback_agent_name="John Smith")
