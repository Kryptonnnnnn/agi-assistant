# run_full_demo.py - Complete Integrated Demo
"""
This script demonstrates the ENTIRE system:
1. Records a workflow
2. Analyzes it
3. Opens dashboard
4. Lets you automate it
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def print_banner(text):
    """Print a fancy banner"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required = {
        'flask': 'Flask',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'cv2': 'OpenCV',
        'mss': 'MSS',
        'sounddevice': 'SoundDevice',
        'whisper': 'OpenAI Whisper',
        'pytesseract': 'PyTesseract'
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name}")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True

def run_recording_session():
    """Run a recording session"""
    print_banner("STEP 1: RECORD A WORKFLOW")
    
    print("📹 Let's record a workflow!")
    print("\n💡 Suggested workflow:")
    print("   1. Open Notepad (Win+R → notepad → Enter)")
    print("   2. Type: 'AGI Assistant Demo'")
    print("   3. Save file (Ctrl+S)")
    print("   4. Type filename and press Enter")
    print("   5. Close Notepad")
    
    print("\n⏱️  This will take about 40 seconds...")
    input("\n👉 Press Enter when ready to start recording...")
    
    print("\n🔴 STARTING RECORDING IN 3 SECONDS...")
    time.sleep(3)
    
    # Run main.py
    subprocess.run([sys.executable, "main.py"])
    
    print("\n✅ Recording complete!")
    time.sleep(2)

def show_results():
    """Show the analysis results"""
    print_banner("STEP 2: REVIEW RESULTS")
    
    # Find the latest workflow
    workflows_dir = Path("data/workflows")
    
    if not workflows_dir.exists() or not list(workflows_dir.glob("*.json")):
        print("⚠️  No workflow found. Recording may have failed.")
        return None
    
    latest_workflow = max(workflows_dir.glob("workflow_*.json"), 
                         key=lambda p: p.stat().st_mtime)
    
    print(f"📄 Latest workflow: {latest_workflow.name}")
    
    # Load and display
    import json
    with open(latest_workflow, 'r') as f:
        workflow = json.load(f)
    
    print(f"\n📊 Workflow Statistics:")
    print(f"   • ID: {workflow.get('workflow_id')}")
    print(f"   • Steps: {len(workflow.get('automation_steps', []))}")
    print(f"   • Created: {workflow.get('created_at')}")
    
    # Show first few steps
    steps = workflow.get('automation_steps', [])
    if steps:
        print(f"\n🎯 First few automation steps:")
        for step in steps[:3]:
            print(f"   {step['step']}. {step.get('description', 'N/A')}")
        
        if len(steps) > 3:
            print(f"   ... and {len(steps) - 3} more steps")
    
    return workflow.get('workflow_id')

def launch_dashboard(workflow_id):
    """Launch the dashboard"""
    print_banner("STEP 3: LAUNCH VISUAL DASHBOARD")
    
    print("🎨 Starting the Visual Dashboard...")
    print("📊 URL: http://localhost:5000")
    print("\n✨ Features you'll see:")
    print("   ✅ Visual workflow viewer")
    print("   ✅ One-click automation button")
    print("   ✅ Real-time execution feedback")
    print("   ✅ Continual learning tracking")
    
    print("\n⏱️  Opening browser in 3 seconds...")
    print("⚠️  Dashboard will stay open until you press Ctrl+C here\n")
    
    time.sleep(3)
    
    # Open browser
    webbrowser.open('http://localhost:5000')
    
    print("="*60)
    print("🎉 DASHBOARD IS NOW RUNNING!")
    print("="*60)
    print("\n📋 What to do next:")
    print("   1. Look at the dashboard in your browser")
    print("   2. Find your workflow (it should be at the top)")
    print("   3. Click '▶️ Automate This' button")
    print("   4. Watch the real-time feedback!")
    print("   5. Run it multiple times to see learning in action")
    print("\n⚠️  Press Ctrl+C here when done to stop the dashboard")
    print("="*60 + "\n")
    
    # Start dashboard
    subprocess.run([sys.executable, "dashboard.py"])

def main():
    """Main demo flow"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║     🤖 AGI ASSISTANT - COMPLETE INTEGRATED DEMO 🤖        ║
    ║                                                            ║
    ║           Watch → Learn → Automate → Improve              ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print("This demo will:")
    print("  1️⃣  Record a workflow (30 seconds)")
    print("  2️⃣  Analyze it with AI")
    print("  3️⃣  Show results")
    print("  4️⃣  Launch visual dashboard")
    print("  5️⃣  Let you automate with one click")
    
    print("\n💡 This demonstrates ALL bonus features:")
    print("   ✅ Visual dashboard")
    print("   ✅ Toggle to automate")
    print("   ✅ Real-time feedback with reasoning")
    print("   ✅ Continual learning")
    
    input("\n👉 Press Enter to start the full demo...")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        print("Run: pip install -r requirements.txt")
        return
    
    # Step 2: Record workflow
    run_recording_session()
    
    # Step 3: Show results
    workflow_id = show_results()
    
    if not workflow_id:
        print("\n❌ Demo cannot continue without a workflow")
        return
    
    print("\n✅ Workflow successfully recorded and analyzed!")
    input("\n👉 Press Enter to launch the dashboard...")
    
    # Step 4: Launch dashboard
    try:
        launch_dashboard(workflow_id)
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("👋 DEMO COMPLETE!")
        print("="*60)
        print("\n🎉 What you just experienced:")
        print("   ✅ Recorded a workflow")
        print("   ✅ AI analyzed it automatically")
        print("   ✅ Viewed it in beautiful dashboard")
        print("   ✅ (Hopefully) Automated it with one click!")
        print("   ✅ Saw real-time feedback and learning")
        
        print("\n🏆 This is a COMPLETE Round 1 + Bonus submission!")
        print("\n📹 Now record this demo for your submission video!")
        print("\n💡 Tips for video:")
        print("   • Show the whole flow like you just experienced")
        print("   • Highlight the visual dashboard")
        print("   • Show the one-click automation")
        print("   • Point out the real-time feedback")
        print("   • Demonstrate the learning by running 2-3 times")
        
        print("\n🚀 YOU'RE READY TO WIN! 🚀\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
