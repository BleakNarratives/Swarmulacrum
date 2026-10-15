"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: smoke_test.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import re
from case_db_core import CaseDatabase

class VerificationSmokeTest:
    def __init__(self):
        self.db = CaseDatabase()

    def clean_text(self, text):
        """Standardize text to prevent mismatching on whitespace or punctuation."""
        return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

    def verify_response_integrity(self, ai_output_text):
        print("\n" + "="*60)
        print("          ENTERING ZERO-TRUST VERIFICATION LOOP")
        print("="*60)
        
        # Pattern to look for citations like: [Document | Line X]: "quoted text"
        # or standard quotes containing statutory assertions.
        quotes = re.findall(r'"([^"]*)"', ai_output_text)
        
        if not quotes:
            print("[!] WARNING: No direct quotes found in the AI response to validate.")
            print("[!] Enterprise protocol requires explicit database citations.")
            return False

        hallucination_detected = False
        verified_count = 0

        for quote in quotes:
            cleaned_quote = quote.strip()
            if len(cleaned_quote) < 10:  # Skip short conversational phrases
                continue
                
            print(r"[*] Validating quote:f' \"{cleaned_quote[:50]}...\"'")
            
            # Query the local database for this exact string snippet
            matches = self.db.query_exact_text(cleaned_quote)
            
            if matches:
                print(f"    [✓] VERIFIED: Found match in {matches[0][0]} at Line {matches[0][1]}")
                verified_count += 1
            else:
                # Let's do a fuzzy fallback check in case of slight casing/spacing shifts
                words = cleaned_quote.split()
                anchor_word = words[0] if words else ""
                fallback_matches = self.db.query_exact_text(anchor_word) if anchor_word else []
                
                fuzzy_found = False
                for f_match in fallback_matches:
                    if self.clean_text(cleaned_quote) in self.clean_text(f_match[2]):
                        print(f"    [✓] VERIFIED (Fuzzy Match): Found in {f_match[0]} at Line {f_match[1]}")
                        verified_count += 1
                        fuzzy_found = True
                        break
                        
                if not fuzzy_found:
                    print(f"    [X] CRITICAL FAILURE: Hallucination or broken citation detected!")
                    print(f"        The AI claimed this text exists, but it is NOT in your database.")
                    hallucination_detected = True

        print("-" * 60)
        print(f"[*] Smoke Test Summary: Verified Anchors: {verified_count} | Hallucinations: {1 if hallucination_detected else 0}")
        
        if hallucination_detected:
            print("[-] STATUS: REJECTED. Do not use this output in a legal brief.")
            return False
        else:
            print("[+] STATUS: PASSED. Output is verified against the local baseline records.")
            return True

if __name__ == "__main__":
    # Sample execution testing a mock validation string
    tester = VerificationSmokeTest()
    sample_ai_response = 'The report states "suspect fled on foot" which contradicts the physical evidence.'
    tester.verify_response_integrity(sample_ai_response)
