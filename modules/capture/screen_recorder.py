from mss import mss
import time, os
from datetime import datetime

def capture_screenshots(session_id=None, output_dir="data/clips", interval=3, duration=15):
    os.makedirs(output_dir, exist_ok=True)
    sct = mss()
    start_time = time.time()
    count = 0
    screenshot_paths = []  # ✅ store file paths

    while time.time() - start_time < duration:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if session_id:
            filename = os.path.join(output_dir, f"screenshot_{session_id}_{timestamp}_{count}.png")
        else:
            filename = os.path.join(output_dir, f"screenshot_{timestamp}_{count}.png")

        sct.shot(output=filename)
        print("Saved:", filename)
        screenshot_paths.append(filename)  # ✅ keep track of saved file
        count += 1
        time.sleep(interval)

    return screenshot_paths  # ✅ return the list
