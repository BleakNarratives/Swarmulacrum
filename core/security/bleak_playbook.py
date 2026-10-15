"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: bleak_playbook.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import os
import re
import json
import sys

class RealLegalAnalyzer:
    def __init__(self):
        # The actual target statutory and administrative patterns to scan for in real documents
        self.target_patterns = {
            "civil_rights_1983": [r"1983", r"color\s+of\s+law", r"deprivation\s+of\s+rights"],
            "criminal_conspiracy_241": [r"241", r"conspiracy\s+against\s+rights"],
            "criminal_deprivation_242": [r"242", r"deprivation\s+under\s+color"],
            "procedural_defenses": [r"immunity", r"good\s+faith", r"discretionary"],
            "administrative_breaches": [r"oath", r"ministerial", r"mandate", r"jurisdiction"]
        }

    def process_case_document(self, file_path):
        """
        Reads a real raw text file, executes precise regex matching, 
        and extracts the exact surrounding text for verification.
        """
        if not os.path.exists(file_path):
            print(f"[-] ERROR: File not found at {file_path}")
            return None

        print(f"[*] Parsing real-world text from: {file_path}")
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        analysis_report = {
            "source_document": file_path,
            "total_lines_scanned": len(lines),
            "matches_found": {}
        }

        # Scan line by line to pull the actual context where matches occur
        for line_idx, line in enumerate(lines):
            clean_line = line.strip()
            for category, regex_list in self.target_patterns.items():
                for pattern in regex_list:
                    if re.search(pattern, clean_line, re.IGNORECASE):
                        if category not in analysis_report["matches_found"]:
                            analysis_report["matches_found"][category] = []
                        
                        # Capture the line number and the exact text line where it happened
                        analysis_report["matches_found"][category].append({
                            "line_number": line_idx + 1,
                            "matched_pattern": pattern,
                            "context": clean_line
                        })

        return analysis_report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Usage: bleakplay <path_to_raw_text_file>")
        sys.exit(1)

    target_file = sys.argv[1]
    analyzer = RealLegalAnalyzer()
    report = analyzer.process_case_document(target_file)

    if report:
        # Write the actual results out to a real JSON file for validation
        output_path = "/storage/emulated/0/RootBase/OutClaw/case_analysis_output.json"
        with open(output_path, 'w', encoding='utf-8') as out_f:
            json.dump(report, out_f, indent=4)
        
        print(f"[+] Scan execution complete. Real matches logged to: {output_path}")
        print(f"[*] Summary of Categories Found: {list(report['matches_found'].keys())}")
