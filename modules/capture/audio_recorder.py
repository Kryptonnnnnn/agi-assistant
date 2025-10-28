import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime

def record_audio(session_id=None, output_dir="data/clips", duration=15, fs=44100):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if session_id:
        filename = os.path.join(output_dir, f"audio_{session_id}_{timestamp}.wav")
    else:
        filename = os.path.join(output_dir, f"audio_{timestamp}.wav")

    # 🔍 Detect default input device info
    device_info = sd.query_devices(sd.default.device[0], 'input')
    channels = device_info['max_input_channels']
    print(f"🎧 Using {channels} input channel(s)")

    if channels < 1:
        raise RuntimeError("No available input channels — check your mic settings.")

    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()

    write(filename, fs, recording)
    print(f"Saved audio: {filename}")
    return filename
