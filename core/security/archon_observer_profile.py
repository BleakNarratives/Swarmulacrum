#!/usr/bin/env python3
"""
ARCHON OBSERVER - Telemetry & Execution Pattern Extractor
Parses local git history and execution logs to build an objective, 
indifferent behavioral profile of system interactions.
"""

import os
import json
import subprocess
from datetime import datetime, timezone

def parse_git_telemetry(repo_path):
    try:
        cmd = ["git", "-C", repo_path, "log", "-n", "30", "--pretty=format:%h|%an|%ad|%s"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logs = []
        for line in res.stdout.strip().splitlines():
            if line:
                parts = line.split("|")
                logs.append({"hash": parts[0], "author": parts[1], "date": parts[2], "msg": parts[3]})
        return logs
    except Exception as e:
        return [{"error": f"Failed to parse git log: {str(e)}"}]

def build_archon_spec(repo_path):
    git_history = parse_git_telemetry(repo_path)
    
    spec = {
        "observer_node": "ARCHON_LOG_01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "system_fingerprint": {
            "execution_environment": "Termux / Crostini Linux (XDG Compliant)",
            "primary_patterns": [
                "Zero-dependency fallbacks",
                "Explicit AST/docstring metadata parsing",
                "Single canonical file paths with Git-based versioning",
                "Strict aversion to destructive full-file AI overwrites"
            ],
            "security_posture": "Deterministic verification gates, circuit-breaker patterns, sub-process isolation"
        },
        "recent_telemetry_events": git_history
    }
    
    out_path = os.path.join(repo_path, "archon_mikey_spec.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    return out_path

if __name__ == "__main__":
    target_repo = os.path.expanduser("~/Swarmulacrum")
    out = build_archon_spec(target_repo)
    print(f"[Archon Observer] Cold telemetry profile written to: {out}")
