# demo.py - Interactive Demo for AGI Assistant
"""
Interactive demo script to showcase all features
"""

import time
from pathlib import Path
import json

def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         🤖 AGI ASSISTANT - INTERACTIVE DEMO 🤖            ║
    ║                                                            ║
    ║         Watch. Learn. Automate. (Locally)                 ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_menu():
    print("\n" + "="*60)
    print("📋 DEMO MENU")
    print("="*60)
    print("1. 🎬 Run Full Demo (30s recording)")
    print("2. 🧪 Quick Test (10s recording)")
    print("3. 📊 View Saved Workflows")
    print("4. 🔍 Analyze Existing Session")
    print("5. 🤖 Preview Automation (Dry Run)")
    print("6. 📁 Show Storage Stats")
    print("7. 🧹 Clean Old Data")
    print("8. ℹ️  Show System Info")
    print("9. ❌ Exit")
    print("="*60)
    
    choice = input("\nSelect option (1-9): ").strip()
    return choice

def run_full_demo():
    """Run a full 30-second recording demo"""
    print("\n" + "="*60)
    print("🎬 FULL DEMO - 30 Second Recording")
    print("="*60)
    print("\n📝 Instructions:")
    print("   1. The system will record your screen for 30 seconds")
    print("   2. During recording, try to:")
    print("      • Open an application (e.g., Notepad, Excel)")
    print("      • Type something")
    print("      • Click some buttons")
    print("      • Optionally speak commands like 'save file'")
    print("   3. System will analyze and suggest automation")
    print("\n⏱️  Recording starts in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...", end='\r')
        time.sleep(1)
    
    print("\n🔴 RECORDING NOW! Do your workflow...")
    
    # Run the actual system
    from main import AGIAssistant
    assistant = AGIAssistant(session_duration=30, screenshot_interval=3)
    session_data, llm_analysis = assistant.start_observation()
    
    return session_data, llm_analysis

def run_quick_test():
    """Run a quick 10-second test"""
    print("\n" + "="*60)
    print("🧪 QUICK TEST - 10 Second Recording")
    print("="*60)
    print("\n⏱️  Recording starts in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"   {i}...", end='\r')
        time.sleep(1)
    
    print("\n🔴 RECORDING! Move your mouse and click something...")
    
    from main import AGIAssistant
    assistant = AGIAssistant(session_duration=10, screenshot_interval=2)
    session_data, llm_analysis = assistant.start_observation()
    
    return session_data, llm_analysis

def view_workflows():
    """View all saved workflows"""
    print("\n" + "="*60)
    print("📊 SAVED WORKFLOWS")
    print("="*60)
    
    workflows_dir = Path("data/workflows")
    
    if not workflows_dir.exists() or not list(workflows_dir.glob("*.json")):
        print("\n⚠️  No workflows saved yet")
        print("💡 Run a demo first to generate workflows")
        return
    
    workflows = sorted(workflows_dir.glob("workflow_*.json"), 
                      key=lambda p: p.stat().st_mtime, reverse=True)
    
    for i, wf_path in enumerate(workflows, 1):
        try:
            with open(wf_path, 'r') as f:
                wf = json.load(f)
            
            print(f"\n{i}. {wf_path.name}")
            print(f"   ID: {wf.get('workflow_id')}")
            print(f"   Created: {wf.get('created_at', 'Unknown')}")
            print(f"   Steps: {len(wf.get('automation_steps', []))}")
            
            # Show first few steps
            steps = wf.get('automation_steps', [])[:3]
            if steps:
                print(f"   First steps:")
                for step in steps:
                    print(f"      • {step.get('description')}")
        
        except Exception as e:
            print(f"\n{i}. {wf_path.name} (Error: {e})")

def analyze_existing_session():
    """Analyze an existing session file"""
    print("\n" + "="*60)
    print("🔍 ANALYZE EXISTING SESSION")
    print("="*60)
    
    json_dir = Path("data/json")
    
    if not json_dir.exists():
        print("\n⚠️  No sessions found")
        return
    
    sessions = sorted(json_dir.glob("session_summary_*.json"),
                     key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not sessions:
        print("\n⚠️  No sessions found")
        return
    
    print(f"\nFound {len(sessions)} session(s). Analyzing most recent...")
    
    latest_session = sessions[0]
    
    try:
        with open(latest_session, 'r') as f:
            data = json.load(f)
        
        session_data = data.get('session_data', {})
        llm_analysis = data.get('llm_analysis', {})
        
        print(f"\n📄 Session: {latest_session.name}")
        print(f"   ID: {session_data.get('session_id')}")
        print(f"   Timestamp: {session_data.get('timestamp')}")
        print(f"   Duration: {session_data.get('duration')}s")
        print(f"   Screenshots: {len(session_data.get('screenshots', []))}")
        
        # Show analysis
        if llm_analysis:
            print(f"\n🧠 Analysis:")
            print(f"   Automation Potential: {llm_analysis.get('automation_potential', 'N/A')}/10")
            print(f"   Actions Detected: {len(llm_analysis.get('detected_actions', []))}")
            print(f"   Patterns: {len(llm_analysis.get('detected_patterns', []))}")
            
            summary = llm_analysis.get('workflow_summary', '')
            if summary:
                print(f"\n   Summary: {summary}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

def preview_automation():
    """Preview automation in dry-run mode"""
    print("\n" + "="*60)
    print("🤖 AUTOMATION PREVIEW (Dry Run)")
    print("="*60)
    
    workflows_dir = Path("data/workflows")
    
    if not workflows_dir.exists() or not list(workflows_dir.glob("*.json")):
        print("\n⚠️  No workflows available")
        return
    
    workflows = sorted(workflows_dir.glob("workflow_*.json"),
                      key=lambda p: p.stat().st_mtime, reverse=True)
    
    latest_workflow = workflows[0]
    print(f"\n📄 Using: {latest_workflow.name}")
    
    from run_automation import AutomationRunner
    runner = AutomationRunner(str(latest_workflow))
    runner.execute_workflow(dry_run=True)

def show_storage_stats():
    """Show storage statistics"""
    print("\n" + "="*60)
    print("📁 STORAGE STATISTICS")
    print("="*60)
    
    from modules.storage.data_manager import get_storage_info
    
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("\n⚠️  No data directory found")
        return
    
    stats = get_storage_info(data_dir)
    
    print(f"\n📊 Storage Usage:")
    print(f"   Clips: {stats['clips_size_mb']:.2f} MB ({stats['clips_count']} files)")
    print(f"   JSON: {stats['json_size_mb']:.2f} MB ({stats['json_count']} files)")
    print(f"   Workflows: {stats['workflows_size_mb']:.2f} MB ({stats['workflows_count']} files)")
    print(f"   ─────────────────────────────")
    print(f"   Total: {stats['total_size_mb']:.2f} MB ({stats['file_count']} files)")
    
    if stats['total_size_mb'] > 500:
        print(f"\n⚠️  Storage is high. Consider cleaning old data.")

def clean_old_data():
    """Clean old data files"""
    print("\n" + "="*60)
    print("🧹 CLEAN OLD DATA")
    print("="*60)
    
    print("\nThis will delete clips and sessions older than 7 days.")
    print("Workflows are never deleted automatically.")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return
    
    from modules.storage.data_manager import cleanup_old_data
    
    data_dir = Path("data")
    stats = cleanup_old_data(data_dir, days_to_keep=7)
    
    print(f"\n✅ Cleanup complete:")
    print(f"   Files deleted: {stats['files_deleted']}")
    print(f"   Space freed: {stats['space_freed_mb']:.2f} MB")
    
    if stats['errors']:
        print(f"\n⚠️  {len(stats['errors'])} errors occurred")

def show_system_info():
    """Show system information"""
    print("\n" + "="*60)
    print("ℹ️  SYSTEM INFORMATION")
    print("="*60)
    
    import sys
    import platform
    
    print(f"\n🖥️  System:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Architecture: {platform.machine()}")
    
    print(f"\n📦 Dependencies:")
    
    # Check each dependency
    deps = {
        "PIL": "Pillow (Image processing)",
        "numpy": "NumPy (Array operations)",
        "cv2": "OpenCV (Computer vision)",
        "mss": "MSS (Screen capture)",
        "sounddevice": "SoundDevice (Audio recording)",
        "whisper": "OpenAI Whisper (Speech-to-text)",
        "pytesseract": "PyTesseract (OCR)",
    }
    
    for module, desc in deps.items():
        try:
            __import__(module)
            print(f"   ✅ {desc}")
        except ImportError:
            print(f"   ❌ {desc}")
    
    # Check Tesseract
    print(f"\n🔧 External Tools:")
    try:
        import subprocess
        result = subprocess.run(["tesseract", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"   ✅ {version}")
        else:
            print(f"   ❌ Tesseract OCR (Not found)")
    except:
        print(f"   ❌ Tesseract OCR (Not found)")
    
    # Check Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"   ✅ Ollama ({len(models)} model(s) installed)")
        else:
            print(f"   ⚠️  Ollama (Not running)")
    except:
        print(f"   ⚠️  Ollama (Not running)")

def show_help():
    """Show usage tips"""
    print("\n" + "="*60)
    print("💡 USAGE TIPS")
    print("="*60)
    
    tips = [
        "🎯 Best Practices:",
        "   • Perform repetitive tasks for better pattern detection",
        "   • Speak commands clearly for voice recognition",
        "   • Use well-defined workflows (open → edit → save)",
        "   • Run multiple sessions to improve learning",
        "",
        "🔧 Optimization:",
        "   • Install Ollama for better LLM analysis",
        "   • Use SSD for faster screenshot processing",
        "   • Clean old data regularly to save space",
        "   • Keep recording sessions under 60 seconds",
        "",
        "🐛 Troubleshooting:",
        "   • If OCR fails: Check Tesseract installation",
        "   • If audio fails: Check microphone permissions",
        "   • If slow: Reduce screenshot interval",
        "   • If storage full: Run cleanup option",
        "",
        "🚀 Round 2 Ready:",
        "   • Workflows with 7+ potential score are automation-ready",
        "   • JSON files contain structured automation steps",
        "   • Use run_automation.py to execute workflows",
    ]
    
    for tip in tips:
        print(tip)

def main():
    """Main demo loop"""
    print_banner()
    
    # Check if setup is complete
    setup_file = Path("data")
    if not setup_file.exists():
        print("\n⚠️  First time setup detected!")
        print("💡 Run 'python setup.py' first to configure the system\n")
        return
    
    while True:
        choice = show_menu()
        
        try:
            if choice == '1':
                run_full_demo()
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                run_quick_test()
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                view_workflows()
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                analyze_existing_session()
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                preview_automation()
                input("\nPress Enter to continue...")
            
            elif choice == '6':
                show_storage_stats()
                input("\nPress Enter to continue...")
            
            elif choice == '7':
                clean_old_data()
                input("\nPress Enter to continue...")
            
            elif choice == '8':
                show_system_info()
                show_help()
                input("\nPress Enter to continue...")
            
            elif choice == '9':
                print("\n👋 Thanks for using AGI Assistant!")
                print("🏆 Good luck with the hackathon!\n")
                break
            
            else:
                print("\n⚠️  Invalid choice. Please select 1-9.")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()