"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: legal_maxims.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
OUTCLAW LEGAL MAXIMS

"He who can be fooled, let him." - The First Maxim of Law

Timeless legal principles, maxims, and aphorisms that guide legal reasoning.

"""

import sqlite3
from typing import Dict, List, Optional

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"


class LegalMaxims:
    """
    Collection of legal maxims, principles, and time-tested wisdom for legal analysis.
    """
    
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()
        
        # Fundamental Legal Maxims
        self.maxims = {
            "first_maxim": {
                "text": "He who can be fooled, let him.",
                "latin": "Qui decipi potest, decipiatur.",
                "meaning": "The law does not protect those who are willfully blind or gullible. "
                         "If someone can be fooled, they will be - and the law provides no remedy.",
                "application": "Always verify, never assume. The law protects the vigilant, "
                             "not the careless. If you sign something without reading it, "
                             "you're bound by it. If you believe what you're told without verification, "
                             "you have no recourse.",
                "category": "Fundamental Principle",
                "source": "Ancient Roman Law",
                "importance": "CRITICAL",
                "quote": "This is the very first maxim of law - the foundation of all legal wisdom"
            },
            
            "ignorance_no_excuse": {
                "text": "Ignorance of the law is no excuse.",
                "latin": "Ignorantia legis neminem excusat.",
                "meaning": "Every person is presumed to know the law. Not knowing a law "
                         "does not excuse violation of it.",
                "application": "This is why legal education is CRITICAL. You cannot claim "
                             "ignorance as a defense. Knowledge is your only protection.",
                "category": "Fundamental Principle",
                "source": "Roman Law",
                "importance": "CRITICAL"
            },
            
            "equality_before_law": {
                "text": "All are equal before the law.",
                "latin": "Omnes legis servi sumus ut liberi esse possimus.",
                "meaning": "The law applies equally to all persons, regardless of status or position.",
                "application": "No one is above the law - not judges, not police, not officials. "
                             "Use this to demand equal treatment.",
                "category": "Equality",
                "source": "Roman Law",
                "importance": "HIGH"
            },
            
            "no_one_judge_own_cause": {
                "text": "No one shall be a judge in his own cause.",
                "latin": "Nemo judex in causa sua.",
                "meaning": "A person cannot be impartial when they have a personal interest in the outcome.",
                "application": "Use to demand recusal of judges with conflicts of interest. "
                             "Also applies to administrative officials making decisions that affect them personally.",
                "category": "Due Process",
                "source": "Natural Law",
                "importance": "CRITICAL",
                "remedy": "Motion for recusal, demand for impartial tribunal"
            },
            
            "he_who_acts_as_judge": {
                "text": "He who acts as judge must act according to law.",
                "latin": "Judex non potest dare quod non habet.",
                "meaning": "Judges (and all officials) must follow the law, not their own preferences.",
                "application": "When a judge violates the law, they act without authority. "
                             "Their rulings are VOID.",
                "category": "Judicial Authority",
                "source": "Common Law",
                "importance": "CRITICAL"
            },
            
            "where_there_is_right_there_is_remedy": {
                "text": "Where there is a right, there is a remedy.",
                "latin": "Ubi jus, ibi remedium.",
                "meaning": "For every legal right, there exists a legal remedy for its violation.",
                "application": "If your rights have been violated, the law provides a way to seek redress. Never accept that there's nothing you can do.",
                "category": "Rights and Remedies",
                "source": "Common Law",
                "importance": "CRITICAL"
            },
            
            "justice_delayed_is_justice_denied": {
                "text": "Justice delayed is justice denied.",
                "latin": "Justitia tarda est justitia denegata.",
                "meaning": "Unreasonable delay in obtaining justice is equivalent to denial of justice.",
                "application": "Use to demand timely court action, oppose unreasonable delays, seek expedited proceedings when necessary.",
                "category": "Procedural Justice",
                "source": "Common Law",
                "importance": "HIGH",
                "remedy": "Motion to advance, motion for expedited hearing"
            },
            
            "he_who_seeks_equity_must_do_equity": {
                "text": "He who seeks equity must do equity.",
                "latin": "Qui aequitatem petiti, aequitatem facere debet.",
                "meaning": "To receive fair treatment from the court, you must act fairly yourself.",
                "application": "Clean hands doctrine - you cannot seek equitable relief if "
                             "you've acted unfairly or in bad faith.",
                "category": "Equity",
                "source": "Chancery Courts",
                "importance": "HIGH"
            },
            
            "he_who_comes_into_equity_must_come_with_clean_hands": {
                "text": "He who comes into equity must come with clean hands.",
                "latin": "Qui in aequitate venit, venit in puris manibus.",
                "meaning": "A party seeking equitable relief must not have acted improperly "
                         "in the matter before the court.",
                "application": "Defense against claims by those acting in bad faith. "
                             "Also a warning: don't engage in misconduct yourself.",
                "category": "Equity",
                "source": "Chancery Courts",
                "importance": "HIGH"
            },
            
            "fraud_unravels_everything": {
                "text": "Fraud unravels everything.",
                "latin": "Fraus omnia corrumpit.",
                "meaning": "Fraud vitiates all transactions, contracts, and proceedings tainted by it.",
                "application": "If you can prove fraud, you can void contracts, challenge "
                             "court rulings, and expose corruption.",
                "category": "Fraud",
                "source": "Common Law",
                "importance": "CRITICAL",
                "remedy": "Void ab initio (void from the beginning)"
            },
            
            "expressio_unius_est_exclusio_alterius": {
                "text": "The express mention of one thing is the exclusion of another.",
                "latin": "Expressio unius est exclusio alterius.",
                "meaning": "When a law or contract specifically lists certain things, "
                         "it implicitly excludes things not listed.",
                "application": "Use to limit government power to ONLY what is explicitly "
                             "stated in statutes. If a power isn't listed, they don't have it.",
                "category": "Statutory Interpretation",
                "source": "Common Law",
                "importance": "CRITICAL"
            },
            
            "ejusdem_generis": {
                "text": "Of the same kind.",
                "latin": "Ejusdem generis.",
                "meaning": "When a law lists specific things followed by general language, "
                         "the general language is limited to things of the same kind as the specifics.",
                "application": "Limits broad interpretive language to similar categories.",
                "category": "Statutory Interpretation",
                "source": "Common Law",
                "importance": "MEDIUM"
            },
            
            "noscitur_a_sociis": {
                "text": "It is known from its associates.",
                "latin": "Noscitur a sociis.",
                "meaning": "The meaning of unclear words can be determined by the company they keep.",
                "application": "Use to interpret ambiguous legal terms based on surrounding "
                             "words and context.",
                "category": "Statutory Interpretation",
                "source": "Common Law",
                "importance": "MEDIUM"
            },
            
            "in_pari_materia": {
                "text": "Upon the same matter or subject.",
                "latin": "In pari materia.",
                "meaning": "Statutes dealing with the same subject matter should be "
                         "construed together and harmonized if possible.",
                "application": "When interpreting a law, look at related laws on the same topic.",
                "category": "Statutory Interpretation",
                "source": "Common Law",
                "importance": "MEDIUM"
            },
            
            "stare_decisis": {
                "text": "To stand by things decided.",
                "latin": "Stare decisis.",
                "meaning": "Courts should follow precedent - previous rulings on similar "
                         "legal issues should guide current decisions.",
                "application": "Use established case law to support your arguments. "
                             "Also use to challenge courts that ignore precedent.",
                "category": "Precedent",
                "source": "Common Law",
                "importance": "CRITICAL"
            },
            
            "res_judicata": {
                "text": "A matter judged.",
                "latin": "Res judicata.",
                "meaning": "A final judgment by a court of competent jurisdiction bars "
                         "further litigation of the same claim between the same parties.",
                "application": "Prevents re-litigation of already-decided cases. "
                             "Can be used as a defense.",
                "category": "Finality",
                "source": "Common Law",
                "importance": "HIGH"
            },
            
            "collateral_estoppel": {
                "text": "Issue preclusion.",
                "latin": "Collateral estoppel (modern term).",
                "meaning": "When an issue has been actually litigated and determined in a "
                         "previous case, the parties cannot re-litigate that issue.",
                "application": "Binds parties to previously-decided issues, even in different cases.",
                "category": "Finality",
                "source": "Common Law",
                "importance": "HIGH"
            },
            
            "actus_reus_non_facit_reum_nisi_mens_sit_rea": {
                "text": "An act does not make a person guilty unless the mind is also guilty.",
                "latin": "Actus reus non facit reum nisi mens sit rea.",
                "meaning": "For criminal liability, there must be both a guilty act AND a guilty mind.",
                "application": "Requires proof of intent, not just the action itself.",
                "category": "Criminal Law",
                "source": "Common Law",
                "importance": "HIGH"
            },
            
            "nullum_crimen_sine_lege": {
                "text": "No crime without law.",
                "latin": "Nullum crimen sine lege.",
                "meaning": "An act cannot be criminal unless it violates a specific criminal law.",
                "application": "Protects against retroactive criminal laws and vague statutes. "
                             "If there's no law against it, it's not a crime.",
                "category": "Criminal Law",
                "source": "Roman Law",
                "importance": "CRITICAL"
            },
            
            "nulla_poena_sine_lege": {
                "text": "No punishment without law.",
                "latin": "Nulla poena sine lege.",
                "meaning": "There can be no criminal punishment without a specific penal law.",
                "application": "Limits judicial creativity in sentencing. Punishment must be "
                             "authorized by law.",
                "category": "Criminal Law",
                "source": "Roman Law",
                "importance": "CRITICAL"
            },
            
            "fructus_naturales": {
                "text": "Natural fruits.",
                "latin": "Fructus naturales.",
                "meaning": "Natural productions of the earth that require no human labor.",
                "application": "Property law - distinction between natural and industrial products.",
                "category": "Property Law",
                "source": "Common Law",
                "importance": "LOW"
            },
            
            "sic_utere_tuo_ut_alienum_non_laedas": {
                "text": "Use your own property in such a manner as not to injure that of another.",
                "latin": "Sic utere tuo ut alienum non laedas.",
                "meaning": "Property rights are not absolute - you cannot use your property "
                         "in a way that harms others.",
                "application": "Limit on property rights. Basis for nuisance law.",
                "category": "Property Law",
                "source": "Roman Law",
                "importance": "MEDIUM"
            },
            
            "qui_tacet_consentire_videtur": {
                "text": "He who is silent appears to consent.",
                "latin": "Qui tacet consentire videtur.",
                "meaning": "Silence in the face of an offer or statement may be interpreted as consent.",
                "application": "Be careful - failing to object can be seen as agreement. "
                             "ALWAYS object to preserve your rights.",
                "category": "Contracts and Procedure",
                "source": "Roman Law",
                "importance": "HIGH",
                "warning": "This is why you MUST object to court actions you disagree with. "
                          "Silence = consent."
            },
            
            "ex_abundanti_cautela": {
                "text": "Out of abundant caution.",
                "latin": "Ex abundant cautela.",
                "meaning": "Taking extra precautions to avoid any possible error or omission.",
                "application": "In legal practice: double-check everything, document everything, "
                             "preserve all objections, create a complete record.",
                "category": "Practice and Procedure",
                "source": "Common Law",
                "importance": "HIGH"
            },
            
            "de_minimis_non_curat_lex": {
                "text": "The law does not concern itself with trifles.",
                "latin": "De minimis non curat lex.",
                "meaning": "The law will not intervene in trivial matters.",
                "application": "Use to argue that minor technical violations should not "
                             "result in serious consequences.",
                "category": "General Principle",
                "source": "Common Law",
                "importance": "MEDIUM"
            },
            
            "lex_non_cogit_ad_impossibilia": {
                "text": "The law does not compel the impossible.",
                "latin": "Lex non cogit ad impossibilia.",
                "meaning": "The law does not require a person to do what is impossible.",
                "application": "Defense when compliance with a law or order is impossible.",
                "category": "General Principle",
                "source": "Common Law",
                "importance": "MEDIUM"
            },
            
            "salus_populi_suprema_lex_esto": {
                "text": "Let the welfare of the people be the supreme law.",
                "latin": "Salus populi suprema lex esto.",
                "meaning": "The safety and welfare of the people should be the highest law.",
                "application": "Principle that government exists to serve the people, "
                             "not the other way around.",
                "category": "Government Purpose",
                "source": "Roman Law (Cicero)",
                "importance": "CRITICAL"
            },
            
            "vigilantibus_non_dormientibus_jura_subveniunt": {
                "text": "The laws aid the vigilant, not those who sleep upon their rights.",
                "latin": "Vigilantibus non dormientibus jura subveniunt.",
                "meaning": "The law protects those who are watchful and proactive, "
                         "not those who are careless or passive.",
                "application": "CRITICAL: You MUST be proactive in asserting your rights. "
                             "Statutes of limitations, notice requirements, and filing "
                             "deadlines are strictly enforced.",
                "category": "Fundamental Principle",
                "source": "Roman Law",
                "importance": "CRITICAL",
                "warning": "This relates directly to the First Maxim. The vigilant are protected; "
                          "the careless are not."
            }
        }
        
        self._load_into_db()
    
    def _init_db(self):
        """Initialize database table for legal maxims."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS legal_maxims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                maxim_id TEXT UNIQUE,
                text TEXT,
                latin TEXT,
                meaning TEXT,
                application TEXT,
                category TEXT,
                source TEXT,
                importance TEXT,
                warning TEXT,
                remedy TEXT,
                quote TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_into_db(self):
        """Load maxims into database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing
        cursor.execute("DELETE FROM legal_maxims")
        
        # Insert all maxims
        for maxim_id, data in self.maxims.items():
            cursor.execute("""
                INSERT INTO legal_maxims (
                    maxim_id, text, latin, meaning, application, category, 
                    source, importance, warning, remedy, quote
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                maxim_id,
                data.get('text'),
                data.get('latin'),
                data.get('meaning'),
                data.get('application'),
                data.get('category'),
                data.get('source'),
                data.get('importance'),
                data.get('warning'),
                data.get('remedy'),
                data.get('quote')
            ))
        
        conn.commit()
        conn.close()
    
    def get_maxim(self, maxim_id: str) -> Optional[Dict]:
        """Get a specific legal maxim by ID."""
        return self.maxims.get(maxim_id)
    
    def get_all_maxims(self) -> Dict:
        """Get all legal maxims."""
        return self.maxims
    
    def get_maxims_by_category(self, category: str) -> List[Dict]:
        """Get all maxims in a specific category."""
        return {k: v for k, v in self.maxims.items() if v.get('category') == category}
    
    def get_maxims_by_importance(self, importance: str) -> List[Dict]:
        """Get all maxims of a specific importance level."""
        return {k: v for k, v in self.maxims.items() if v.get('importance') == importance}
    
    def search_maxims(self, query: str) -> List[Dict]:
        """Search maxims by text, meaning, or application."""
        query_lower = query.lower()
        results = []
        
        for maxim_id, data in self.maxims.items():
            if (query_lower in data.get('text', '').lower() or
                query_lower in data.get('meaning', '').lower() or
                query_lower in data.get('application', '').lower() or
                query_lower in data.get('latin', '').lower()):
                results.append({"id": maxim_id, **data})
        
        return results
    
    def get_critical_maxims(self) -> List[Dict]:
        """Get all critical legal maxims - the most important ones."""
        return self.get_maxims_by_importance("CRITICAL")
    
    def get_first_maxim(self) -> Dict:
        """Get the very first maxim of law."""
        return self.get_maxim("first_maxim")
    
    def get_maxim_of_the_day(self) -> Dict:
        """Get a random maxim for daily contemplation."""
        import random
        maxim_ids = list(self.maxims.keys())
        return self.maxims[random.choice(maxim_ids)]


# Singleton
_maxims = None


def get_legal_maxims():
    """Get or create the singleton legal maxims instance."""
    global _maxims
    if _maxims is None:
        _maxims = LegalMaxims()
    return _maxims


if __name__ == "__main__":
    print("=" * 80)
    print("OUTCLAW LEGAL MAXIMS")
    print("Timeless Wisdom for the Legal Warrior")
    print("=" * 80)
    
    maxims = get_legal_maxims()
    
    # Show the First Maxim
    first = maxims.get_first_maxim()
    print("\n" + "=" * 80)
    print("THE FIRST MAXIM OF LAW")
    print("=" * 80)
    print(f"\nEnglish: {first['text']}")
    print(f"Latin: {first['latin']}")
    print(f"\nMeaning: {first['meaning']}")
    print(f"\nApplication: {first['application']}")
    print(f"\nQuote: {first.get('quote', '')}")
    print(f"\nSource: {first['source']}")
    print(f"Importance: {first['importance']}")
    
    # Show other critical maxims
    print("\n" + "=" * 80)
    print("CRITICAL LEGAL MAXIMS")
    print("=" * 80)
    
    critical = maxims.get_critical_maxims()
    for maxim_id, data in critical.items():
        if maxim_id != "first_maxim":  # Already showed this one
            print(f"\n{data['text']}")
            print(f"  Latin: {data.get('latin', 'N/A')}")
            print(f"  Importance: {data['importance']}")
            print(f"  Category: {data['category']}")
    
    # Show a random maxim
    print("\n" + "=" * 80)
    print("MAXIM OF THE DAY")
    print("=" * 80)
    
    daily = maxims.get_maxim_of_the_day()
    print(f"\n{daily['text']}")
    print(f"  Latin: {daily.get('latin', 'N/A')}")
    print(f"  Meaning: {daily['meaning'][:100]}...")
    
    print("\n" + "=" * 80)
    print("[+] Legal Maxims Database Loaded")
    print(f"[+] Total Maxims: {len(maxims.get_all_maxims())}")
    print(f"[+] Critical: {len(critical)}")
    print("[+] Wisdom for the vigilant")
    print("=" * 80)
