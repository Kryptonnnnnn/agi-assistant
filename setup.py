# setup.py - AGI Assistant Setup Script
"""
Automated setup script to check dependencies and configure the system
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor >= 9:
        print_success(f"Python {version_str} detected")
        return True
    else:
        print_error(f"Python {version_str} detected")
        print_error("Python 3.9 or higher is required")
        return False

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print_success("pip is installed")
        return True
    except:
        print_error("pip is not installed")
        return False

def install_requirements():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print_error("requirements.txt not found")
        return False
    
    try:
        print("Installing packages (this may take a few minutes)...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print_success("All Python packages installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install some packages")
        return False

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    print_header("Checking Tesseract OCR")
    
    try:
        result = subprocess.run(["tesseract", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print_success(f"Tesseract is installed: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print_warning("Tesseract OCR is not installed")
    print("\n📥 Installation instructions:")
    
    system = platform.system()
    if system == "Windows":
        print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   After installation, add to PATH or update ocr_processor.py")
    elif system == "Darwin":
        print("   macOS: Run 'brew install tesseract'")
    elif system == "Linux":
        print("   Linux: Run 'sudo apt-get install tesseract-ocr'")
    
    return False

def check_ollama():
    """Check if Ollama is installed"""
    print_header("Checking Ollama (Optional)")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print_success(f"Ollama is running with {len(models)} model(s)")
            
            if models:
                print("\n📋 Available models:")
                for model in models:
                    print(f"   - {model['name']}")
            else:
                print_warning("No models installed. Run: ollama pull llama3.2:1b")
            
            return True
    except:
        pass
    
    print_warning("Ollama is not running (will use fallback analysis)")
    print("\n💡 For better LLM analysis:")
    print("   1. Install from: https://ollama.ai")
    print("   2. Run: ollama pull llama3.2:1b")
    print("   3. Ollama will run in background")
    
    return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        "data/clips",
        "data/json",
        "data/workflows",
        "modules/capture",
        "modules/processing",
        "modules/llm",
        "modules/storage",
        "modules/automation"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files
    for module_dir in ["modules", "modules/capture", "modules/processing", 
                       "modules/llm", "modules/storage", "modules/automation"]:
        init_file = Path(module_dir) / "__init__.py"
        init_file.touch(exist_ok=True)
    
    print_success(f"Created {len(directories)} directories")
    return True

def check_disk_space():
    """Check available disk space"""
    print_header("Checking Disk Space")
    
    try:
        import shutil
        stats = shutil.disk_usage(".")
        free_gb = stats.free / (1024**3)
        
        if free_gb > 5:
            print_success(f"Available space: {free_gb:.1f} GB")
            return True
        else:
            print_warning(f"Low disk space: {free_gb:.1f} GB")
            print("   Recommended: At least 5 GB free for recordings")
            return True
    except:
        print_warning("Could not check disk space")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    print_header("Testing Module Imports")
    
    required_modules = [
        ("PIL", "Pillow"),
        ("numpy", "numpy"),
        ("cv2", "opencv-python"),
        ("mss", "mss"),
        ("sounddevice", "sounddevice"),
        ("soundfile", "soundfile"),
        ("whisper", "openai-whisper"),
        ("pytesseract", "pytesseract"),
    ]
    
    all_ok = True
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print_success(f"{package_name}")
        except ImportError:
            print_error(f"{package_name} - Not found")
            all_ok = False
    
    return all_ok

def run_quick_test():
    """Run a quick functionality test"""
    print_header("Running Quick Test")
    
    try:
        # Test screen capture
        import mss
        with mss.mss() as sct:
            monitor = sct.monitors[1]
        print_success("Screen capture: OK")
        
        # Test audio devices
        import sounddevice as sd
        devices = sd.query_devices()
        print_success(f"Audio devices: {len(devices)} found")
        
        # Test OCR
        import pytesseract
        from PIL import Image
        print_success("OCR module: OK")
        
        return True
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def main():
    """Main setup routine"""
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"🤖 AGI ASSISTANT - SETUP WIZARD")
    print(f"{'='*60}{Colors.END}\n")
    
    # Track setup status
    checks = {
        "Python Version": check_python_version(),
        "pip": check_pip(),
    }
    
    if not all(checks.values()):
        print_error("\n❌ Critical dependencies missing. Please install them first.")
        return False
    
    # Create directories
    checks["Directories"] = create_directories()
    
    # Install requirements
    print("\nDo you want to install Python dependencies? (y/n): ", end='')
    if input().lower().strip() == 'y':
        checks["Python Packages"] = install_requirements()
    else:
        print_warning("Skipped Python package installation")
        checks["Python Packages"] = None
    
    # Check external dependencies
    checks["Tesseract OCR"] = check_tesseract()
    checks["Ollama LLM"] = check_ollama()
    checks["Disk Space"] = check_disk_space()
    
    # Test imports if packages were installed
    if checks["Python Packages"]:
        checks["Module Imports"] = test_imports()
        checks["Quick Test"] = run_quick_test()
    
    # Summary
    print_header("Setup Summary")
    
    for check_name, status in checks.items():
        if status is True:
            print_success(check_name)
        elif status is False:
            print_error(check_name)
        elif status is None:
            print_warning(f"{check_name} (Skipped)")
    
    # Final verdict
    critical_checks = ["Python Version", "pip", "Python Packages", "Module Imports"]
    critical_ok = all(checks.get(c) for c in critical_checks if checks.get(c) is not None)
    
    print("\n" + "="*60)
    if critical_ok:
        print_success("✅ Setup complete! You can now run: python main.py")
        
        if not checks.get("Tesseract OCR"):
            print_warning("\n⚠️  Install Tesseract OCR for better results")
        
        if not checks.get("Ollama LLM"):
            print_warning("⚠️  Install Ollama for enhanced LLM analysis")
    else:
        print_error("❌ Setup incomplete. Please resolve errors above.")
    
    print("="*60 + "\n")
    
    return critical_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)