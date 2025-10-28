from pynput import mouse, keyboard
import time

def record_input_events(duration=5):
    events = []
    start_time = time.time()

    def on_move(x, y):
        events.append({"type": "move", "pos": (x, y), "time": time.time()})

    def on_click(x, y, button, pressed):
        events.append({"type": "click", "pos": (x, y), "button": str(button), "pressed": pressed, "time": time.time()})

    def on_press(key):
        events.append({"type": "key", "key": str(key), "pressed": True, "time": time.time()})

    def on_release(key):
        events.append({"type": "key", "key": str(key), "pressed": False, "time": time.time()})

    with mouse.Listener(on_move=on_move, on_click=on_click) as ml, \
         keyboard.Listener(on_press=on_press, on_release=on_release) as kl:
        while time.time() - start_time < duration:
            time.sleep(0.1)
        ml.stop()
        kl.stop()

    return events
