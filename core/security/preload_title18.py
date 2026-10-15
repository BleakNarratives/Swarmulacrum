"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: preload_title18.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import sqlite3
import os

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"

def init_statute_vault():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the dedicated statutory reference table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS federal_statutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT UNIQUE,
            title_name TEXT,
            elements_text TEXT
        )
    """)
    
    # Core Title 18 elements to lock down the baseline
    core_statutes = [
        (
            "18 USC 241", 
            "Conspiracy Against Rights", 
            "If two or more persons conspire to injure, oppress, threaten, or intimidate any person in any State, Territory, Commonwealth, Possession, or District in the free exercise or enjoyment of any right or privilege secured to him by the Constitution or laws of the United States..."
        ),
        (
            "18 USC 242", 
            "Deprivation of Rights Under Color of Law", 
            "Whoever, under color of any law, statute, ordinance, regulation, or custom, willfully subjects any person in any State, Territory, Commonwealth, Possession, or District to the deprivation of any rights, privileges, or immunities secured or protected by the Constitution or laws of the United States..."
        ),
        (
            "18 USC 1001", 
            "Statements or Entries Generally (Fraud/False Statements)", 
            "Except as otherwise provided in this section, whoever, in any matter within the jurisdiction of the executive, legislative, or judicial branch of the Government of the United States, knowingly and willfully—(1) falsifies, conceals, or covers up by any trick, scheme, or device a material fact; (2) makes any materially false, fictitious, or fraudulent statement or representation..."
        ),
        (
            "18 USC 1512", 
            "Tampering with a Witness, Victim, or an Informant (Obstruction)", 
            "Whoever alters, destroys, mutilates, or conceals a record, document, or other object, or attempts to do so, with the intent to impair the object’s integrity or availability for use in an official proceeding..."
        )
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO federal_statutes (section, title_name, elements_text)
        VALUES (?, ?, ?)
    """, core_statutes)
    
    conn.commit()
    print(f"[+] Loaded {len(core_statutes)} bedrock Title 18 USC statutes into local vault.")
    conn.close()

if __name__ == "__main__":
    init_statute_vault()
