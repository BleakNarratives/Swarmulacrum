"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: init_arena.py
LAST_SYNC: 2026-08-02T01:13:31Z
[/DNA_TAG]
"""
import sqlite3
import os

db_path = '/storage/emulated/0/RootBase/OutClaw/arena/data/arena_log.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS arena_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  round INTEGER,
  device TEXT,
  agent TEXT,
  task_id TEXT,
  input_summary TEXT,
  output_path TEXT,
  output_hash TEXT,
  gaps_found TEXT,
  status TEXT DEFAULT 'pending',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_task ON arena_runs(task_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_round ON arena_runs(round);')

conn.commit()
conn.close()
print(f"Arena database initialized successfully at: {db_path}")
