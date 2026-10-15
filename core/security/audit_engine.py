import os, sys, ast, json, time, html, re

def extract_dna_metadata(content):
    dna = {}
    match = re.search(r'\[DNA_TAG\](.*?)\[/DNA_TAG\]', content, re.DOTALL)
    if match:
        tag_block = match.group(1).strip()
        for line in tag_block.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                dna[key.strip()] = val.strip()
    return dna

def analyze_file(filepath):
    results = {"file": filepath, "classes": [], "functions": [], "loc": 0, "issues": [], "content": "", "dna": {}}
    dangerous_patterns = [
        ("eval(", "HIGH", "Use of 'eval()' detected."),
        ("os.system(", "MEDIUM", "Direct 'os.system()' call detected.")
    ]
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            results["content"] = content
            lines = content.splitlines()
            results["loc"] = len(lines)
            results["dna"] = extract_dna_metadata(content)
            
            tree = ast.parse(content, filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef): results["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef): results["functions"].append(node.name)
    except: pass
    return results

def generate_html_report(target_dir):
    reports = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"): reports.append(analyze_file(os.path.join(root, file)))
    
    html_content = "<html><style>body{background:#0b0f19;color:#fff;}.drawer{max-height:0;overflow:hidden;transition:0.4s;}.open{max-height:500px;}</style><body>"
    for r in reports:
        html_content += f"<div onclick=\"document.getElementById('{r['file']}').classList.toggle('open')\">{r['file']}</div>"
        html_content += f"<div id='{r['file']}' class='drawer'>DNA: {r['dna']}</div>"
    html_content += "</body></html>"
    with open("Swarmulacrum_Audit_Report_v2.html", "w") as f: f.write(html_content)
    print("[Audit v2.0] Report: Swarmulacrum_Audit_Report_v2.html")

if __name__ == "__main__":
    generate_html_report(sys.argv[1])
