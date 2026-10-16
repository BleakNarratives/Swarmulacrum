#!/usr/bin/env python3
"""
Jules REST API Bridge for Swarmulacrum
Reads API key directly from Concierge Vault JSON.
"""

import os
import sys
import json
import urllib.request

def load_vault_key(key_name="JULES_API_KEY"):
    vault_paths = [
        os.path.expanduser("~/.concierge/vault.json"),
        os.path.expanduser("~/vault.json"),
        os.path.expanduser("~/.valet/vault.json")
    ]
    for path in vault_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if key_name in data:
                        return data[key_name]
            except Exception:
                pass
    return os.getenv(key_name, "")

JULES_API_KEY = load_vault_key("JULES_API_KEY")
BASE_URL = "https://jules.googleapis.com/v1alpha"

def make_request(endpoint, method="GET", payload=None):
    if not JULES_API_KEY:
        print("[ERROR] JULES_API_KEY not found in Concierge vault.json or environment.")
        sys.exit(1)
        
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "X-Goog-Api-Key": JULES_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[API Error] {e}")
        return None

def list_sessions():
    res = make_request("sessions")
    if res and "sessions" in res:
        for s in res["sessions"]:
            print(f"Session: {s.get('name')} | State: {s.get('state')} | Title: {s.get('title', 'N/A')}")
    else:
        print("[Jules Bridge] No active sessions found or key invalid.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_sessions()
    else:
        print("Usage: python3 jules_bridge.py list (Reads directly from Concierge vault)")
