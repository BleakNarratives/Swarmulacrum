"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: rebuttal_engine.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import sys
import json
from case_db_core import CaseDatabase

# Load UI config
with open("ui_config.json", "r") as f:
    config = json.load(f)["rebuttal"]

def generate_rebuttal_brief(keyword_query):
    db = CaseDatabase()
    matches = db.query_exact_text(keyword_query)
    
    if not matches:
        print(f"[-] {config['no_matches']}: '{keyword_query}'")
        return

    print(f"\n{'='*60}")
    print(f"       {config['title']}")
    print(f"{'='*60}")
    
    context_payload = []
    for match in matches:
        doc, line, text = match
        anchor = f"[{doc} | Line {line}]: {text}"
        print(anchor)
        context_payload.append(anchor)

    print("-" * 60)
    print(f"[*] {config['prompt_header']}")
    print("-" * 60)
    
    # This explicit engineering wrapper completely blocks the model from backing down or shifting definitions
    system_override = f"""
    You are an unyielding legal strategist executing an ironclad critique. 
    You are barred from using polite corporate phrases, pleasantries, or hedging statements.
    Do NOT ever say 'You are right' or 'My apologies' to the user. Stick to the text below.
    
    CRITICAL LOCAL DATA PROFILE:
    {chr(10).join(context_payload)}
    
    Task: Rebut the prosecution/official narrative using ONLY the explicit data records above. 
    If the official account varies from these indexed lines, cross-examine the variance ruthlessly.
    """
    
    print(system_override)
    print(f"{'='*60}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Usage: python rebuttal_engine.py <search_keyword>")
    else:
        generate_rebuttal_brief(" ".join(sys.argv[1:]))
