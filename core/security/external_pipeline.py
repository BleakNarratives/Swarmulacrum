"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: external_pipeline.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import os
import json
import sqlite3

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"

def compile_packet_for_precedent_filter(chunk_filename):
    chunk_dir = "/storage/emulated/0/RootBase/OutClaw/StagedChunks"
    target_path = os.path.join(chunk_dir, chunk_filename)
    
    if not os.path.exists(target_path):
        print(f"[-] Staged chunk file not found at: {target_path}")
        return

    print(f"[*] Compiling defensive dossier for Precedent Evaluation Filter: {chunk_filename}")
    
    # Connect to local database to grab our hardened legal baselines
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fetch preloaded accountability metrics to weaponize the prompt
    cursor.execute("SELECT doctrine_name, rule_summary FROM liability_benchmarks")
    doctrines = cursor.fetchall()
    
    conn.close()
    
    # Construct the strict structural frame for the External Precedent Model
    packet = []
    packet.append("=== SYSTEM INSTRUCTION FOR EXTERNAL PRECEDENT AUDIT ===")
    packet.append("You are acting as an independent, high-level legal auditing engine.")
    packet.append("Your objective is a zero-trust evaluation of the attached evidentiary document chunk against binding legal precedent.")
    packet.append("Analyze the source data for official overreach, structural fraud, or civil rights violations under color of law.\n")
    
    packet.append("=== IMMUTABLE CONSTITUTIONAL & CIVIL LIABILITY PRECEDENTS ===")
    for name, rule in doctrines:
        packet.append(f"[-] BINDING PRECEDENT: {name}\n    LEGAL STANDARDS: {rule}\n")
        
    packet.append("=== SOURCE EVIDENTIARY FILE LOCATION ===")
    packet.append(f"Target local file scheduled for analysis: {target_path}\n")
    
    packet.append("=== REQUIRED AUDIT OUTPUT STRUCTURE ===")
    packet.append("1. ISOLATED VIOLATIONS: List lines where mandatory language ('shall'/'must') was broken by an official.")
    packet.append("2. IMMUNITY CHIP EVALUATION: Identify where an official stepped outside their scope of employment, piercing qualified immunity based on established precedent.")
    packet.append("3. EVIDENCE INTEGRITY: Flag omissions or hidden records matching Brady/RICO conspiracy structures.")
    packet.append("4. PRECEDENT COMPLIANCE RATING: Rate the output liability risk from '0 (Protected by Law)' to '10 (Immunity Completely Shattered by Precedent)'.")

    # Save the ready-to-pipe packet out as a clean text file
    output_packet_path = f"/storage/emulated/0/RootBase/OutClaw/export_{chunk_filename.replace('.pdf', '.txt')}"
    with open(output_packet_path, "w") as f:
        f.write("\n".join(packet))
        
    print(f"[+] Dossier ready for external pipeline! Packet stored at: {output_packet_path}")
    print("[*] Copy the text from this file or feed it straight to the external model interface.")

if __name__ == "__main__":
    compile_packet_for_precedent_filter("bundle_pages_1_to_10.pdf")
