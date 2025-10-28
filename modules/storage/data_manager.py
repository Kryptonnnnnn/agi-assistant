# modules/storage/data_manager.py
"""
Data Manager - Handles storage optimization and cleanup
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
import json

def get_file_size(file_path: Path) -> int:
    """Get file size in bytes"""
    try:
        return file_path.stat().st_size
    except:
        return 0

def get_directory_size(directory: Path) -> int:
    """Get total size of directory in bytes"""
    total_size = 0
    try:
        for item in directory.rglob('*'):
            if item.is_file():
                total_size += get_file_size(item)
    except Exception as e:
        print(f"Error calculating directory size: {e}")
    return total_size

def get_storage_info(data_dir: Path) -> Dict:
    """
    Get storage information for data directory
    
    Args:
        data_dir: Path to data directory
    
    Returns:
        Dictionary with storage statistics
    """
    clips_dir = data_dir / "clips"
    json_dir = data_dir / "json"
    workflows_dir = data_dir / "workflows"
    
    info = {
        'clips_size_mb': get_directory_size(clips_dir) / (1024 * 1024),
        'json_size_mb': get_directory_size(json_dir) / (1024 * 1024),
        'workflows_size_mb': get_directory_size(workflows_dir) / (1024 * 1024),
        'total_size_mb': 0,
        'file_count': 0,
        'clips_count': 0,
        'json_count': 0,
        'workflows_count': 0
    }
    
    # Count files
    try:
        info['clips_count'] = len(list(clips_dir.glob('*')))
        info['json_count'] = len(list(json_dir.glob('*.json')))
        info['workflows_count'] = len(list(workflows_dir.glob('*.json')))
        info['file_count'] = info['clips_count'] + info['json_count'] + info['workflows_count']
    except:
        pass
    
    info['total_size_mb'] = info['clips_size_mb'] + info['json_size_mb'] + info['workflows_size_mb']
    
    return info

def cleanup_old_data(data_dir: Path, days_to_keep: int = 7) -> Dict:
    """
    Clean up old data files
    
    Args:
        data_dir: Path to data directory
        days_to_keep: Keep files from last N days
    
    Returns:
        Cleanup statistics
    """
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    stats = {
        'files_deleted': 0,
        'space_freed_mb': 0,
        'errors': []
    }
    
    # Clean clips directory
    clips_dir = data_dir / "clips"
    if clips_dir.exists():
        for file_path in clips_dir.glob('*'):
            try:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    size_mb = get_file_size(file_path) / (1024 * 1024)
                    file_path.unlink()
                    stats['files_deleted'] += 1
                    stats['space_freed_mb'] += size_mb
            except Exception as e:
                stats['errors'].append(f"Error deleting {file_path.name}: {e}")
    
    # Clean old JSON summaries (but keep recent ones)
    json_dir = data_dir / "json"
    if json_dir.exists():
        for file_path in json_dir.glob('session_summary_*.json'):
            try:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    size_mb = get_file_size(file_path) / (1024 * 1024)
                    file_path.unlink()
                    stats['files_deleted'] += 1
                    stats['space_freed_mb'] += size_mb
            except Exception as e:
                stats['errors'].append(f"Error deleting {file_path.name}: {e}")
    
    # Never delete workflows automatically
    
    print(f"   Deleted {stats['files_deleted']} files, freed {stats['space_freed_mb']:.2f} MB")
    if stats['errors']:
        print(f"   ⚠️  {len(stats['errors'])} errors occurred")
    
    return stats

def optimize_json_storage(json_file: Path, max_size_kb: int = 500) -> bool:
    """
    Optimize JSON file by removing unnecessary data
    
    Args:
        json_file: Path to JSON file
        max_size_kb: Maximum file size in KB
    
    Returns:
        True if optimization was performed
    """
    try:
        if get_file_size(json_file) / 1024 < max_size_kb:
            return False
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Remove verbose data
        if 'session_data' in data:
            session = data['session_data']
            
            # Limit OCR results
            if 'ocr_results' in session:
                for ocr in session['ocr_results']:
                    if 'words_with_positions' in ocr:
                        ocr['words_with_positions'] = ocr['words_with_positions'][:20]
            
            # Limit audio segments
            if 'audio_transcription' in session:
                if 'segments' in session['audio_transcription']:
                    session['audio_transcription']['segments'] = \
                        session['audio_transcription']['segments'][:10]
        
        # Save optimized version
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error optimizing {json_file.name}: {e}")
        return False

def get_workflow_summary(workflows_dir: Path) -> List[Dict]:
    """
    Get summary of all saved workflows
    
    Args:
        workflows_dir: Path to workflows directory
    
    Returns:
        List of workflow summaries
    """
    workflows = []
    
    if not workflows_dir.exists():
        return workflows
    
    for workflow_file in workflows_dir.glob('workflow_*.json'):
        try:
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
                workflows.append({
                    'id': workflow.get('workflow_id'),
                    'created_at': workflow.get('created_at'),
                    'steps_count': len(workflow.get('automation_steps', [])),
                    'file': workflow_file.name
                })
        except Exception as e:
            print(f"Error reading {workflow_file.name}: {e}")
    
    return workflows

def archive_old_workflows(workflows_dir: Path, archive_dir: Path = None) -> int:
    """
    Archive workflows older than 30 days
    
    Args:
        workflows_dir: Path to workflows directory
        archive_dir: Path to archive directory (created if None)
    
    Returns:
        Number of workflows archived
    """
    if archive_dir is None:
        archive_dir = workflows_dir.parent / "archive"
    
    archive_dir.mkdir(exist_ok=True)
    
    cutoff_date = datetime.now() - timedelta(days=30)
    archived_count = 0
    
    for workflow_file in workflows_dir.glob('workflow_*.json'):
        try:
            file_time = datetime.fromtimestamp(workflow_file.stat().st_mtime)
            if file_time < cutoff_date:
                shutil.move(str(workflow_file), str(archive_dir / workflow_file.name))
                archived_count += 1
        except Exception as e:
            print(f"Error archiving {workflow_file.name}: {e}")
    
    return archived_count