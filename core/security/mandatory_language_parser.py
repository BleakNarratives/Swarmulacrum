"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: mandatory_language_parser.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import re
import sqlite3

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"

def audit_mandatory_directives(doc_id_to_scan):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Grab all lines for the document
    cursor.execute("""
        SELECT line_number, raw_text 
        FROM text_records 
        WHERE doc_id = ?
    """, (doc_id_to_scan,))
    rows = cursor.fetchall()
    
    print(f"\n{'='*70}")
    print("        MANDATORY LANGUAGE & MINISTERIAL DIRECTIVE AUDIT")
    print(f"{'='*70}")
    
    triggered_violations = 0
    for line_num, text in rows:
        # Match "shall", "must", "required to", "commanded"
        if re.search(r'\b(shall|must|required to|commanded)\b', text, re.IGNORECASE):
            print(f"[!] Target Directive Found at Line {line_num}:")
            print(f"    \"{text}\"")
            
            # Highlight this as a potential point where immunity can be broken if bypassed
            triggered_violations += 1
            
    print("-" * 70)
    print(f"[*] Audit complete. Found {triggered_violations} lines containing mandatory statutory commands.")
    conn.close()

if __name__ == "__main__":
    print("[*] Statutory parser online. Ready to evaluate mandatory language contexts against database doc IDs.")
