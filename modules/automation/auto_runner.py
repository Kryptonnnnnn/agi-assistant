# modules/automation/auto_runner.py
import pyautogui
import time

def execute_workflow(workflow_steps):
    """
    Executes a workflow list generated from workflow_parser
    """
    for step in workflow_steps:
        action = step["action"]
        args = step.get("args", {})
        
        if action == "click":
            pyautogui.click(args["x"], args["y"])
        elif action == "type":
            pyautogui.typewrite(args["text"], interval=0.05)
        elif action == "hotkey":
            pyautogui.hotkey(*args["keys"])
        elif action == "wait":
            time.sleep(args["seconds"])
        
        print(f"Executed: {action}")
