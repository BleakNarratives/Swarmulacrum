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
    results = {
        "file": filepath,
        "classes": [],
        "functions": [],
        "loc": 0,
        "issues": [],
        "content": "",
        "dna": {},
        "syntax_error": False
    }
    
    dangerous_patterns = [
        ("eval(", "HIGH", "Use of 'eval()' allows arbitrary code execution."),
        ("exec(", "HIGH", "Use of 'exec()' bypasses static type/scope safety."),
        ("shell=True", "CRITICAL", "Subprocess execution with 'shell=True' opens command injection risk."),
        ("os.system(", "MEDIUM", "Direct 'os.system()' call detected; prefer 'subprocess.run()' with args array."),
        ("password =", "CRITICAL", "Potential hardcoded credential detected."),
        ("api_key =", "HIGH", "Potential hardcoded API key detected.")
    ]
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            results["content"] = content
            lines = content.splitlines()
            results["loc"] = len(lines)
            results["dna"] = extract_dna_metadata(content)
            
            for idx, line in enumerate(lines, 1):
                for pattern, severity, desc in dangerous_patterns:
                    if pattern in line:
                        results["issues"].append({
                            "line": idx,
                            "severity": severity,
                            "pattern": pattern,
                            "description": desc,
                            "code_snippet": line.strip()
                        })
            
            try:
                tree = ast.parse(content, filename=filepath)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        results["classes"].append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        results["functions"].append(node.name)
            except SyntaxError as se:
                results["syntax_error"] = True
                results["issues"].append({
                    "line": se.lineno or 0,
                    "severity": "CRITICAL",
                    "pattern": "SyntaxError",
                    "description": f"AST Syntax Parsing Error: {se.msg}",
                    "code_snippet": se.text.strip() if se.text else ""
                })
    except Exception as e:
        results["issues"].append({
            "line": 0, "severity": "INFO", "pattern": "File Error", 
            "description": f"File Read Warning: {str(e)}", "code_snippet": ""
        })
        
    return results

def generate_html_report(target_dir, version_suffix="v2"):
    file_reports = []
    total_loc = 0
    total_classes = 0
    total_functions = 0
    total_issues = 0
    critical_count = 0
    
    output_file = f"Swarmulacrum_Audit_Report_{version_suffix}.html"
    
    for root, _, files in os.walk(target_dir):
        if ".git" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                rep = analyze_file(full_path)
                file_reports.append(rep)
                total_loc += rep["loc"]
                total_classes += len(rep["classes"])
                total_functions += len(rep["functions"])
                total_issues += len(rep["issues"])
                critical_count += sum(1 for i in rep["issues"] if i["severity"] in ["CRITICAL", "HIGH"])
                
    health_score = max(0, 100 - (critical_count * 15 + (total_issues - critical_count) * 5))
    status_color = "#22c55e" if health_score >= 80 else ("#eab308" if health_score >= 50 else "#ef4444")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarmulacrum Security & AST Audit [{version_suffix.upper()}]</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b0f19; color: #e2e8f0; margin: 0; padding: 24px; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        .header {{ border-bottom: 1px solid #1e293b; padding-bottom: 20px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }}
        .title {{ font-size: 22px; font-weight: 700; color: #38bdf8; letter-spacing: -0.5px; }}
        .badge {{ background: {status_color}; color: #0b0f19; padding: 6px 14px; border-radius: 6px; font-weight: 700; font-size: 13px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }}
        .card {{ background: #131c2e; border: 1px solid #1e293b; padding: 18px; border-radius: 8px; text-align: center; }}
        .card-val {{ font-size: 26px; font-weight: 700; color: #f8fafc; margin-top: 4px; }}
        .card-lbl {{ font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; }}
        table {{ width: 100%; border-collapse: collapse; background: #131c2e; border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 14px 18px; text-align: left; border-bottom: 1px solid #1e293b; font-size: 14px; }}
        th {{ background: #0b0f19; color: #64748b; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
        tr.clickable {{ cursor: pointer; transition: background 0.2s ease; outline: none; }}
        tr.clickable:hover, tr.clickable:focus {{ background: #1e293b; box-shadow: inset 3px 0 0 #38bdf8; }}
        .drawer {{ 
            max-height: 0; 
            overflow: hidden; 
            opacity: 0;
            transform: translateY(12px);
            transition: max-height 0.35s cubic-bezier(0, 1, 0, 1), opacity 0.25s ease, transform 0.25s ease;
            background: #0f172a; 
            padding: 0 20px;
            font-family: monospace; 
            font-size: 13px; 
            color: #cbd5e1;
        }}
        .drawer.open {{ 
            max-height: 1200px; 
            opacity: 1;
            transform: translateY(0);
            padding: 20px;
            border-bottom: 2px solid #38bdf8;
            transition: max-height 0.4s ease-in-out, opacity 0.3s ease, transform 0.3s ease;
        }}
        .dna-box {{ background: #1e293b; border-left: 3px solid #38bdf8; padding: 10px 14px; margin-bottom: 12px; border-radius: 0 4px 4px 0; }}
        .issue-box {{ background: #3b0707; border: 1px solid #f87171; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; color: #fca5a5; }}
        .syntax-alert {{ background: #450a0a; border: 1px solid #ef4444; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px; color: #fca5a5; font-weight: 600; }}
        .code-block {{ background: #0b0f19; padding: 14px; border-radius: 6px; overflow-x: auto; max-height: 280px; border: 1px solid #1e293b; color: #38bdf8; white-space: pre-wrap; }}
        @media (max-width: 600px) {{
            .metrics {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .header {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
            table {{ display: block; overflow-x: auto; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="title">Swarmulacrum Executive Security Audit [{version_suffix.upper()}]</div>
                <div style="color: #64748b; font-size: 12px; margin-top: 4px;">Target: {target_dir} | Scanned: {time.strftime("%Y-%m-%d %H:%M:%S")}</div>
            </div>
            <div class="badge">HEALTH SCORE: {health_score}%</div>
        </div>
        
        <div class="metrics">
            <div class="card"><div class="card-lbl">Files Analyzed</div><div class="card-val">{len(file_reports)}</div></div>
            <div class="card"><div class="card-lbl">Lines of Code</div><div class="card-val">{total_loc}</div></div>
            <div class="card"><div class="card-lbl">AST Functions / Classes</div><div class="card-val">{total_functions} / {total_classes}</div></div>
            <div class="card"><div class="card-lbl">Security Issues</div><div class="card-val" style="color: {'#22c55e' if total_issues == 0 else '#f87171'}">{total_issues}</div></div>
        </div>
        
        <h3>Module Integrity & AST Breakdown</h3>
        <table>
            <thead>
                <tr>
                    <th>Module Path</th>
                    <th>LOC</th>
                    <th>Functions</th>
                    <th>Classes</th>
                    <th>Security Status</th>
                </tr>
            </thead>
            <tbody>
"""
    for idx, rep in enumerate(file_reports):
        rel_path = os.path.relpath(rep["file"], target_dir)
        issue_cnt = len(rep["issues"])
        if rep["syntax_error"]:
            status_str = '<span style="color: #ef4444; font-weight: 700;">PARSE WARNING</span>'
        elif issue_cnt == 0:
            status_str = '<span style="color: #22c55e; font-weight: 600;">PASSED</span>'
        else:
            status_str = f'<span style="color: #f87171; font-weight: 600;">{issue_cnt} Finding(s)</span>'
        
        drawer_id = f"drawer_{idx}"
        
        html_content += f"""
                <tr class="clickable" tabindex="0" onclick="toggleDrawer('{drawer_id}')">
                    <td><code>{rel_path}</code></td>
                    <td>{rep["loc"]}</td>
                    <td>{len(rep["functions"])}</td>
                    <td>{len(rep["classes"])}</td>
                    <td>{status_str}</td>
                </tr>
                <tr>
                    <td colspan="5" style="padding:0; border:none;">
                        <div id="{drawer_id}" class="drawer">
"""
        if rep["syntax_error"]:
            html_content += "<div class='syntax-alert'>⚠️ AST PARSING FALLBACK: SyntaxError detected during static inspection. Source displayed in raw inspection view below.</div>"

        if rep["dna"]:
            html_content += "<div class='dna-box'><strong>DNA Backtag Metadata:</strong><br>"
            for k, v in rep["dna"].items():
                html_content += f"<span style='color: #94a3b8;'>{k}:</span> {html.escape(v)} | "
            html_content += "</div>"

        html_content += f"""
                            <strong>AST Map:</strong><br>
                            Functions ({len(rep['functions'])}): {', '.join(rep['functions']) if rep['functions'] else 'None'}<br>
                            Classes ({len(rep['classes'])}): {', '.join(rep['classes']) if rep['classes'] else 'None'}<br><br>
"""
        if rep["issues"]:
            html_content += "<strong>Security Findings:</strong><br>"
            for iss in rep["issues"]:
                html_content += f"""
                            <div class="issue-box">
                                [Line {iss['line']}] [{iss['severity']}] {iss['description']}<br>
                                <code>{html.escape(iss['code_snippet'])}</code>
                            </div>
"""
        else:
            html_content += "<div style='color: #22c55e; margin-bottom: 10px;'>✓ Module structure verified. Zero security flags.</div>"

        escaped_code = html.escape(rep["content"])
        html_content += f"""
                            <strong>Source Code Inspection:</strong>
                            <div class="code-block">{escaped_code}</div>
                        </div>
                    </td>
                </tr>
"""
    html_content += """
            </tbody>
        </table>
    </div>

    <script>
        function toggleDrawer(id) {
            var el = document.getElementById(id);
            el.classList.toggle('open');
        }

        document.addEventListener('keydown', function(event) {
            const rows = Array.from(document.querySelectorAll('tr.clickable'));
            const currentIndex = rows.findIndex(r => r === document.activeElement);

            if (event.key === 'ArrowDown') {
                if (currentIndex === -1) {
                    rows[0].focus();
                } else {
                    rows[(currentIndex + 1) % rows.length].focus();
                }
                event.preventDefault();
            } else if (event.key === 'ArrowUp') {
                if (currentIndex === -1) {
                    rows[rows.length - 1].focus();
                } else {
                    rows[(currentIndex - 1 + rows.length) % rows.length].focus();
                }
                event.preventDefault();
            } else if (event.key === 'Enter' || event.key === ' ') {
                if (document.activeElement.classList.contains('clickable')) {
                    document.activeElement.click();
                    event.preventDefault();
                }
            }
        });
    </script>
</body>
</html>
"""
    full_output_path = os.path.join(target_dir, output_file)
    with open(full_output_path, "w") as f:
        f.write(html_content)
    return full_output_path

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    out = generate_html_report(target, version_suffix="v2")
    print(f"[Audit Engine v2.1] Report saved to: {out}")
