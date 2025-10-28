import subprocess
import os

def transcribe_audio(audio_file):
    """
    Transcribes an audio file using whisper.cpp CLI and returns transcription data.
    """
    whisper_bin = "./whisper.cpp/build/bin/whisper-cli"
    model_path = "./whisper.cpp/models/ggml-base.en.bin"

    if not os.path.exists(whisper_bin):
        raise FileNotFoundError(f"Whisper binary not found at {whisper_bin}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    try:
        # Run whisper.cpp command and capture stdout/stderr
        result = subprocess.run(
            [whisper_bin, "-m", model_path, "-f", audio_file, "-otxt"],
            capture_output=True,
            text=True,
            check=True
        )

        transcript = result.stdout.strip()

        # Whisper sometimes writes text to a .txt file instead of stdout
        txt_file = audio_file.replace(".wav", ".txt")
        if os.path.exists(txt_file):
            with open(txt_file, "r") as f:
                transcript = f.read().strip()

        # Handle blank or empty transcriptions
        if not transcript or "[BLANK_AUDIO]" in transcript:
            return {
                "success": False,
                "text": "[BLANK_AUDIO]",
                "file": txt_file if os.path.exists(txt_file) else None
            }

        return {
            "success": True,
            "text": transcript,
            "file": txt_file if os.path.exists(txt_file) else None
        }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "text": f"Transcription failed: {e.stderr.strip()}",
            "file": None
        }


def extract_commands_from_transcription(transcription_text: str):
    """
    Extracts possible user commands or intent-like actions from transcription text.
    Used by LLM modules to detect automation triggers.
    """
    if not transcription_text or not isinstance(transcription_text, str):
        return []

    actions = []

    # Basic keyword-based detection (you can expand this later)
    keywords = [
        "open", "close", "click", "save", "search",
        "start", "stop", "run", "analyze", "record",
        "delete", "copy", "move", "upload", "download"
    ]

    text_lower = transcription_text.lower()

    for word in keywords:
        if word in text_lower:
            actions.append(f"Detected command: '{word}'")

    # Remove duplicates and return
    return list(set(actions))
