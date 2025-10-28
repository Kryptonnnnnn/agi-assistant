# modules/automation/workflow_parser.py
"""
Workflow Parser - Converts session_summary.json to automation-ready workflow steps
"""

import json
from typing import List, Dict, Any
from pathlib import Path

def parse_summary_to_workflow(summary_file: str) -> List[Dict[str, Any]]:
    """
    Converts session_summary.json to automation steps
    
    Args:
        summary_file: Path to session_summary.json
    
    Returns:
        List of automation workflow steps
    """
    try:
        with open(summary_file, "r") as f:
            summary = json.load(f)
    except FileNotFoundError:
        print(f"Error: {summary_file} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {summary_file}")
        return []
    
    workflow_steps = []
    
    # Extract LLM analysis
    llm_analysis = summary.get("llm_analysis", {})
    
    # Check if automation steps are already generated
    if "automation_steps" in llm_analysis:
        return llm_analysis["automation_steps"]
    
    # Otherwise, generate from detected actions
    detected_actions = llm_analysis.get("detected_actions", [])
    
    for i, action in enumerate(detected_actions):
        step = parse_action_to_step(action, i + 1)
        if step:
            workflow_steps.append(step)
    
    # If no actions detected, try to infer from OCR and transcription
    if not workflow_steps:
        workflow_steps = infer_steps_from_session(summary)
    
    return workflow_steps

def parse_action_to_step(action: str, step_number: int) -> Dict[str, Any]:
    """
    Parse a detected action into an automation step
    
    Args:
        action: Action description string
        step_number: Step number in workflow
    
    Returns:
        Automation step dictionary
    """
    action_lower = action.lower()
    
    # Click action
    if "click" in action_lower or "clicked" in action_lower:
        if ":" in action:
            target = action.split(":", 1)[1].strip()
        else:
            target = "Unknown"
        
        return {
            "step": step_number,
            "action": "click",
            "target": target,
            "args": {"button": target},
            "description": action
        }
    
    # Type/Input action
    elif "type" in action_lower or "input" in action_lower or "enter" in action_lower:
        if ":" in action:
            target = action.split(":", 1)[1].strip()
        else:
            target = ""
        
        return {
            "step": step_number,
            "action": "type",
            "target": target,
            "args": {"text": target},
            "description": action
        }
    
    # Wait action
    elif "wait" in action_lower:
        seconds = 2  # Default wait time
        return {
            "step": step_number,
            "action": "wait",
            "args": {"seconds": seconds},
            "description": action
        }
    
    # Hotkey action
    elif "hotkey" in action_lower or "shortcut" in action_lower:
        if ":" in action:
            keys = action.split(":", 1)[1].strip()
        else:
            keys = "ctrl+s"
        
        return {
            "step": step_number,
            "action": "hotkey",
            "args": {"keys": keys},
            "description": action
        }
    
    # Voice command
    elif "voice command" in action_lower:
        if ":" in action:
            command = action.split(":", 1)[1].strip()
        else:
            command = ""
        
        return {
            "step": step_number,
            "action": "execute",
            "command": command,
            "description": action
        }
    
    # Generic action
    else:
        return {
            "step": step_number,
            "action": "generic",
            "description": action
        }

def infer_steps_from_session(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Infer workflow steps from OCR and transcription when no actions detected
    
    Args:
        summary: Complete session summary
    
    Returns:
        List of inferred workflow steps
    """
    steps = []
    step_number = 1
    
    # Check OCR results for UI elements
    session_data = summary.get("session_data", {})
    ocr_results = session_data.get("ocr_results", [])
    
    for ocr in ocr_results:
        ui_elements = ocr.get("ui_elements", [])
        for element in ui_elements:
            if element['type'] == 'button':
                steps.append({
                    "step": step_number,
                    "action": "click",
                    "target": element['text'],
                    "args": {
                        "x": element['position']['x'],
                        "y": element['position']['y']
                    },
                    "description": f"Click button at ({element['position']['x']}, {element['position']['y']})"
                })
                step_number += 1
            
            elif element['type'] == 'input':
                steps.append({
                    "step": step_number,
                    "action": "type",
                    "target": element['text'],
                    "args": {
                        "x": element['position']['x'],
                        "y": element['position']['y'],
                        "text": ""
                    },
                    "description": f"Type into field at ({element['position']['x']}, {element['position']['y']})"
                })
                step_number += 1
    
    # Check transcription for commands
    audio_transcription = session_data.get("audio_transcription", {})
    if audio_transcription.get("success"):
        text = audio_transcription.get("text", "")
        
        # Extract potential commands
        command_keywords = ["open", "close", "save", "delete", "create", "run"]
        words = text.lower().split()
        
        for i, word in enumerate(words):
            if word in command_keywords and i + 1 < len(words):
                target = words[i + 1]
                steps.append({
                    "step": step_number,
                    "action": "execute",
                    "command": f"{word} {target}",
                    "description": f"Voice command: {word} {target}"
                })
                step_number += 1
    
    return steps

def save_workflow_json(workflow_steps: List[Dict[str, Any]], output_file: str):
    """
    Save workflow steps to JSON file
    
    Args:
        workflow_steps: List of workflow steps
        output_file: Output file path
    """
    workflow_data = {
        "workflow_id": Path(output_file).stem,
        "steps": workflow_steps,
        "step_count": len(workflow_steps),
        "generated_from": "workflow_parser.py"
    }
    
    with open(output_file, 'w') as f:
        json.dump(workflow_data, f, indent=2)
    
    print(f"Workflow saved to: {output_file}")

def get_workflow_summary(workflow_steps: List[Dict[str, Any]]) -> str:
    """
    Generate a human-readable summary of workflow
    
    Args:
        workflow_steps: List of workflow steps
    
    Returns:
        Summary string
    """
    if not workflow_steps:
        return "Empty workflow"
    
    summary_lines = [f"Workflow with {len(workflow_steps)} steps:"]
    
    for step in workflow_steps[:10]:  # Show first 10 steps
        summary_lines.append(f"  {step['step']}. {step.get('description', step['action'])}")
    
    if len(workflow_steps) > 10:
        summary_lines.append(f"  ... and {len(workflow_steps) - 10} more steps")
    
    return "\n".join(summary_lines)

# Example usage and testing
if __name__ == "__main__":
    # Test the parser
    summary_file = "data/json/session_summary.json"
    
    if Path(summary_file).exists():
        print("Parsing workflow from session summary...")
        workflow = parse_summary_to_workflow(summary_file)
        
        print("\n" + "="*60)
        print(get_workflow_summary(workflow))
        print("="*60)
        
        # Save to workflow file
        output_file = "data/workflows/parsed_workflow.json"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        save_workflow_json(workflow, output_file)
    else:
        print(f"No summary file found at {summary_file}")
        print("Run main.py first to generate a session summary")