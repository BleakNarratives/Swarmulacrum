"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: preload_liability_matrix.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
import sqlite3

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"

def expand_liability_matrix():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table 3: Liability and Accountability Benchmarks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS liability_benchmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            doctrine_name TEXT,
            rule_summary TEXT,
            actionable_trigger TEXT
        )
    """)
    
    benchmarks = [
        (
            "Immunity & Surety",
            "Piercing Qualified Immunity",
            "Public officials lose qualified immunity when their conduct violates clearly established statutory or constitutional rights of which a reasonable person would have known (Harlow v. Fitzgerald).",
            "Violation of a clearly established constitutional right or explicit statutory mandate."
        ),
        (
            "Immunity & Surety",
            "Exiting the Umbrella of Surety (Personal Liability)",
            "A public official's faithful performance bond or public official surety bond only covers lawful acts within the scope of employment. Acts committed under fraud, malice, or intentional deprivation of rights break the bond terms, exposing the official's personal assets.",
            "Ultra vires actions, intentional torts, or criminal acts under color of law."
        ),
        (
            "Ministerial vs Judicial",
            "The Ministerial Duty Exception ('Must' vs 'Shall')",
            "A ministerial act is one where the official has no discretion—the law commands performance in a specified manner under given facts. If a statute says 'shall' or 'must', the act is ministerial. Failure to perform, or performing it outside the mandate, leaves no room for judicial or administrative discretion, destroying immunity.",
            "Violation of an explicit mandatory directive ('shall', 'must', 'will') in state or federal code."
        ),
        (
            "Legal Ethics & Bar Rules",
            "ABA Standard / State Supreme Court Bar Grievances",
            "Attorneys are officers of the court and bound by Rules of Professional Conduct (e.g., Rule 3.3 Candor Toward the Tribunal, Rule 8.4 Misconduct). Filing fraudulent documents or knowingly misrepresenting facts to a judge warrants immediate Bar Grievances and Judicial Complaints directly to the State Supreme Court.",
            "Falsification of records, material omissions, or intimidating witnesses/parties under color of legal proceedings."
        ),
        (
            "Consumer Protection",
            "FTC Act Section 5 & Unfair Deceptive Practices",
            "Prohibits unfair or deceptive acts or practices in or affecting commerce. When private corporate actors or commercial debt collectors pose as or collaborate with corrupt state actors to execute fraudulent actions, it triggers severe statutory penalties.",
            "Deceptive commercial claims, fraudulent representations of authority, or predatory collection schemes."
        )
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO liability_benchmarks (category, doctrine_name, rule_summary, actionable_trigger)
        VALUES (?, ?, ?, ?)
    """, benchmarks)
    
    conn.commit()
    print(f"[+] Loaded {len(benchmarks)} high-caliber liability and immunity doctrines into database.")
    conn.close()

if __name__ == "__main__":
    expand_liability_matrix()
