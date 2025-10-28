# setup_git.py - Prepare repository for Git upload
"""
This script:
1. Creates .gitkeep files to preserve directory structure
2. Creates .gitignore
3. Provides Git commands to run
"""

from pathlib import Path

def create_gitkeep_files():
    """Create .gitkeep files in data directories"""
    directories = [
        "data/clips",
        "data/json",
        "data/workflows",
        "templates"
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep file
        gitkeep = dir_path / ".gitkeep"
        gitkeep.touch()
        print(f"   ✅ Created {gitkeep}")
    
    print("\n✅ Directory structure ready for Git!\n")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# AGI Assistant .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Data files (recordings - too large!)
data/clips/*.png
data/clips/*.wav
data/clips/*.mp4
data/json/session_summary_*.json
data/workflows/workflow_*.json
data/learning_database.json

# Keep directory structure
!data/clips/.gitkeep
!data/json/.gitkeep
!data/workflows/.gitkeep

# Models (Large files)
*.pth
*.bin
*.pt
models/

# Logs
*.log

# OS
Thumbs.db
.DS_Store

# Temporary files
temp/
tmp/
*.tmp

# Flask
instance/
.webassets-cache

# Environment
.env
.env.local

# Large videos (upload separately)
demo_video.mp4
*.mp4
"""
    
    gitignore_path = Path(".gitignore")
    
    if gitignore_path.exists():
        print("⚠️  .gitignore already exists")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Skipped .gitignore creation")
            return
    
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore\n")

def show_git_commands():
    """Display Git commands to run"""
    commands = """
╔══════════════════════════════════════════════════════════╗
║  GIT COMMANDS TO RUN                                     ║
╚══════════════════════════════════════════════════════════╝

📝 STEP 1: Initialize Git repository (if not done)
────────────────────────────────────────────────────────
git init


📝 STEP 2: Add all files
────────────────────────────────────────────────────────
git add .


📝 STEP 3: Check what will be committed
────────────────────────────────────────────────────────
git status


📝 STEP 4: Commit
────────────────────────────────────────────────────────
git commit -m "🤖 AGI Assistant - Complete submission with all bonus features

- Complete Round 1: Observe & Understand system
- Visual Dashboard with beautiful UI
- One-click automation toggle
- Real-time feedback with AI reasoning
- Continual learning system
- All bonus features implemented
- Professional documentation
- Production-ready code"


📝 STEP 5: Create GitHub repository
────────────────────────────────────────────────────────
Go to: https://github.com/new

Repository name: agi-assistant-hackathon
Description: AGI Assistant - Desktop AI that watches, learns, and automates
✅ Public (so judges can see it)
❌ Don't initialize with README (you have one)


📝 STEP 6: Add remote and push
────────────────────────────────────────────────────────
git remote add origin https://github.com/kryptonnnnnn/agi-assistant-hackathon.git
git branch -M main
git push -u origin main


📝 OPTIONAL: Create a release tag
────────────────────────────────────────────────────────
git tag -a v1.0 -m "Hackathon submission - Round 1 complete with all bonus features"
git push origin v1.0


✅ Done! Your code is now on GitHub!

"""
    print(commands)

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║  AGI ASSISTANT - GIT SETUP                               ║
╚══════════════════════════════════════════════════════════╝

This will prepare your repository for upload to GitHub.
    """)
    
    # Create directory structure
    create_gitkeep_files()
    
    # Create .gitignore
    create_gitignore()
    
    # Show commands
    show_git_commands()
    
    print("💡 IMPORTANT NOTES:")
    print("   • Your data/clips/ folder will NOT be uploaded (too large)")
    print("   • Demo video should be uploaded separately")
    print("   • Only code and documentation will be in Git")
    print("   • Directory structure is preserved with .gitkeep files")
    
    print("\n🚀 You're ready to upload to GitHub!")
    print("   Follow the commands above step by step.\n")

if __name__ == "__main__":
    main()