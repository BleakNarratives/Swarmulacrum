"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: arena_runner.py
LAST_SYNC: 2026-08-02T01:13:31Z
[/DNA_TAG]
"""
import sqlite3
import os
import hashlib
import json
from datetime import datetime

DB_PATH = '/storage/emulated/0/RootBase/OutClaw/arena/data/arena_log.db'

def get_connection():
    # Enable WAL mode for concurrent multi-agent read/write safety
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def hash_file(file_path):
    sha256_hash = hashlib.sha256()
    if not os.path.exists(file_path):
        return "FILE_MISSING"
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def register_run(round_num, device, agent, task_id, input_summary, output_path):
    out_hash = hash_file(output_path)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO arena_runs (round, device, agent, task_id, input_summary, output_path, output_hash, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'completed')
        ''', (round_num, device, agent, task_id, input_summary, output_path, out_hash))
        conn.commit()
        print(f"[Foresight Logger] Task {task_id} registered successfully. Hash: {out_hash[:8]}...")
    except Exception as e:
        conn.rollback()
        print(f"[Foresight Error] Failed to log task {task_id}: {e}")
    finally:
      conn.close()

if __name__ == "__main__":
    print("Arena Runner Engine armed with WAL concurrency and SHA-256 verification.")
