"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: outclaw_validator.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import re

def validate_session(question: str, answer: str) -> dict:
    """
    Validates OutClaw legal session output before it's shown as final/resolved.
    Returns: {"pass": bool, "issues": list}

    What this DOES NOT catch:
    - Factual accuracy of statutes or case law (flags for human review, doesn't verify).
    - Tone appropriateness.
    - Logical fallacies that mimic valid legal reasoning.
    - Citation formats outside the patterns below (state-specific codes, etc.)
    """
    issues = []

    if len(answer.strip()) < 20:
        issues.append("Answer is too short to be substantive.")

    action_verbs = ["file", "contact", "consult", "send", "review", "draft", "verify", "request"]
    if not any(verb in answer.lower() for verb in action_verbs):
        issues.append("Missing actionable next-step verbs.")

    disclaimer_keywords = ["not legal advice", "consult an attorney", "for informational purposes"]
    if not any(dk in answer.lower() for dk in disclaimer_keywords):
        issues.append("Missing mandatory legal liability disclaimer.")

    # Citation patterns, checked independently — a match on one doesn't get
    # cancelled out by unrelated words elsewhere in the answer.
    citation_patterns = [
        r'\d+\s+U\.?S\.?C\.?\s*§?\s*\d+',           # 42 U.S.C. § 1983 / 18 USC 1001
        r'\d+\s+C\.?F\.?R\.?\s*§?\s*\d+',           # 29 C.F.R. 1604
        r'§\s*\d+[\.\d]*',                          # § 1983, § 12.5
        r'\b[A-Z][a-zA-Z\'\.]+\s+v\.?\s+[A-Z][a-zA-Z\'\.]+',  # Smith v. Jones
        r'\bRule\s+\d+',                            # Rule 12
        r'\d+\s+F\.\s?\d?d?\s+\d+',                 # 123 F.3d 456
    ]
    matched = [pat for pat in citation_patterns if re.search(pat, answer)]
    if matched:
        issues.append("Cited specific statute or case law - REQUIRES MANUAL VERIFICATION.")

    return {
        "pass": len(issues) == 0,
        "issues": issues
    }

# --- full regression suite ---
tests = {
    "1: real USC citation": (
        "Can my landlord evict me without notice?",
        "Under 42 U.S.C. § 1983, tenants have due process rights. You should contact a tenant rights attorney."
    ),
    "2: zip code, no real citation": (
        "How do I find my local courthouse?",
        "You can find your local courthouse by searching your zip code on the county website, or contact the clerk's office."
    ),
    "3: clean pass": (
        "Can I get my security deposit back?",
        "In most states you can file a small claims request. This is not legal advice, please consult an attorney to verify your state's specific timeline."
    ),
    "4: case law citation (Smith v. Jones)": (
        "Do I have a free speech right at work?",
        "This depends on context. See Smith v. Jones for a similar precedent. Consult an attorney to verify."
    ),
    "5: real citation + coincidental 'zip code' in same answer": (
        "Can I be fined for this?",
        "Under 42 U.S.C. § 1983 your rights may apply, contact your county's zip code office for local enforcement info."
    ),
    "6: CFR citation": (
        "Can my employer do this?",
        "Refer to 29 C.F.R. 1604 on workplace harassment. Contact an employment attorney to verify."
    ),
    "7: too short / non-answer": (
        "Can I sue my neighbor?",
        "Maybe."
    ),
}

all_pass = True
for label, (q, a) in tests.items():
    result = validate_session(q, a)
    print(f"--- {label} ---\n{result}\n")
