# dashboard.py - AGI Assistant Visual Dashboard
"""
Beautiful web-based dashboard with:
- Visual workflow viewer
- One-click automation toggle
- Real-time execution feedback
- Continual learning tracking
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from threading import Thread
import pyautogui

app = Flask(__name__)

# Global state
automation_running = False
execution_logs = []
learning_history = []

class DashboardController:
    def __init__(self):
        self.data_dir = Path("data")
        self.workflows_dir = self.data_dir / "workflows"
        self.json_dir = self.data_dir / "json"
        self.learning_db = self.data_dir / "learning_database.json"
        
        # Initialize learning database
        self.load_learning_data()
    
    def load_learning_data(self):
        """Load continual learning database"""
        if self.learning_db.exists():
            with open(self.learning_db, 'r') as f:
                return json.load(f)
        return {
            'total_sessions': 0,
            'total_automations': 0,
            'workflow_improvements': {},
            'success_rate': {},
            'learning_curve': []
        }
    
    def save_learning_data(self, data):
        """Save learning progress"""
        with open(self.learning_db, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all_workflows(self):
        """Get all available workflows with metadata"""
        workflows = []
        
        if not self.workflows_dir.exists():
            return workflows
        
        for wf_file in sorted(self.workflows_dir.glob("workflow_*.json"), 
                             key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                with open(wf_file, 'r') as f:
                    wf = json.load(f)
                
                # Get corresponding session summary
                session_id = wf.get('workflow_id')
                summary = self.get_session_summary(session_id)
                
                workflows.append({
                    'id': session_id,
                    'filename': wf_file.name,
                    'created_at': wf.get('created_at'),
                    'steps_count': len(wf.get('automation_steps', [])),
                    'automation_potential': summary.get('automation_potential', 0),
                    'workflow_summary': summary.get('workflow_summary', 'No summary'),
                    'detected_actions': summary.get('detected_actions', []),
                    'patterns': summary.get('detected_patterns', []),
                    'execution_count': self.get_execution_count(session_id),
                    'success_rate': self.get_success_rate(session_id),
                    'last_executed': self.get_last_execution(session_id)
                })
            except Exception as e:
                print(f"Error loading workflow {wf_file.name}: {e}")
        
        return workflows
    
    def get_session_summary(self, session_id):
        """Get session summary for a workflow"""
        summary_file = self.json_dir / f"session_summary_{session_id}.json"
        
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                data = json.load(f)
                return data.get('llm_analysis', {})
        
        return {}
    
    def get_execution_count(self, workflow_id):
        """Get how many times workflow was executed"""
        learning_data = self.load_learning_data()
        return learning_data.get('success_rate', {}).get(workflow_id, {}).get('total', 0)
    
    def get_success_rate(self, workflow_id):
        """Get success rate for workflow"""
        learning_data = self.load_learning_data()
        stats = learning_data.get('success_rate', {}).get(workflow_id, {})
        
        total = stats.get('total', 0)
        successful = stats.get('successful', 0)
        
        if total == 0:
            return 0
        return int((successful / total) * 100)
    
    def get_last_execution(self, workflow_id):
        """Get timestamp of last execution"""
        learning_data = self.load_learning_data()
        return learning_data.get('success_rate', {}).get(workflow_id, {}).get('last_run', None)
    
    def get_dashboard_stats(self):
        """Get overall statistics for dashboard"""
        learning_data = self.load_learning_data()
        workflows = self.get_all_workflows()
        
        total_automation_potential = sum(w['automation_potential'] for w in workflows)
        avg_potential = total_automation_potential / len(workflows) if workflows else 0
        
        return {
            'total_workflows': len(workflows),
            'total_sessions': learning_data.get('total_sessions', 0),
            'total_automations': learning_data.get('total_automations', 0),
            'avg_automation_potential': round(avg_potential, 1),
            'learning_curve': learning_data.get('learning_curve', [])
        }
    
    def execute_workflow_with_feedback(self, workflow_id):
        """Execute workflow with real-time feedback"""
        global automation_running, execution_logs
        
        automation_running = True
        execution_logs = []
        
        def log_feedback(message, step_info=None):
            """Add feedback to execution log"""
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'step': step_info
            }
            execution_logs.append(log_entry)
            print(f"💬 {message}")
        
        try:
            # Load workflow
            workflow_file = self.workflows_dir / f"workflow_{workflow_id}.json"
            
            if not workflow_file.exists():
                log_feedback("❌ Workflow file not found")
                return False
            
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
            
            steps = workflow.get('automation_steps', [])
            
            log_feedback(f"🚀 Starting automation for workflow: {workflow_id}")
            log_feedback(f"📋 Total steps to execute: {len(steps)}")
            log_feedback("⏱️  Waiting 3 seconds for you to prepare...")
            time.sleep(3)
            
            successful_steps = 0
            
            # Execute each step
            for i, step in enumerate(steps, 1):
                if not automation_running:
                    log_feedback("⚠️  Automation stopped by user")
                    break
                
                action = step.get('action')
                description = step.get('description', '')
                
                log_feedback(f"📍 Step {i}/{len(steps)}: {action.upper()}", step)
                
                # Real-time reasoning
                reasoning = self.get_reasoning_for_action(step, workflow)
                log_feedback(f"🤔 Reasoning: {reasoning}")
                
                try:
                    # Execute the action
                    if action == 'click':
                        target = step.get('target', '')
                        log_feedback(f"🖱️  Clicking '{target}'...")
                        
                        args = step.get('args', {})
                        if 'x' in args and 'y' in args:
                            pyautogui.click(args['x'], args['y'])
                            log_feedback(f"✅ Clicked at ({args['x']}, {args['y']})")
                        else:
                            log_feedback(f"⚠️  No coordinates available, skipping")
                    
                    elif action == 'type':
                        text = step.get('args', {}).get('text', '')
                        log_feedback(f"⌨️  Typing: '{text}'...")
                        pyautogui.write(text, interval=0.05)
                        log_feedback(f"✅ Typed successfully")
                    
                    elif action == 'wait':
                        seconds = step.get('args', {}).get('seconds', 1)
                        log_feedback(f"⏸️  Waiting {seconds} seconds...")
                        time.sleep(seconds)
                        log_feedback(f"✅ Wait complete")
                    
                    elif action == 'hotkey':
                        keys = step.get('args', {}).get('keys', '')
                        log_feedback(f"⌨️  Pressing hotkey: {keys}...")
                        key_list = keys.lower().replace(' ', '').split('+')
                        pyautogui.hotkey(*key_list)
                        log_feedback(f"✅ Hotkey pressed")
                    
                    else:
                        log_feedback(f"⚠️  Unknown action type: {action}")
                    
                    successful_steps += 1
                    time.sleep(0.5)  # Small delay between steps
                
                except Exception as e:
                    log_feedback(f"❌ Error executing step: {e}")
            
            # Calculate success
            success_rate = (successful_steps / len(steps)) * 100
            
            if success_rate == 100:
                log_feedback(f"🎉 Automation complete! All {len(steps)} steps executed successfully!")
            else:
                log_feedback(f"⚠️  Automation completed with {successful_steps}/{len(steps)} successful steps ({success_rate:.0f}%)")
            
            # Update learning database
            self.update_learning_data(workflow_id, success_rate == 100, successful_steps, len(steps))
            
            automation_running = False
            return True
        
        except Exception as e:
            log_feedback(f"❌ Critical error: {e}")
            automation_running = False
            return False
    
    def get_reasoning_for_action(self, step, workflow):
        """Generate human-readable reasoning for action"""
        action = step.get('action')
        description = step.get('description', '')
        
        reasoning_templates = {
            'click': "I need to click this element to proceed with the workflow",
            'type': "I'm entering this text because it was part of the observed pattern",
            'wait': "I'm pausing to allow the UI to update and respond",
            'hotkey': "I'm using this keyboard shortcut as it was detected in the original workflow"
        }
        
        base_reason = reasoning_templates.get(action, "Executing this step as part of the learned workflow")
        
        # Add context
        if 'save' in description.lower():
            return f"{base_reason}. This appears to be a save operation."
        elif 'open' in description.lower():
            return f"{base_reason}. This will open the application or file."
        elif 'close' in description.lower():
            return f"{base_reason}. This will close the current window."
        
        return base_reason
    
    def update_learning_data(self, workflow_id, success, successful_steps, total_steps):
        """Update continual learning database"""
        learning_data = self.load_learning_data()
        
        # Update totals
        learning_data['total_automations'] = learning_data.get('total_automations', 0) + 1
        
        # Update workflow-specific stats
        if workflow_id not in learning_data['success_rate']:
            learning_data['success_rate'][workflow_id] = {
                'total': 0,
                'successful': 0,
                'last_run': None
            }
        
        stats = learning_data['success_rate'][workflow_id]
        stats['total'] += 1
        if success:
            stats['successful'] += 1
        stats['last_run'] = datetime.now().isoformat()
        
        # Update learning curve
        learning_data['learning_curve'].append({
            'timestamp': datetime.now().isoformat(),
            'workflow_id': workflow_id,
            'success': success,
            'steps_completed': successful_steps,
            'total_steps': total_steps
        })
        
        # Keep only last 100 entries
        learning_data['learning_curve'] = learning_data['learning_curve'][-100:]
        
        self.save_learning_data(learning_data)

# Initialize controller
controller = DashboardController()

# Flask Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/workflows')
def get_workflows():
    """API endpoint to get all workflows"""
    workflows = controller.get_all_workflows()
    return jsonify(workflows)

@app.route('/api/stats')
def get_stats():
    """API endpoint to get dashboard statistics"""
    stats = controller.get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/execute/<workflow_id>', methods=['POST'])
def execute_workflow(workflow_id):
    """API endpoint to execute a workflow"""
    global automation_running
    
    if automation_running:
        return jsonify({'error': 'Automation already running'}), 400
    
    # Run in background thread
    thread = Thread(target=controller.execute_workflow_with_feedback, args=(workflow_id,))
    thread.start()
    
    return jsonify({'status': 'started', 'workflow_id': workflow_id})

@app.route('/api/stop', methods=['POST'])
def stop_execution():
    """API endpoint to stop automation"""
    global automation_running
    automation_running = False
    return jsonify({'status': 'stopped'})

@app.route('/api/logs')
def get_logs():
    """API endpoint to get execution logs (for real-time updates)"""
    global execution_logs
    return jsonify({
        'logs': execution_logs,
        'running': automation_running
    })

@app.route('/api/learning')
def get_learning_data():
    """API endpoint to get learning data"""
    learning_data = controller.load_learning_data()
    return jsonify(learning_data)

def create_html_template():
    """Create the dashboard HTML template"""
    template_dir = Path("templates")
    template_dir.mkdir(exist_ok=True)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AGI Assistant - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        
        .stat-card .value {
            font-size: 2.5em;
            font-weight: bold;
            color: #333;
        }
        
        .workflows-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .workflow-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 5px solid #667eea;
            transition: all 0.3s;
        }
        
        .workflow-card:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateX(5px);
        }
        
        .workflow-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .workflow-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }
        
        .automation-score {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .workflow-meta {
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #666;
        }
        
        .workflow-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .execution-panel {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            display: none;
        }
        
        .execution-panel.active {
            display: block;
        }
        
        .log-container {
            background: #1e1e1e;
            color: #00ff00;
            border-radius: 10px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .log-entry {
            margin-bottom: 10px;
            padding: 5px;
            border-left: 3px solid #00ff00;
            padding-left: 10px;
        }
        
        .log-entry.error {
            border-left-color: #ff0000;
            color: #ff6b6b;
        }
        
        .log-entry.success {
            border-left-color: #00ff00;
            color: #51cf66;
        }
        
        .log-entry.info {
            border-left-color: #339af0;
            color: #74c0fc;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
        }
        
        .badge-success { background: #d4edda; color: #155724; }
        .badge-warning { background: #fff3cd; color: #856404; }
        .badge-info { background: #d1ecf1; color: #0c5460; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .running-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #51cf66;
            border-radius: 50%;
            margin-left: 10px;
            animation: pulse 1.5s infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AGI Assistant Dashboard</h1>
            <p>Watch. Learn. Automate.</p>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be loaded here -->
        </div>
        
        <div class="execution-panel" id="executionPanel">
            <div class="section-title">
                ⚡ Live Automation
                <span id="runningIndicator"></span>
            </div>
            <div class="log-container" id="logContainer">
                <div class="log-entry info">Waiting for automation to start...</div>
            </div>
            <button class="btn btn-danger" onclick="stopAutomation()">⏹️ Stop Automation</button>
        </div>
        
        <div class="workflows-section">
            <div class="section-title">
                📋 Detected Workflows
            </div>
            <div id="workflowsContainer">
                <!-- Workflows will be loaded here -->
            </div>
        </div>
    </div>
    
    <script>
        let autoUpdateInterval = null;
        
        async function loadStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            const statsHtml = `
                <div class="stat-card">
                    <h3>Total Workflows</h3>
                    <div class="value">${stats.total_workflows}</div>
                </div>
                <div class="stat-card">
                    <h3>Recording Sessions</h3>
                    <div class="value">${stats.total_sessions}</div>
                </div>
                <div class="stat-card">
                    <h3>Automations Run</h3>
                    <div class="value">${stats.total_automations}</div>
                </div>
                <div class="stat-card">
                    <h3>Avg Automation Score</h3>
                    <div class="value">${stats.avg_automation_potential}/10</div>
                </div>
            `;
            
            document.getElementById('statsGrid').innerHTML = statsHtml;
        }
        
        async function loadWorkflows() {
            const response = await fetch('/api/workflows');
            const workflows = await response.json();
            
            if (workflows.length === 0) {
                document.getElementById('workflowsContainer').innerHTML = `
                    <p style="text-align: center; color: #666; padding: 40px;">
                        No workflows detected yet. Run <code>python main.py</code> to create one!
                    </p>
                `;
                return;
            }
            
            const workflowsHtml = workflows.map(wf => `
                <div class="workflow-card">
                    <div class="workflow-header">
                        <div class="workflow-title">
                            Workflow: ${wf.id}
                        </div>
                        <div class="automation-score">
                            ${wf.automation_potential}/10
                        </div>
                    </div>
                    <div class="workflow-meta">
                        <span>📅 ${new Date(wf.created_at).toLocaleString()}</span>
                        <span>📊 ${wf.steps_count} steps</span>
                        <span>🔄 ${wf.execution_count} runs</span>
                        <span>✅ ${wf.success_rate}% success</span>
                    </div>
                    <p style="color: #666; margin-bottom: 15px;">
                        ${wf.workflow_summary}
                    </p>
                    <div class="workflow-actions">
                        <button class="btn btn-primary" onclick="executeWorkflow('${wf.id}')">
                            ▶️ Automate This
                        </button>
                        <button class="btn btn-secondary" onclick="viewDetails('${wf.id}')">
                            🔍 View Details
                        </button>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('workflowsContainer').innerHTML = workflowsHtml;
        }
        
        async function executeWorkflow(workflowId) {
            document.getElementById('executionPanel').classList.add('active');
            document.getElementById('logContainer').innerHTML = '<div class="log-entry info">Starting automation...</div>';
            
            await fetch(`/api/execute/${workflowId}`, { method: 'POST' });
            
            // Start polling for logs
            autoUpdateInterval = setInterval(updateLogs, 500);
        }
        
        async function updateLogs() {
            const response = await fetch('/api/logs');
            const data = await response.json();
            
            const logsHtml = data.logs.map(log => {
                let className = 'log-entry';
                if (log.message.includes('❌')) className += ' error';
                else if (log.message.includes('✅')) className += ' success';
                else className += ' info';
                
                return `<div class="${className}">${log.message}</div>`;
            }).join('');
            
            document.getElementById('logContainer').innerHTML = logsHtml;
            document.getElementById('logContainer').scrollTop = document.getElementById('logContainer').scrollHeight;
            
            // Update running indicator
            if (data.running) {
                document.getElementById('runningIndicator').innerHTML = '<span class="running-indicator"></span>';
            } else {
                document.getElementById('runningIndicator').innerHTML = '';
                clearInterval(autoUpdateInterval);
                loadStats();  // Refresh stats after automation
                loadWorkflows();  // Refresh workflows
            }
        }
        
        async function stopAutomation() {
            await fetch('/api/stop', { method: 'POST' });
            clearInterval(autoUpdateInterval);
        }
        
        function viewDetails(workflowId) {
            alert(`Workflow details for: ${workflowId}\n\nCheck data/workflows/workflow_${workflowId}.json for full details.`);
        }
        
        // Initial load
        loadStats();
        loadWorkflows();
        
        // Auto-refresh every 5 seconds
        setInterval(() => {
            loadStats();
            loadWorkflows();
        }, 5000);
    </script>
</body>
</html>"""
    
    with open(template_dir / "dashboard.html", 'w') as f:
        f.write(html_content)

def main():
    """Start the dashboard server"""
    print("\n" + "="*60)
    print("🎨 AGI ASSISTANT - VISUAL DASHBOARD")
    print("="*60)
    print("\n🚀 Starting dashboard server...")
    print("📊 Dashboard URL: http://localhost:5000")
    print("\n💡 Features:")
    print("   • Visual workflow viewer")
    print("   • One-click automation")
    print("   • Real-time execution feedback")
    print("   • Continual learning tracking")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Create HTML template
    create_html_template()
    
    # Start Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()