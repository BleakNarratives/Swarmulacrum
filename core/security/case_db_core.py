"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: case_db_core.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import sqlite3
import os
import sys
import re

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"

class CaseDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        # Table 1: Document Metadata
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_name TEXT UNIQUE,
                file_path TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table 2: Raw Verified Lines (The Immutable Baseline)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS text_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id INTEGER,
                line_number INTEGER,
                raw_text TEXT,
                FOREIGN KEY(doc_id) REFERENCES documents(id)
            )
        """)
        self.conn.commit()

    def ingest_document(self, file_path, doc_name):
        if not os.path.exists(file_path):
            print(f"[-] Document missing at path: {file_path}")
            return False
            
        try:
            self.cursor.execute("INSERT OR IGNORE INTO documents (doc_name, file_path) VALUES (?, ?)", (doc_name, file_path))
            self.conn.commit()
            
            self.cursor.execute("SELECT id FROM documents WHERE doc_name = ?", (doc_name,))
            doc_id = self.cursor.fetchone()[0]
            
            # Wipe existing line records for this doc to prevent duplicate scaling
            self.cursor.execute("DELETE FROM text_records WHERE doc_id = ?", (doc_id,))
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            insert_buffer = []
            for idx, line in enumerate(lines):
                insert_buffer.append((doc_id, idx + 1, line.strip()))
                
            self.cursor.executemany("INSERT INTO text_records (doc_id, line_number, raw_text) VALUES (?, ?, ?)", insert_buffer)
            self.conn.commit()
            print(f"[+] Ingested {len(lines)} un-alterable records into database for: {doc_name}")
            return True
        except Exception as e:
            print(f"[-] Database ingestion failure: {e}")
            return False

    def query_exact_text(self, keyword):
        """Returns direct, un-editable source data matches to pin down AI drift."""
        self.cursor.execute("""
            SELECT d.doc_name, r.line_number, r.raw_text 
            FROM text_records r 
            JOIN documents d ON r.doc_id = d.id 
            WHERE r.raw_text LIKE ?
        """, (f"%{keyword}%",))
        return self.cursor.fetchall()

if __name__ == "__main__":
    db = CaseDatabase()
    print(f"[*] Local Case Matrix Database active at: {DB_PATH}")
