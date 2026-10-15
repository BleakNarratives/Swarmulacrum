"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: event_bus.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
OUTCLAW EVENT BUS - Inter-Process Communication System

This module provides a lightweight event bus for coordinating between
multiple AI agents (Mistral Vibe, Gemini CLI, etc.) working on the same project.

Prevents file conflicts, duplicates work, and enables parallel processing.
"""

import json
import os
import time
import threading
import hashlib
from datetime import datetime
from pathlib import Path

# Central coordination directory
BUS_DIR = "/storage/emulated/0/RootBase/OutClaw/.event_bus"
Path(BUS_DIR).mkdir(exist_ok=True)


class EventBus:
    """
    Distributed event bus for multi-agent coordination.
    Uses file-based messaging for cross-process communication.
    """
    
    def __init__(self, agent_name="unknown"):
        self.agent_name = agent_name
        self.lock_file = os.path.join(BUS_DIR, "bus.lock")
        self.event_log = os.path.join(BUS_DIR, "event_log.json")
        self.task_registry = os.path.join(BUS_DIR, "task_registry.json")
        self.agent_status = os.path.join(BUS_DIR, "agent_status.json")
        
        # Initialize if not exists
        self._initialize()
    
    def _initialize(self):
        """Initialize bus files if they don't exist."""
        if not os.path.exists(self.event_log):
            with open(self.event_log, 'w') as f:
                json.dump([], f)
        if not os.path.exists(self.task_registry):
            with open(self.task_registry, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.agent_status):
            with open(self.agent_status, 'w') as f:
                json.dump({}, f)
    
    def _acquire_lock(self, timeout=10):
        """Acquire file lock for thread-safe operations."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                fd = os.open(self.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return True
            except FileExistsError:
                time.sleep(0.1)
        return False
    
    def _release_lock(self):
        """Release file lock."""
        if os.path.exists(self.lock_file):
            os.unlink(self.lock_file)
    
    def _read_json(self, filepath):
        """Read JSON file with lock."""
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def _write_json(self, filepath, data):
        """Write JSON file with lock."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_agent(self, capabilities=None):
        """Register this agent's capabilities."""
        status = self._read_json(self.agent_status)
        status[self.agent_name] = {
            "last_seen": datetime.now().isoformat(),
            "capabilities": capabilities or [],
            "status": "active"
        }
        self._write_json(self.agent_status, status)
    
    def emit_event(self, event_type, data, priority="normal"):
        """Emit an event to the bus."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_name,
            "type": event_type,
            "data": data,
            "priority": priority
        }
        
        log = self._read_json(self.event_log)
        if isinstance(log, list):
            log.append(event)
        else:
            log = [event]
        
        self._write_json(self.event_log, log)
        return event
    
    def subscribe(self, event_type, callback):
        """Subscribe to events (polling-based)."""
        def poller():
            last_index = 0
            while True:
                log = self._read_json(self.event_log)
                if isinstance(log, list):
                    for i, event in enumerate(log[last_index:], last_index):
                        if event.get('type') == event_type:
                            callback(event)
                    last_index = len(log)
                time.sleep(1)
        
        thread = threading.Thread(target=poller, daemon=True)
        thread.start()
        return thread
    
    def get_unread_events(self, agent_name=None, event_type=None):
        """Get unread events for this agent."""
        log = self._read_json(self.event_log)
        events = []
        
        for event in (log or []):
            if agent_name and event.get('agent') == agent_name:
                continue  # Skip our own events
            if event_type and event.get('type') != event_type:
                continue
            events.append(event)
        
        return events
    
    def claim_task(self, task_name, description, agent=None):
        """
        Claim a task for processing.
        Returns True if task was claimed, False if already claimed by another agent.
        """
        registry = self._read_json(self.task_registry)
        
        if task_name in registry:
            # Task already exists
            existing = registry[task_name]
            if existing.get('status') == 'completed':
                return False, "Task already completed"
            if existing.get('assigned_to') != self.agent_name:
                return False, f"Task assigned to {existing.get('assigned_to')}"
            return True, "Task already claimed by you"
        
        # Claim the task
        registry[task_name] = {
            "description": description,
            "assigned_to": agent or self.agent_name,
            "claimed_at": datetime.now().isoformat(),
            "status": "in_progress",
            "progress": 0
        }
        self._write_json(self.task_registry, registry)
        return True, "Task claimed"
    
    def update_task_progress(self, task_name, progress, status=None, result=None):
        """Update task progress."""
        registry = self._read_json(self.task_registry)
        
        if task_name not in registry:
            return False, "Task not found"
        
        task = registry[task_name]
        task['progress'] = progress
        if status:
            task['status'] = status
        if result:
            task['result'] = result
        task['last_updated'] = datetime.now().isoformat()
        
        self._write_json(self.task_registry, registry)
        return True, "Task updated"
    
    def complete_task(self, task_name, result):
        """Mark task as completed."""
        success, msg = self.update_task_progress(
            task_name, 
            progress=100, 
            status="completed",
            result=result
        )
        if success:
            # Emit completion event
            self.emit_event("task_completed", {
                "task": task_name,
                "result": result,
                "agent": self.agent_name
            })
        return success, msg
    
    def get_task_status(self, task_name):
        """Get status of a task."""
        registry = self._read_json(self.task_registry)
        return registry.get(task_name, None)
    
    def list_pending_tasks(self):
        """List all pending tasks."""
        registry = self._read_json(self.task_registry)
        return {
            k: v for k, v in registry.items() 
            if v.get('status') != 'completed'
        }
    
    def get_agent_capabilities(self, agent_name):
        """Get capabilities of a specific agent."""
        status = self._read_json(self.agent_status)
        return status.get(agent_name, {}).get('capabilities', [])
    
    def list_active_agents(self):
        """List all active agents."""
        status = self._read_json(self.agent_status)
        # Filter out agents not seen in last 5 minutes
        cutoff = datetime.now().timestamp() - 300
        active = {}
        for name, info in status.items():
            last_seen = datetime.fromisoformat(info.get('last_seen', '1970-01-01')).timestamp()
            if last_seen > cutoff:
                active[name] = info
        return active
    
    def file_lock(self, filepath, operation, timeout=30):
        """
        Acquire lock for a specific file operation.
        Prevents concurrent modification conflicts.
        
        Usage:
            with bus.file_lock('/path/to/file.txt', 'write'):
                # Safe to modify file
        """
        lock_path = os.path.join(BUS_DIR, "file_locks", hashlib.md5(filepath.encode()).hexdigest() + ".lock")
        Path(lock_path).parent.mkdir(exist_ok=True)
        
        class FileLockContext:
            def __enter__(self):
                start = time.time()
                while time.time() - start < timeout:
                    try:
                        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                        os.close(fd)
                        return self
                    except FileExistsError:
                        time.sleep(0.5)
                raise TimeoutError(f"Could not acquire lock for {filepath}")
            
            def __exit__(self, *args):
                if os.path.exists(lock_path):
                    os.unlink(lock_path)
        
        return FileLockContext()


# Global event bus instance
_bus_instance = None


def get_bus(agent_name="mistral_vibe"):
    """Get or create the global event bus instance."""
    global _bus_instance
    if _bus_instance is None:
        _bus_instance = EventBus(agent_name)
        _bus_instance.register_agent()
    return _bus_instance


# Convenience functions for direct use
def emit(event_type, data, priority="normal", agent="mistral_vibe"):
    """Quick emit function."""
    bus = get_bus(agent)
    return bus.emit_event(event_type, data, priority)


def claim(task_name, description):
    """Quick task claim function."""
    bus = get_bus()
    return bus.claim_task(task_name, description)


def complete(task_name, result):
    """Quick task complete function."""
    bus = get_bus()
    return bus.complete_task(task_name, result)


def status(task_name):
    """Quick task status check."""
    bus = get_bus()
    return bus.get_task_status(task_name)


def pending_tasks():
    """Get pending tasks."""
    bus = get_bus()
    return bus.list_pending_tasks()


def other_agents():
    """List other active agents."""
    bus = get_bus()
    agents = bus.list_active_agents()
    return {k: v for k, v in agents.items() if k != bus.agent_name}


if __name__ == "__main__":
    # Test the event bus
    bus = get_bus("test_agent")
    
    # Register capabilities
    bus.register_agent(capabilities=["document_analysis", "template_generation", "legal_research"])
    
    # Claim a task
    success, msg = bus.claim_task("test_task", "Testing the event bus system")
    print(f"Task claim: {success} - {msg}")
    
    # Update progress
    bus.update_task_progress("test_task", progress=50)
    
    # Complete task
    bus.complete_task("test_task", result={"status": "success", "data": "test complete"})
    
    # List pending
    print(f"\nPending tasks: {bus.list_pending_tasks()}")
    
    # Get task status
    print(f"\nTask status: {bus.get_task_status('test_task')}")
    
    # Emit event
    bus.emit_event("system_test", {"message": "Event bus operational"})
    
    print("\n[+] Event Bus System Operational")
