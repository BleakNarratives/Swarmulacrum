"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: orchestrator.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import os
from OutClaw.sentinel.docket_scraper import SentinelDocketScraper
from OutClaw.sentinel.grievance_auditor import GrievanceAuditor
from ModMind.molt_engine import MOLT_v7_Engine

def run_outclaw_pipeline():
    print("[*] Starting OutClaw Functional Pipeline...")
    
    # 1. Ingestion
    sentinel = SentinelDocketScraper("Active Case")
    draft_path = sentinel.fetch_new_filings()
    
    # 2. Audit and Refine (Recursive Loop)
    engine = MOLT_v7_Engine()
    
    status = "FLAGGED"
    attempts = 0
    while status == "FLAGGED" and attempts < 3:
        status = engine.assess_and_refine(draft_path)
        attempts += 1
        
    print(f"[*] Pipeline complete. Final status: {status}")

if __name__ == "__main__":
    run_outclaw_pipeline()
