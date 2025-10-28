# modules/llm/local_llm.py
"""
Local LLM Module - Analyzes sessions using local language models
Supports: Ollama, LLaMA.cpp, or fallback to rule-based analysis
"""

import json
import requests
from typing import Dict, Any, List
from pathlib import Path

class LocalLLM:
    def __init__(self, backend: str = "ollama", model: str = "phi3:latest"):
        """
        Initialize Local LLM
        
        Args:
            backend: LLM backend ("ollama", "llamacpp", or "rules")
            model: Model name
        """
        self.backend = backend
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    
    def is_available(self) -> bool:
        """Check if LLM backend is available"""
        if self.backend == "ollama":
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                return response.status_code == 200
            except:
                return False
        return True
    
    def generate(self, prompt: str) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: Input prompt
        
        Returns:
            Generated text
        """
        if self.backend == "ollama":
            return self._generate_ollama(prompt)
        else:
            return self._generate_rules_based(prompt)
    
    def _generate_ollama(self, prompt: str) -> str:
        """Generate using Ollama"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 500
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "").strip() or "No meaningful response from model."
            else:
                print(f"   ⚠️  Ollama error: {response.status_code} -> {response.text}")
                return self._generate_rules_based(prompt)
        
        except Exception as e:
            print(f"   ⚠️  Ollama connection failed: {e}")
            return self._generate_rules_based(prompt)
    
    def _generate_rules_based(self, prompt: str) -> str:
        """Fallback rule-based generation"""
        # Simple keyword-based analysis
        prompt_lower = prompt.lower()
        
        if "summarize" in prompt_lower or "summary" in prompt_lower:
            return "User performed desktop activities including screen navigation and possible application usage."
        elif "actions" in prompt_lower:
            return "Detected actions: Screen viewing, potential clicking, and keyboard interaction."
        elif "automation" in prompt_lower:
            return "This workflow shows potential for automation if repetitive patterns are confirmed in future sessions."
        else:
            return "Analysis completed using rule-based system. Install Ollama for advanced LLM analysis."

def analyze_session_with_llm(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze session data using local LLM
    
    Args:
        session_data: Complete session data with OCR and transcription
    
    Returns:
        LLM analysis results
    """
    print("   Initializing local LLM...")
    
    # Initialize LLM
    llm = LocalLLM(backend="ollama", model="phi3:latest")
    
    if not llm.is_available():
        print("   ⚠️  Ollama not available. Using rule-based analysis.")
        print("   💡 Install Ollama (https://ollama.ai) for better results!")
    
    # Prepare context for LLM
    context = prepare_context_for_llm(session_data)
    
    # Generate analysis
    analysis = {}
    
    # 1. Workflow Summary
    print("   Analyzing workflow...")
    summary_prompt = f"""Analyze this desktop session and provide a brief summary of what the user did.

Context:
{context}

Provide a concise 2-3 sentence summary of the user's workflow."""
    
    analysis['workflow_summary'] = llm.generate(summary_prompt)
    
    # 2. Detect Actions
    print("   Detecting actions...")
    actions = detect_actions_from_session(session_data)
    analysis['detected_actions'] = actions
    
    # 3. Detect Patterns
    print("   Analyzing patterns...")
    patterns = detect_patterns(session_data, actions)
    analysis['detected_patterns'] = patterns
    
    # 4. Automation Suggestions
    print("   Generating automation suggestions...")
    automation_prompt = f"""Based on this desktop session, suggest how it could be automated.

Context:
{context}

Actions detected: {', '.join(actions[:5])}

Provide 2-3 specific automation suggestions."""
    
    suggestions_text = llm.generate(automation_prompt)
    analysis['automation_suggestions'] = suggestions_text.split('\n')[:3]
    
    # 5. Calculate Automation Potential
    potential = calculate_automation_potential(session_data, actions, patterns)
    analysis['automation_potential'] = potential
    
    # 6. Generate Automation Steps (if high potential)
    if potential >= 7:
        print("   Generating automation steps...")
        analysis['automation_steps'] = generate_automation_steps(session_data, actions)
    
    # 7. Metadata
    analysis['metadata'] = {
        'session_id': session_data.get('session_id'),
        'timestamp': session_data.get('timestamp'),
        'llm_backend': llm.backend,
        'llm_model': llm.model
    }
    
    return analysis

def prepare_context_for_llm(session_data: Dict[str, Any]) -> str:
    """Prepare concise context for LLM"""
    context_parts = []
    
    # OCR text
    ocr_results = session_data.get('ocr_results', [])
    if ocr_results:
        all_text = ' '.join([r.get('text', '')[:200] for r in ocr_results if r.get('success')])
        context_parts.append(f"Screen text: {all_text[:500]}")
    
    # Audio transcription
    transcription = session_data.get('audio_transcription', {})
    if transcription.get('success'):
        context_parts.append(f"User said: {transcription.get('text', '')[:300]}")
    
    # UI elements
    ui_elements = []
    for ocr in ocr_results:
        ui_elements.extend(ocr.get('ui_elements', []))
    if ui_elements:
        context_parts.append(f"UI elements detected: {len(ui_elements)}")
    
    return '\n'.join(context_parts)

def detect_actions_from_session(session_data: Dict[str, Any]) -> List[str]:
    """Detect user actions from session data"""
    actions = []
    
    # From OCR - detect UI interactions
    ocr_results = session_data.get('ocr_results', [])
    for ocr in ocr_results:
        ui_elements = ocr.get('ui_elements', [])
        for element in ui_elements:
            if element['type'] == 'button':
                actions.append(f"Clicked button: {element['text']}")
            elif element['type'] == 'input':
                actions.append(f"Interacted with input: {element['text']}")
    
    # From audio - detect voice commands
    transcription = session_data.get('audio_transcription', {})
    if transcription.get('success'):
        from modules.processing.stt_processor import extract_commands_from_transcription
        commands = extract_commands_from_transcription(transcription)
        for cmd in commands:
            actions.append(f"Voice command: {cmd['command']}")
    
    # If no specific actions detected, infer general ones
    if not actions:
        actions = [
            "Viewed screen content",
            "Navigated desktop",
            "Potential mouse/keyboard interaction"
        ]
    
    return actions

def detect_patterns(session_data: Dict[str, Any], actions: List[str]) -> List[str]:
    """Detect repetitive patterns"""
    patterns = []
    
    # Check for repeated actions
    action_types = {}
    for action in actions:
        action_type = action.split(':')[0]
        action_types[action_type] = action_types.get(action_type, 0) + 1
    
    for action_type, count in action_types.items():
        if count >= 2:
            patterns.append(f"Repeated {count}x: {action_type}")
    
    # Check for sequential patterns in OCR text
    ocr_results = session_data.get('ocr_results', [])
    if len(ocr_results) >= 3:
        patterns.append("Multi-step workflow detected across screenshots")
    
    return patterns if patterns else ["No clear patterns detected in single session"]

def calculate_automation_potential(session_data: Dict[str, Any], 
                                   actions: List[str], 
                                   patterns: List[str]) -> int:
    """Calculate automation potential (0-10)"""
    score = 0
    
    # Base score for any activity
    score += 2
    
    # Bonus for detected actions
    score += min(len(actions), 3)
    
    # Bonus for patterns
    score += min(len(patterns), 2)
    
    # Bonus for UI element detection
    ocr_results = session_data.get('ocr_results', [])
    total_ui_elements = sum(len(ocr.get('ui_elements', [])) for ocr in ocr_results)
    if total_ui_elements >= 5:
        score += 2
    elif total_ui_elements >= 2:
        score += 1
    
    # Bonus for voice commands
    transcription = session_data.get('audio_transcription', {})
    if transcription.get('success') and transcription.get('text'):
        score += 1
    
    return min(score, 10)

def generate_automation_steps(session_data: Dict[str, Any], 
                               actions: List[str]) -> List[Dict[str, Any]]:
    """Generate automation steps from detected actions"""
    steps = []
    
    for i, action in enumerate(actions):
        if "Clicked button" in action:
            button_text = action.split(':')[1].strip()
            steps.append({
                "step": i + 1,
                "action": "click",
                "target": button_text,
                "description": f"Click button '{button_text}'"
            })
        
        elif "Interacted with input" in action:
            input_text = action.split(':')[1].strip()
            steps.append({
                "step": i + 1,
                "action": "type",
                "target": input_text,
                "description": f"Type into field '{input_text}'"
            })
        
        elif "Voice command" in action:
            command = action.split(':')[1].strip()
            steps.append({
                "step": i + 1,
                "action": "execute",
                "command": command,
                "description": f"Execute command: {command}"
            })
        
        else:
            steps.append({
                "step": i + 1,
                "action": "generic",
                "description": action
            })
    
    return steps