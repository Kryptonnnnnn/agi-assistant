# main.py - AGI Assistant: Complete Observe & Understand System

import os
import json
import time
from datetime import datetime
from pathlib import Path

# Import modules
from modules.capture.screen_recorder import capture_screenshots
from modules.capture.audio_recorder import record_audio
from modules.processing.ocr_processor import extract_text_from_screenshots
from modules.processing.stt_processor import transcribe_audio
from modules.llm.local_llm import analyze_session_with_llm
from modules.storage.data_manager import cleanup_old_data, get_storage_info

class AGIAssistant:
    def __init__(self, session_duration=15, screenshot_interval=3):
        """
        Initialize AGI Assistant
        
        Args:
            session_duration: Recording session length in seconds
            screenshot_interval: Time between screenshots in seconds
        """
        self.session_duration = session_duration
        self.screenshot_interval = screenshot_interval
        self.data_dir = Path("data")
        self.clips_dir = self.data_dir / "clips"
        self.json_dir = self.data_dir / "json"
        self.workflows_dir = self.data_dir / "workflows"
        
        # Create directories
        for d in [self.clips_dir, self.json_dir, self.workflows_dir]:
            d.mkdir(parents=True, exist_ok=True)
    
    def start_observation(self):
        """Main observation loop - captures screen and audio"""
        print("\n" + "="*60)
        print("=== AGI Assistant: Observe & Understand ===")
        print("="*60)
        print(f"📹 Recording for {self.session_duration} seconds...")
        print(f"📸 Taking screenshots every {self.screenshot_interval} seconds")
        print(f"🎤 Recording audio continuously")
        print("="*60 + "\n")
        
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Step 1: Capture Screenshots
        print("📸 Capturing screenshots...")
        screenshot_paths = capture_screenshots(
            duration=self.session_duration,
            interval=self.screenshot_interval,
            output_dir=self.clips_dir,
            session_id=session_id
        )
        print(f"✅ Saved {len(screenshot_paths)} screenshots\n")
        
        # Step 2: Record Audio
        print("🎤 Recording audio...")
        audio_path = record_audio(
            duration=self.session_duration,
            output_dir=self.clips_dir,
            session_id=session_id
        )
        print(f"✅ Audio saved: {audio_path}\n")
        
        # Step 3: Extract Text from Screenshots (OCR)
        print("🔍 Extracting text from screenshots (OCR)...")
        ocr_results = extract_text_from_screenshots(screenshot_paths)
        print(f"✅ OCR completed for {len(ocr_results)} screenshots\n")
        
        # Step 4: Transcribe Audio (Speech-to-Text)
        print("📝 Transcribing audio...")
        audio_transcription = transcribe_audio(audio_path)
        print(f"✅ Audio transcribed: '{audio_transcription.get('text', '')[:100]}...'\n")
        
        # Step 5: Analyze with LLM
        print("🧠 Analyzing session with local LLM...")
        session_data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "screenshots": screenshot_paths,
            "audio_file": audio_path,
            "ocr_results": ocr_results,
            "audio_transcription": audio_transcription,
            "duration": self.session_duration
        }
        
        llm_analysis = analyze_session_with_llm(session_data)
        
        # Step 6: Save Results
        summary_path = self.json_dir / f"session_summary_{session_id}.json"
        with open(summary_path, 'w') as f:
            json.dump({
                "session_data": session_data,
                "llm_analysis": llm_analysis
            }, f, indent=2, default=str)
        
        print(f"✅ Session summary saved: {summary_path}\n")
        
        # Step 7: Display Insights
        self.display_insights(llm_analysis)
        
        # Step 8: Storage Management
        print("\n📊 Storage Management:")
        storage_info = get_storage_info(self.data_dir)
        print(f"   Total size: {storage_info['total_size_mb']:.2f} MB")
        print(f"   Files: {storage_info['file_count']}")
        
        # Cleanup old data if needed
        cleanup_threshold_mb = 500  # Cleanup if storage exceeds 500MB
        if storage_info['total_size_mb'] > cleanup_threshold_mb:
            print(f"\n🧹 Cleaning up old data (threshold: {cleanup_threshold_mb}MB)...")
            cleanup_old_data(self.data_dir, days_to_keep=7)
        
        print("\n" + "="*60)
        print("✅ Session Complete! Ready for automation.")
        print("="*60 + "\n")
        
        return session_data, llm_analysis
    
    def display_insights(self, llm_analysis):
        """Display LLM analysis insights"""
        print("\n" + "="*60)
        print("🧠 LLM ANALYSIS & INSIGHTS")
        print("="*60)
        
        if not llm_analysis:
            print("⚠️  No analysis available")
            return
        
        # Display workflow summary
        if "workflow_summary" in llm_analysis:
            print("\n📋 Workflow Summary:")
            print(f"   {llm_analysis['workflow_summary']}")
        
        # Display detected actions
        if "detected_actions" in llm_analysis:
            print(f"\n🎯 Detected Actions ({len(llm_analysis['detected_actions'])}):")
            for i, action in enumerate(llm_analysis['detected_actions'][:5], 1):
                print(f"   {i}. {action}")
            if len(llm_analysis['detected_actions']) > 5:
                print(f"   ... and {len(llm_analysis['detected_actions']) - 5} more")
        
        # Display automation suggestions
        if "automation_suggestions" in llm_analysis:
            print("\n🤖 Automation Suggestions:")
            for suggestion in llm_analysis['automation_suggestions']:
                print(f"   • {suggestion}")
        
        # Display patterns
        if "detected_patterns" in llm_analysis:
            print("\n🔄 Detected Patterns:")
            for pattern in llm_analysis['detected_patterns']:
                print(f"   • {pattern}")
        
        # Display automation potential
        if "automation_potential" in llm_analysis:
            potential = llm_analysis['automation_potential']
            print(f"\n⚡ Automation Potential: {potential}/10")
            
            if potential >= 7:
                print("   ✅ Highly automatable workflow detected!")
            elif potential >= 4:
                print("   ⚠️  Partially automatable - may need user input")
            else:
                print("   ℹ️  Low automation potential - too variable")
        
        print("\n" + "="*60)

def main():
    """Main entry point"""
    # Configuration
    SESSION_DURATION = 30  # seconds
    SCREENSHOT_INTERVAL = 3  # seconds
    
    # Initialize assistant
    assistant = AGIAssistant(
        session_duration=SESSION_DURATION,
        screenshot_interval=SCREENSHOT_INTERVAL
    )
    
    # Start observation
    try:
        session_data, llm_analysis = assistant.start_observation()
        
        # Save workflow if automation potential is high
        if llm_analysis and llm_analysis.get("automation_potential", 0) >= 7:
            workflow_path = assistant.workflows_dir / f"workflow_{session_data['session_id']}.json"
            with open(workflow_path, 'w') as f:
                json.dump({
                    "workflow_id": session_data['session_id'],
                    "created_at": datetime.now().isoformat(),
                    "automation_steps": llm_analysis.get("automation_steps", []),
                    "metadata": llm_analysis.get("metadata", {})
                }, f, indent=2)
            print(f"\n💾 Automatable workflow saved: {workflow_path}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()