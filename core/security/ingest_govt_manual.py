"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: ingest_govt_manual.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import sqlite3
import sys
import os

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"

def upload_manual_standard(agency, section, procedure_text, consequence):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO govt_manuals_vault (agency_or_source, manual_section, mandatory_procedure, breach_consequence)
        VALUES (?, ?, ?, ?)
    """, (agency, section, procedure_text, consequence))
    
    conn.commit()
    print(f"[+] Operational Guideline Added to Vault: {agency} - Section {section}")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("[-] Usage: python ingest_govt_manual.py <Agency> <Section> <Procedure_Text> <Consequence>")
        print("[-] Example: python ingest_govt_manual.py 'DOJ Manual' '9-5.000' 'Must disclose Brady material' 'Breaches Due Process'")
    else:
        upload_manual_standard(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
