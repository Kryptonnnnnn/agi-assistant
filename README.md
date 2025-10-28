# 🤖 AGI Assistant - Desktop AI That Learns From You

> **Watch. Learn. Automate. Improve.** A local-first AI assistant that observes your desktop, understands your workflows, and automates repetitive tasks.

**🌟 NOW WITH VISUAL DASHBOARD & ALL BONUS FEATURES! 🌟**

---

## 🎯 What Is This?

This is a **complete AGI Assistant** that includes:

### ✅ Round 1 Requirements
- 📹 Screen & audio capture (local)
- 🔍 OCR text extraction
- 🎤 Speech-to-text transcription
- 🧠 LLM analysis
- 📊 Pattern recognition
- 💡 Automation suggestions
- 📄 Structured JSON output

### 🌟 BONUS FEATURES (All Implemented!)
- 🎨 **Visual Dashboard** - Beautiful web interface
- 🎯 **One-Click Automation** - Toggle to execute workflows
- 💬 **Real-Time Feedback** - See reasoning as it happens
- 📈 **Continual Learning** - System improves over time

**Everything runs 100% locally. No cloud. No uploads. Privacy-first.**

---

## 🚀 Quick Start (NEW: Integrated Demo)

### One Command to See Everything

```bash
python run_full_demo.py
```

This will:
1. ✅ Record a workflow (30s)
2. ✅ Analyze with AI
3. ✅ Show results
4. ✅ Launch visual dashboard
5. ✅ Let you automate with one click!

### Or Run Components Separately

```bash
# 1. Record a workflow
python main.py

# 2. Launch visual dashboard
python dashboard.py

# 3. Click "Automate This" in browser!
```

---

## 🎨 Visual Dashboard Features

### Beautiful Web Interface

Open `http://localhost:5000` to see:

1. **Statistics Dashboard**
   - Total workflows detected
   - Recording sessions count
   - Automations executed
   - Average automation score

2. **Workflow Cards**
   - Visual representation of each workflow
   - Automation potential score (0-10)
   - Execution history
   - Success rate tracking

3. **One-Click Automation**
   - Click "▶️ Automate This" button
   - Watch it execute in real-time
   - No configuration needed!

4. **Real-Time Feedback Panel**
   - Live execution logs
   - Reasoning for each action
   - Color-coded status
   - Running indicator

5. **Continual Learning Tracking**
   - Execution count per workflow
   - Success rate percentage
   - Learning curve visualization
   - Improvement over time

### Screenshot

```
┌─────────────────────────────────────────────────────────┐
│  🤖 AGI Assistant Dashboard                            │
│  Watch. Learn. Automate.                               │
├─────────────────────────────────────────────────────────┤
│  [12 Workflows] [25 Sessions] [8 Automations] [8.5/10]│
├─────────────────────────────────────────────────────────┤
│  ⚡ Workflow: 20251027_131013        Score: 9/10       │
│  📅 Oct 27, 2025  📊 5 steps  🔄 3 runs  ✅ 100%      │
│  Summary: User opened Excel, entered data, saved file  │
│  [▶️ Automate This] [🔍 View Details]                  │
├─────────────────────────────────────────────────────────┤
│  💬 Real-Time Execution Feedback                        │
│  🚀 Starting automation...                             │
│  🤔 Reasoning: I need to click Save to complete task  │
│  ✅ Step 1/5 complete                                  │
└─────────────────────────────────────────────────────────┘
```


## 📦 Installation

### Step 1: Clone Repository

```bash
git clone <https://github.com/Kryptonnnnnn/agi-assistant-hackathon>
cd the_agi_assistant
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Install External Tools

**Tesseract OCR:**
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

**Ollama (Optional):**
- Download: https://ollama.ai
- Pull model: `ollama pull llama3.2:1b`

### Step 4: Verify Installation

```bash
python setup.py
```

---

## 🎯 Usage

### Option 1: Full Integrated Demo (Recommended)

```bash
python run_full_demo.py
```

This runs the complete flow and showcases all features!

### Option 2: Step-by-Step

```bash
# 1. Record workflow
python main.py

# 2. Launch dashboard
python dashboard.py

# 3. Use dashboard in browser
# Open: http://localhost:5000
# Click "Automate This" on any workflow
```

### Option 3: Interactive Menu

```bash
python demo.py
```

Choose from:
1. Full demo
2. Quick test
3. View workflows
4. Preview automation
5. Storage stats
6. And more!

---

## 🌟 What Makes This Special

### 1. Visual Dashboard (Bonus ✅)

- Modern, responsive web UI
- Beautiful purple gradient design
- Real-time updates
- Professional presentation

### 2. One-Click Automation (Bonus ✅)

- Click button → automation starts
- No configuration needed
- No command line required
- Perfect for demos

### 3. Real-Time Feedback (Bonus ✅)

- Live execution logs
- Reasoning for each action ("I'm clicking Save because...")
- Color-coded status
- Transparent AI decision-making

### 4. Continual Learning (Bonus ✅)

- Tracks every execution
- Calculates success rates
- Improves over time
- Learning curve visualization

### 5. Complete Local Processing

- No cloud API calls
- No data uploads
- Full privacy
- Works offline

---

## 📊 Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER PERFORMS TASK                    │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  CAPTURE LAYER (modules/capture/)                        │
│  • screen_recorder.py → Screenshots every 3s            │
│  • audio_recorder.py → Continuous audio recording       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  PROCESSING LAYER (modules/processing/)                  │
│  • ocr_processor.py → Extract text + UI elements        │
│  • stt_processor.py → Transcribe audio (Whisper)        │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  UNDERSTANDING LAYER (modules/llm/)                      │
│  • local_llm.py → Analyze workflow with LLM             │
│  • Detect patterns, generate automation steps           │
│  • Score automation potential (0-10)                    │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  STORAGE LAYER (modules/storage/)                        │
│  • data_manager.py → Save summaries & workflows         │
│  • Auto-cleanup old data                                │
│  • Optimize storage                                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  VISUALIZATION LAYER (dashboard.py)                      │
│  • Beautiful web dashboard                              │
│  • Real-time execution viewer                           │
│  • Continual learning tracker                           │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  AUTOMATION LAYER (run_automation.py)                    │
│  • Execute workflows with PyAutoGUI                     │
│  • Real-time feedback with reasoning                    │
│  • Update learning database                             │
└─────────────────────────────────────────────────────────┘
```

---

### What to Emphasize

1. **The dashboard** - Visual appeal
2. **One-click automation** - Ease of use
3. **Real-time feedback** - Transparency
4. **Learning feature** - Intelligence
5. **9/10 automation score** - Success

---

## 📂 Project Structure

```
the_agi_assistant/
├── 🎮 Main Applications
│   ├── main.py                    # Core recording system
│   ├── dashboard.py               # 🌟 Visual dashboard
│   ├── launch_dashboard.py        # 🌟 Quick launcher
│   ├── run_full_demo.py           # 🌟 Integrated demo
│   ├── demo.py                    # Interactive menu
│   ├── run_automation.py          # Automation runner
│   └── setup.py                   # Setup wizard
│
├── 📦 Configuration
│   ├── requirements.txt           # Python dependencies
│   └── .gitignore                # Git exclusions
│
├── 📚 Documentation
│   ├── README.md                  # This file
│   ├── QUICKSTART.md             # 5-minute guide
│   ├── DASHBOARD_GUIDE.md        # 🌟 Dashboard docs
│   ├── ROUND2_GUIDE.md           # Round 2 roadmap
│   ├── SUBMISSION_CHECKLIST.md   # Submission guide
│   └── PROJECT_SUMMARY.md        # Complete overview
│
├── 🧩 Modules
│   ├── capture/
│   │   ├── screen_recorder.py    # Screenshot capture
│   │   └── audio_recorder.py     # Audio recording
│   ├── processing/
│   │   ├── ocr_processor.py      # OCR extraction
│   │   └── stt_processor.py      # Speech-to-text
│   ├── llm/
│   │   └── local_llm.py          # LLM analysis
│   ├── storage/
│   │   └── data_manager.py       # Data management
│   └── automation/
│       └── workflow_parser.py    # Workflow parsing
│
├── 🎨 Web Interface
│   └── templates/
│       └── dashboard.html        # 🌟 Dashboard UI
│
└── 💾 Data (Generated at runtime)
    ├── clips/                    # Screenshots & audio
    ├── json/                     # Session summaries
    ├── workflows/                # Automation workflows
    └── learning_database.json    # 🌟 Learning data
```

---

## 🎯 Key Files Explained

### For Judges to Review

1. **main.py** - Complete observation pipeline
2. **dashboard.py** - Visual dashboard (bonus feature!)
3. **modules/llm/local_llm.py** - AI analysis engine
4. **run_full_demo.py** - Quick demonstration


---

## 🚀 Getting Started - Quick Commands

```bash
# First time setup
python setup.py

# Full integrated demo (RECOMMENDED FOR VIDEO)
python run_full_demo.py

# Just record a workflow
python main.py

# Just launch dashboard
python launch_dashboard.py

# Interactive menu
python demo.py
```

---

## 🎓 Key Technologies

- **Screen Capture**: MSS, PyAutoGUI
- **Audio**: sounddevice, soundfile
- **OCR**: Tesseract, OpenCV
- **Speech-to-Text**: OpenAI Whisper (local)
- **LLM**: Ollama (llama3.2)
- **Automation**: PyAutoGUI
- **Dashboard**: Flask, HTML5, CSS3
- **Language**: Python 3.9+

---

## 💡 Usage Examples

### Example 1: Excel Automation

**Record:**
```bash
python main.py
# During recording:
# 1. Open Excel
# 2. Enter data in cells
# 3. Save file
# 4. Close Excel
```

**Automate:**
```bash
python launch_dashboard.py
# Click "Automate This" in browser
# Watch it execute!
```

### Example 2: File Management

**Record:**
```bash
python main.py
# During recording:
# 1. Open File Explorer
# 2. Create new folder
# 3. Rename files
# 4. Move files to folder
```

**Automate:**
- Dashboard → Click "Automate This"
- Watch real-time feedback
- See it learn and improve

### Example 3: Browser Tasks

**Record:**
```bash
python main.py
# During recording:
# 1. Open browser
# 2. Navigate to website
# 3. Fill form
# 4. Submit
```

**Automate:**
- One-click execution
- Real-time reasoning
- Learning tracking

---

## 🐛 Troubleshooting

### Dashboard Won't Start

**Error**: "Address already in use"

**Solution**:
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Workflows Not Showing

**Solution**:
1. Run `python main.py` first
2. Refresh dashboard (F5)
3. Check `data/workflows/` exists

### Automation Clicks Wrong Place

**Solution**:
1. Keep same screen resolution
2. Position windows consistently
3. Use simple, clear workflows for demo

### Audio Transcription Shows [BLANK_AUDIO]

**Solution**:
1. Speak clearly during recording
2. Check microphone permissions
3. Test with: `python -m sounddevice`

---

## 📊 Performance Metrics

### Typical Performance

- **Screenshot capture**: ~200ms per image
- **OCR processing**: ~1-2s per screenshot
- **Audio transcription**: ~5-10s for 30s audio
- **LLM analysis**: ~3-5s (Ollama) or instant (fallback)
- **Total processing**: ~30-60s for 30s session
- **Dashboard load**: <1s
- **Automation execution**: Real-time (as recorded)

### Storage Usage

- **Per session**: ~5-10 MB
- **Per workflow**: ~100-500 KB JSON
- **Dashboard**: Negligible (~100 KB)
- **Learning database**: ~50-200 KB

---


## 🎯 What Is This?

This is a **Round 1 MVP** for the AGI Assistant Hackathon - an AI dashcam for your desktop that:

1. 📹 **Captures** your screen and audio locally
2. 🧠 **Understands** what you're doing using OCR + Speech-to-Text + Local LLM
3. 🔍 **Detects** repetitive workflows and patterns
4. 💡 **Suggests** automation opportunities
5. 📊 **Generates** structured JSON outputs for Round 2 automation

**Everything runs 100% locally. No cloud. No uploads. Privacy-first.**

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **Tesseract OCR** installed
3. **Ollama** (optional, for better LLM analysis)


**Let's build the future of desktop automation! 🚀**
