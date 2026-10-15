"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: family_advocacy.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
OUTCLAW FAMILY ADVOCACY ENGINE

Tools for families of:
- Incarcerated individuals
- Harassed individuals
- Abused individuals
- Intimidated individuals
- Illegally surveilled individuals
- Profiled individuals
- Framed individuals
- Injured individuals

"The hand that rocks the cradle rules the world."
But when the cradle is empty, the world had better watch out.

This module provides specialized legal tools for families to fight back
when their loved ones have been victimized by corrupt officials.

KEY PRINCIPLE: Families have standing. Families have rights. Families have POWER.

When the system targets one, it awakens many.

"""

import json
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"


class FamilyMember:
    """
    Represents a family member who is advocating for a victim.
    
    Family members have legal standing to:
    - File next-friend lawsuits
    - Petition for writs of habeas corpus
    - Demand access to medical records
    - Seek injunctive relief
    - File complaints against officials
    - Request investigations
    - Access public records
    """
    
    RELATIONSHIPS = [
        "spouse", "parent", "child", "sibling", "grandparent",
        "guardian", "next_friend", "power_of_attorney"
    ]
    
    def __init__(self, name: str, relationship: str, contact_info: Dict[str, str],
                 is_legal_guardian: bool = False, has_power_of_attorney: bool = False):
        self.name = name
        self.relationship = relationship
        self.contact_info = contact_info
        self.is_legal_guardian = is_legal_guardian
        self.has_power_of_attorney = has_power_of_attorney
        self.family_member_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique family member ID."""
        import hashlib
        unique_str = f"{self.name}_{self.relationship}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return f"FM_{hashlib.md5(unique_str.encode()).hexdigest()[:8]}"
    
    def has_legal_standing(self) -> bool:
        """Check if this family member has legal standing."""
        return (self.is_legal_guardian or 
                self.has_power_of_attorney or 
                self.relationship in ["spouse", "parent", "child"])
    
    def get_standing_description(self) -> str:
        """Get description of legal standing."""
        if self.is_legal_guardian:
            return "Legal Guardian"
        if self.has_power_of_attorney:
            return "Holds Power of Attorney"
        if self.relationship == "spouse":
            return "Spouse"
        if self.relationship == "parent":
            return "Parent"
        if self.relationship == "child":
            return "Child"
        return f"{self.relationship.capitalize()} (may require additional documentation)"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "family_member_id": self.family_member_id,
            "name": self.name,
            "relationship": self.relationship,
            "contact_info": json.dumps(self.contact_info),
            "is_legal_guardian": int(self.is_legal_guardian),
            "has_power_of_attorney": int(self.has_power_of_attorney)
        }


class Victim:
    """
    Represents the victim that the family is advocating for.
    
    Victim categories:
    - Incarcerated: Wrongfully or unlawfully held
    - Harassed: Subject to ongoing harassment
    - Abused: Physical, emotional, or sexual abuse
    - Intimidated: Threats or coercion
    - Surveilled: Illegal surveillance
    - Profiled: Unlawful profiling
    - Framed: Falsely accused
    - Injured: Physical or psychological harm
    """
    
    VICTIM_CATEGORIES = [
        "incarcerated", "harassed", "abused", "intimidated",
        "surveilled", "profiled", "framed", "injured"
    ]
    
    def __init__(self, name: str, date_of_birth: str, current_location: str,
                 victim_category: str, incident_date: str, 
                 incident_description: str, case_number: Optional[str] = None,
                 facility_name: Optional[str] = None):
        self.name = name
        self.date_of_birth = date_of_birth
        self.current_location = current_location
        self.victim_category = victim_category
        self.incident_date = incident_date
        self.incident_description = incident_description
        self.case_number = case_number
        self.facility_name = facility_name
        self.related_documents: List[str] = []
        self.victim_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique victim ID."""
        import hashlib
        unique_str = f"{self.name}_{self.date_of_birth}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return f"VCT_{hashlib.md5(unique_str.encode()).hexdigest()[:8]}"
    
    def get_category_details(self) -> Dict[str, str]:
        """Get details about the victim category."""
        category_info = {
            "incarcerated": {
                "title": "Incarcerated Individual",
                "description": "Wrongfully or unlawfully held in custody",
                "key_action": "Habeas Corpus Petition"
            },
            "harassed": {
                "title": "Harassed Individual", 
                "description": "Subject to ongoing harassment by officials",
                "key_action": "Restraining Order / Cease and Desist"
            },
            "abused": {
                "title": "Abused Individual",
                "description": "Physical, emotional, or sexual abuse",
                "key_action": "Protective Order / Criminal Complaint"
            },
            "intimidated": {
                "title": "Intimidated Individual",
                "description": "Threats or coercion by officials",
                "key_action": "Injunction / Civil Rights Lawsuit"
            },
            "surveilled": {
                "title": "Illegally Surveilled",
                "description": "Unlawful surveillance or monitoring",
                "key_action": "Privacy Violation Lawsuit / Evidence Suppression"
            },
            "profiled": {
                "title": "Unlawfully Profiled",
                "description": "Racial, religious, or political profiling",
                "key_action": "Discrimination Lawsuit / Policy Challenge"
            },
            "framed": {
                "title": "Framed Individual",
                "description": "Falsely accused or set up",
                "key_action": "Malicious Prosecution / False Arrest Lawsuit"
            },
            "injured": {
                "title": "Injured Individual",
                "description": "Physical or psychological harm",
                "key_action": "Personal Injury Lawsuit / Negligence Claim"
            }
        }
        return category_info.get(self.victim_category, {"title": "Unknown", "description": "", "key_action": ""})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "victim_id": self.victim_id,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "current_location": self.current_location,
            "victim_category": self.victim_category,
            "incident_date": self.incident_date,
            "incident_description": self.incident_description,
            "case_number": self.case_number,
            "facility_name": self.facility_name,
            "related_documents": json.dumps(self.related_documents)
        }


class FamilyAdvocacyCase:
    """
    Represents a complete family advocacy case.
    
    Each case involves:
    - One or more family members advocating
    - One victim they are fighting for
    - Multiple potential legal actions
    - Document collection and tracking
    - Status monitoring
    """
    
    def __init__(self, case_title: str, family_members: List[FamilyMember],
                 victim: Victim, jurisdiction: str, summary: str):
        self.case_title = case_title
        self.family_members = family_members
        self.victim = victim
        self.jurisdiction = jurisdiction
        self.summary = summary
        self.created_date = datetime.now().strftime("%Y-%m-%d")
        self.status = "ACTIVE"
        self.actions_taken: List[Dict[str, Any]] = []
        self.evidence_collected: List[Dict[str, Any]] = []
        self.contacts: List[Dict[str, str]] = []
        self.case_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique case ID."""
        import hashlib
        unique_str = f"{self.case_title}_{self.victim.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return f"FAM_{hashlib.md5(unique_str.encode()).hexdigest()[:8]}"
    
    def add_action(self, action_type: str, action_date: str, description: str,
                  result: Optional[str] = None, documents: Optional[List[str]] = None) -> None:
        """Add an action taken in the case."""
        self.actions_taken.append({
            "action_id": f"{self.case_id}_ACT_{len(self.actions_taken) + 1}",
            "action_type": action_type,
            "action_date": action_date,
            "description": description,
            "result": result,
            "documents": documents or []
        })
    
    def add_evidence(self, evidence_type: str, description: str, source: str,
                    date_obtained: str, location: Optional[str] = None) -> None:
        """Add evidence to the case."""
        self.evidence_collected.append({
            "evidence_id": f"{self.case_id}_EVD_{len(self.evidence_collected) + 1}",
            "evidence_type": evidence_type,
            "description": description,
            "source": source,
            "date_obtained": date_obtained,
            "location": location
        })
    
    def add_contact(self, name: str, title: str, organization: str,
                    phone: str, email: str, notes: Optional[str] = None) -> None:
        """Add a contact to the case."""
        self.contacts.append({
            "contact_id": f"{self.case_id}_CON_{len(self.contacts) + 1}",
            "name": name,
            "title": title,
            "organization": organization,
            "phone": phone,
            "email": email,
            "notes": notes or ""
        })
    
    def get_primary_advocate(self) -> Optional[FamilyMember]:
        """Get the primary family advocate (first with legal standing)."""
        for member in self.family_members:
            if member.has_legal_standing():
                return member
        return self.family_members[0] if self.family_members else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "case_id": self.case_id,
            "case_title": self.case_title,
            "victim_id": self.victim.victim_id,
            "jurisdiction": self.jurisdiction,
            "summary": self.summary,
            "created_date": self.created_date,
            "status": self.status
        }


class FamilyAdvocacyEngine:
    """
    The complete Family Advocacy Engine.
    
    Provides tools for families to fight for their loved ones:
    - Habeas corpus petitions for wrongful incarceration
    - Next-friend lawsuits
    - Complaints against officials
    - Public records requests
    - Evidence collection and preservation
    - Media and public advocacy tools
    
    "When they came for my family, I did not speak out. Then they came for me."
    We make sure they NEVER come for your family.
    """
    
    # Singleton instance
    _instance = None
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    @classmethod
    def get_engine(cls) -> 'FamilyAdvocacyEngine':
        """Get singleton instance of the engine."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _init_db(self) -> None:
        """Initialize database tables for family advocacy."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Victims table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_victims (
                    victim_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    date_of_birth TEXT,
                    current_location TEXT,
                    victim_category TEXT NOT NULL,
                    incident_date TEXT,
                    incident_description TEXT NOT NULL,
                    case_number TEXT,
                    facility_name TEXT,
                    related_documents TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Family members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_family_members (
                    family_member_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    relationship TEXT NOT NULL,
                    contact_info TEXT NOT NULL,
                    is_legal_guardian INTEGER DEFAULT 0,
                    has_power_of_attorney INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Family cases table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_cases (
                    case_id TEXT PRIMARY KEY,
                    case_title TEXT NOT NULL,
                    victim_id TEXT NOT NULL,
                    jurisdiction TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    status TEXT DEFAULT 'ACTIVE',
                    FOREIGN KEY (victim_id) REFERENCES advocacy_victims(victim_id)
                )
            ''')
            
            # Case-family member linkage
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_case_members (
                    case_id TEXT NOT NULL,
                    family_member_id TEXT NOT NULL,
                    PRIMARY KEY (case_id, family_member_id),
                    FOREIGN KEY (case_id) REFERENCES advocacy_cases(case_id),
                    FOREIGN KEY (family_member_id) REFERENCES advocacy_family_members(family_member_id)
                )
            ''')
            
            # Actions taken
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_actions (
                    action_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    action_date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    result TEXT,
                    documents TEXT,
                    FOREIGN KEY (case_id) REFERENCES advocacy_cases(case_id)
                )
            ''')
            
            # Evidence collected
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_evidence (
                    evidence_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    evidence_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    source TEXT NOT NULL,
                    date_obtained TEXT NOT NULL,
                    location TEXT,
                    FOREIGN KEY (case_id) REFERENCES advocacy_cases(case_id)
                )
            ''')
            
            # Contacts
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS advocacy_contacts (
                    contact_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    title TEXT,
                    organization TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    notes TEXT,
                    FOREIGN KEY (case_id) REFERENCES advocacy_cases(case_id)
                )
            ''')
            
            conn.commit()
    
    # =========================================================================
    # VICTIM MANAGEMENT
    # =========================================================================
    
    def register_victim(self, victim: Victim) -> str:
        """Register a victim in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO advocacy_victims 
                (victim_id, name, date_of_birth, current_location, victim_category,
                 incident_date, incident_description, case_number, facility_name, related_documents)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                victim.victim_id,
                victim.name,
                victim.date_of_birth,
                victim.current_location,
                victim.victim_category,
                victim.incident_date,
                victim.incident_description,
                victim.case_number,
                victim.facility_name,
                json.dumps(victim.related_documents)
            ))
            conn.commit()
        return victim.victim_id
    
    def get_victim(self, victim_id: str) -> Optional[Victim]:
        """Retrieve a victim by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT victim_id, name, date_of_birth, current_location, 
                       victim_category, incident_date, incident_description,
                       case_number, facility_name, related_documents
                FROM advocacy_victims WHERE victim_id = ?
            ''', (victim_id,))
            row = cursor.fetchone()
            
            if row:
                victim = Victim(
                    name=row[1],
                    date_of_birth=row[2],
                    current_location=row[3],
                    victim_category=row[4],
                    incident_date=row[5],
                    incident_description=row[6],
                    case_number=row[7],
                    facility_name=row[8]
                )
                victim.victim_id = row[0]
                victim.related_documents = json.loads(row[9]) if row[9] else []
                return victim
        return None
    
    def list_victims(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all victims, optionally filtered by category."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT victim_id, name, victim_category, incident_date, 
                       incident_description, current_location, facility_name
                FROM advocacy_victims
            '''
            params = []
            
            if category:
                query += " WHERE victim_category = ?"
                params.append(category)
            
            query += " ORDER BY incident_date DESC"
            
            cursor.execute(query, params)
            return [
                {
                    "victim_id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "incident_date": row[3],
                    "description": row[4],
                    "location": row[5],
                    "facility": row[6]
                }
                for row in cursor.fetchall()
            ]
    
    # =========================================================================
    # FAMILY MEMBER MANAGEMENT
    # =========================================================================
    
    def register_family_member(self, member: FamilyMember) -> str:
        """Register a family member in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO advocacy_family_members 
                (family_member_id, name, relationship, contact_info, 
                 is_legal_guardian, has_power_of_attorney)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                member.family_member_id,
                member.name,
                member.relationship,
                json.dumps(member.contact_info),
                int(member.is_legal_guardian),
                int(member.has_power_of_attorney)
            ))
            conn.commit()
        return member.family_member_id
    
    def get_family_member(self, member_id: str) -> Optional[FamilyMember]:
        """Retrieve a family member by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT family_member_id, name, relationship, contact_info,
                       is_legal_guardian, has_power_of_attorney
                FROM advocacy_family_members WHERE family_member_id = ?
            ''', (member_id,))
            row = cursor.fetchone()
            
            if row:
                member = FamilyMember(
                    name=row[1],
                    relationship=row[2],
                    contact_info=json.loads(row[3]),
                    is_legal_guardian=bool(row[4]),
                    has_power_of_attorney=bool(row[5])
                )
                member.family_member_id = row[0]
                return member
        return None
    
    def list_family_members(self) -> List[Dict[str, Any]]:
        """List all family members."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT family_member_id, name, relationship, is_legal_guardian,
                       has_power_of_attorney
                FROM advocacy_family_members ORDER BY name
            ''')
            return [
                {
                    "family_member_id": row[0],
                    "name": row[1],
                    "relationship": row[2],
                    "has_legal_standing": bool(row[3] or row[4])
                }
                for row in cursor.fetchall()
            ]
    
    # =========================================================================
    # CASE MANAGEMENT
    # =========================================================================
    
    def create_case(self, case_title: str, family_members: List[FamilyMember],
                    victim: Victim, jurisdiction: str, summary: str) -> FamilyAdvocacyCase:
        """
        Create a new family advocacy case.
        
        Args:
            case_title: Short title for the case
            family_members: List of FamilyMember objects advocating
            victim: The Victim being advocated for
            jurisdiction: Jurisdiction (state, county, etc.)
            summary: Brief description of the case
            
        Returns:
            New FamilyAdvocacyCase object
        """
        case_obj = FamilyAdvocacyCase(
            case_title=case_title,
            family_members=family_members,
            victim=victim,
            jurisdiction=jurisdiction,
            summary=summary
        )
        
        # Save to database
        self._save_case(case_obj)
        
        return case_obj
    
    def _save_case(self, case_obj: FamilyAdvocacyCase) -> None:
        """Save a case to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save victim
            self.register_victim(case_obj.victim)
            
            # Save family members
            for member in case_obj.family_members:
                self.register_family_member(member)
            
            # Save case
            cursor.execute('''
                INSERT OR REPLACE INTO advocacy_cases 
                (case_id, case_title, victim_id, jurisdiction, summary, 
                 created_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                case_obj.case_id,
                case_obj.case_title,
                case_obj.victim.victim_id,
                case_obj.jurisdiction,
                case_obj.summary,
                case_obj.created_date,
                case_obj.status
            ))
            
            # Link family members to case
            for member in case_obj.family_members:
                cursor.execute('''
                    INSERT OR REPLACE INTO advocacy_case_members 
                    (case_id, family_member_id)
                    VALUES (?, ?)
                ''', (case_obj.case_id, member.family_member_id))
            
            # Save actions
            for action in case_obj.actions_taken:
                cursor.execute('''
                    INSERT OR REPLACE INTO advocacy_actions 
                    (action_id, case_id, action_type, action_date, description, 
                     result, documents)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    action["action_id"],
                    case_obj.case_id,
                    action["action_type"],
                    action["action_date"],
                    action["description"],
                    action.get("result"),
                    json.dumps(action.get("documents", []))
                ))
            
            # Save evidence
            for evidence in case_obj.evidence_collected:
                cursor.execute('''
                    INSERT OR REPLACE INTO advocacy_evidence 
                    (evidence_id, case_id, evidence_type, description, source, 
                     date_obtained, location)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    evidence["evidence_id"],
                    case_obj.case_id,
                    evidence["evidence_type"],
                    evidence["description"],
                    evidence["source"],
                    evidence["date_obtained"],
                    evidence.get("location")
                ))
            
            # Save contacts
            for contact in case_obj.contacts:
                cursor.execute('''
                    INSERT OR REPLACE INTO advocacy_contacts 
                    (contact_id, case_id, name, title, organization, phone, 
                     email, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    contact["contact_id"],
                    case_obj.case_id,
                    contact["name"],
                    contact.get("title"),
                    contact["organization"],
                    contact.get("phone"),
                    contact.get("email"),
                    contact.get("notes", "")
                ))
            
            conn.commit()
    
    def get_case(self, case_id: str) -> Optional[FamilyAdvocacyCase]:
        """Retrieve a case by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT case_id, case_title, victim_id, jurisdiction, summary,
                       created_date, status
                FROM advocacy_cases WHERE case_id = ?
            ''', (case_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Get victim
            victim = self.get_victim(row[2])
            if not victim:
                return None
            
            # Get family members
            cursor.execute('''
                SELECT family_member_id FROM advocacy_case_members 
                WHERE case_id = ?
            ''', (case_id,))
            
            family_members = []
            for member_row in cursor.fetchall():
                member = self.get_family_member(member_row[0])
                if member:
                    family_members.append(member)
            
            case_obj = FamilyAdvocacyCase(
                case_title=row[1],
                family_members=family_members,
                victim=victim,
                jurisdiction=row[3],
                summary=row[4]
            )
            case_obj.case_id = row[0]
            case_obj.created_date = row[5]
            case_obj.status = row[6]
            
            # Load actions
            cursor.execute('''
                SELECT action_id, action_type, action_date, description, result, documents
                FROM advocacy_actions WHERE case_id = ? ORDER BY action_date
            ''', (case_id,))
            for action_row in cursor.fetchall():
                case_obj.actions_taken.append({
                    "action_id": action_row[0],
                    "action_type": action_row[1],
                    "action_date": action_row[2],
                    "description": action_row[3],
                    "result": action_row[4],
                    "documents": json.loads(action_row[5]) if action_row[5] else []
                })
            
            # Load evidence
            cursor.execute('''
                SELECT evidence_id, evidence_type, description, source, 
                       date_obtained, location
                FROM advocacy_evidence WHERE case_id = ? ORDER BY date_obtained
            ''', (case_id,))
            for evidence_row in cursor.fetchall():
                case_obj.evidence_collected.append({
                    "evidence_id": evidence_row[0],
                    "evidence_type": evidence_row[1],
                    "description": evidence_row[2],
                    "source": evidence_row[3],
                    "date_obtained": evidence_row[4],
                    "location": evidence_row[5]
                })
            
            # Load contacts
            cursor.execute('''
                SELECT contact_id, name, title, organization, phone, email, notes
                FROM advocacy_contacts WHERE case_id = ? ORDER BY name
            ''', (case_id,))
            for contact_row in cursor.fetchall():
                case_obj.contacts.append({
                    "contact_id": contact_row[0],
                    "name": contact_row[1],
                    "title": contact_row[2],
                    "organization": contact_row[3],
                    "phone": contact_row[4],
                    "email": contact_row[5],
                    "notes": contact_row[6]
                })
            
            return case_obj
    
    def list_cases(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all cases, optionally filtered by status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT c.case_id, c.case_title, c.jurisdiction, c.created_date, 
                       c.status, v.name, v.victim_category
                FROM advocacy_cases c
                JOIN advocacy_victims v ON c.victim_id = v.victim_id
            '''
            params = []
            
            if status:
                query += " WHERE c.status = ?"
                params.append(status)
            
            query += " ORDER BY c.created_date DESC"
            
            cursor.execute(query, params)
            return [
                {
                    "case_id": row[0],
                    "case_title": row[1],
                    "jurisdiction": row[2],
                    "created_date": row[3],
                    "status": row[4],
                    "victim_name": row[5],
                    "victim_category": row[6]
                }
                for row in cursor.fetchall()
            ]
    
    def close_case(self, case_id: str, resolution: str) -> bool:
        """Close a case with a resolution."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE advocacy_cases SET status = ?, summary = ?
                WHERE case_id = ?
            ''', ("CLOSED", f"{resolution} - Closed {datetime.now().strftime('%Y-%m-%d')}", case_id))
            conn.commit()
            return cursor.rowcount > 0
    
    # =========================================================================
    # DOCUMENT GENERATION
    # =========================================================================
    
    def generate_habeas_corpus_petition(self, case_obj: FamilyAdvocacyCase,
                                        court_name: str) -> str:
        """
        Generate a Habeas Corpus petition for wrongful incarceration.
        
        Habeas Corpus ("produce the body") is the fundamental right to
        challenge unlawful detention.
        """
        primary = case_obj.get_primary_advocate()
        if not primary:
            return "ERROR: No family member with legal standing found"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        document = f"""PETITION FOR WRIT OF HABEAS CORPUS

IN THE [DISTRICT/SUPERIOR] COURT OF {court_name}

{primary.name},
    Petitioner,
    
    vs.
    
[WARDEN/JAILER NAME],
    in their official capacity as [TITLE],
    
    and
    
[AGENCY NAME],
    Respondent.

)  CASE NO.: [TO BE ASSIGNED]

PETITION FOR WRIT OF HABEAS CORPUS

TO THE HONORABLE COURT:

Comes now {primary.name}, {primary.relationship} of {case_obj.victim.name},
and respectfully petitions this Honorable Court for a Writ of Habeas Corpus
on behalf of {case_obj.victim.name}, and in support states as follows:

1. PETITIONER'S INTEREST
   
   Petitioner is the {primary.relationship} of {case_obj.victim.name}.
   {primary.get_standing_description()}.
   Petitioner has a direct and substantial interest in the welfare and
   freedom of {case_obj.victim.name}.

2. DETENTION INFORMATION
   
   {case_obj.victim.name} is currently detained at: {case_obj.victim.current_location}
   Facility: {case_obj.victim.facility_name or 'Unknown'}
   Case/Booking Number: {case_obj.victim.case_number or 'Unknown'}

3. GROUNDS FOR HABEAS CORPUS
   
   The detention of {case_obj.victim.name} is unlawful because:
   
   {case_obj.victim.incident_description}

4. EXHAUSTION OF REMEDIES
   
   [List any appeals, grievances, or other remedies that have been pursued]
   
   OR
   
   No adequate remedy exists at law because [EXPLAIN]

5. REQUEST FOR RELIEF
   
   WHEREFORE, Petitioner respectfully requests that this Honorable Court:
   
   1. Issue a Writ of Habeas Corpus directing Respondent to produce
      {case_obj.victim.name} before this Court;
   2. Order the immediate release of {case_obj.victim.name} from unlawful
      detention;
   3. Declare the detention of {case_obj.victim.name} to be unlawful and
      in violation of [SPECIFIC LAWS];
   4. Award such other and further relief as the Court deems just and proper.

I declare under penalty of perjury that the foregoing is true and correct
to the best of my knowledge and belief.

Respectfully submitted,

DATED: {today}

_________________________
{primary.name}
Petitioner

VERIFICATION

I, {primary.name}, declare under penalty of perjury that I am the
{primary.relationship} of {case_obj.victim.name}, that I have personal
knowledge of the facts stated herein, and that the foregoing is true
and correct.

DATED: {today}

_________________________
{primary.name}
"""
        return document
    
    def generate_next_friend_complaint(self, case_obj: FamilyAdvocacyCase,
                                         defendant: str, defendant_title: str) -> str:
        """
        Generate a Next Friend complaint.
        
        A "next friend" is someone who acts on behalf of another who cannot
        act for themselves (incapacitated, minor, or otherwise unable).
        """
        primary = case_obj.get_primary_advocate()
        if not primary:
            return "ERROR: No family member with legal standing found"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        category_info = case_obj.victim.get_category_details()
        
        document = f"""COMPLAINT - NEXT FRIEND ACTION

IN THE [DISTRICT] COURT OF {case_obj.jurisdiction}

{primary.name},
    as Next Friend of {case_obj.victim.name},
    Plaintiff,
    
    vs.
    
{defendant},
{defendant_title},
    Defendant.

)  CASE NO.: [TO BE ASSIGNED]

COMPLAINT FOR [VIOLATION OF RIGHTS]

JURISDICTION AND VENUE

1. This Court has jurisdiction over this matter pursuant to [STATUTE].
2. Venue is proper in this district because the events giving rise to this
   action occurred in {case_obj.jurisdiction}.

PARTIES

3. Plaintiff {primary.name} is the {primary.relationship} of {case_obj.victim.name}
   and acts as Next Friend on behalf of {case_obj.victim.name} who is
   {case_obj.victim.get_category_details()['description'].lower()}.

4. {primary.get_standing_description()}.

5. Defendant {defendant} is [DESCRIBE DEFENDANT'S ROLE].

FACTUAL ALLEGATIONS

6. {case_obj.victim.name} (DOB: {case_obj.victim.date_of_birth}) was
   {case_obj.victim.get_category_details()['description'].lower()} on
   or about {case_obj.victim.incident_date}.

7. The incident occurred as follows: {case_obj.victim.incident_description}

CAUSES OF ACTION

8. COUNT I: [PRIMARY CAUSE OF ACTION - e.g., Violation of 42 U.S.C. § 1983]
   
   Defendant, acting under color of state law, deprived {case_obj.victim.name}
   of rights secured by the Constitution and laws of the United States,
   including but not limited to:
   
   [LIST SPECIFIC RIGHTS VIOLATED]

9. COUNT II: [SECOND CAUSE OF ACTION - e.g., False Imprisonment]
   
   Defendant intentionally and unlawfully restrained {case_obj.victim.name}
   of their liberty without legal justification.

10. COUNT III: [THIRD CAUSE OF ACTION - e.g., Intentional Infliction of Emotional Distress]
    
    Defendant's conduct was so outrageous in character, and so extreme in
degree, as to go beyond all possible bounds of decency, and to be regarded
as atrocious and utterly intolerable in a civilized community.

DAMAGES

11. As a direct and proximate result of Defendant's actions, {case_obj.victim.name}
    has suffered:
    
    a. Physical injuries: [DESCRIBE]
    b. Emotional distress: [DESCRIBE]
    c. Economic damages: [DESCRIBE]
    d. Damage to reputation: [DESCRIBE]
    e. Loss of liberty and enjoyment of life: [DESCRIBE]

12. Plaintiff {primary.name}, as Next Friend, has also suffered emotional
distress and damage to familial relationships.

JURY DEMAND

13. Plaintiff demands a trial by jury on all issues so triable.

PRAYER FOR RELIEF

WHEREFORE, Plaintiff respectfully requests that this Honorable Court:

1. Enter judgment in favor of Plaintiff and against Defendant;
2. Award compensatory damages in an amount to be proven at trial;
3. Award punitive damages in an amount sufficient to punish and deter
   Defendant's conduct;
4. Award injunctive relief as appropriate;
5. Award costs of suit and reasonable attorney's fees;
6. Grant such other and further relief as the Court deems just and proper.

I declare under penalty of perjury that the foregoing is true and correct
to the best of my knowledge and belief.

Respectfully submitted,

DATED: {today}

_________________________
{primary.name}
Next Friend of {case_obj.victim.name}
"""
        return document
    
    def generate_public_records_request(self, case_obj: FamilyAdvocacyCase,
                                          agency: str, records_description: str) -> str:
        """
        Generate a public records request under FOIA or state equivalent.
        
        Families have a right to access public records related to their
        loved ones' cases.
        """
        primary = case_obj.get_primary_advocate()
        if not primary:
            return "ERROR: No family member with legal standing found"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        document = f"""PUBLIC RECORDS REQUEST

[today]

{agency}
[AGENCY ADDRESS]

Attention: Records Custodian / FOIA Officer

Re: Public Records Request - {case_obj.case_title}

To Whom It May Concern:

Pursuant to the [FREEDOM OF INFORMATION ACT / STATE PUBLIC RECORDS ACT],
I, {primary.name}, {primary.relationship} of {case_obj.victim.name}, hereby
request access to and copies of the following public records:

{records_description}

These records are requested in connection with the following matter:

{case_obj.summary}

{case_obj.victim.name} (DOB: {case_obj.victim.date_of_birth}) was
{case_obj.victim.get_category_details()['description'].lower()} on
{case_obj.victim.incident_date} at {case_obj.victim.current_location}.

SPECIFIC RECORDS REQUESTED:

1. All incident reports related to {case_obj.victim.name}
2. All arrest reports and booking information
3. All video/audio recordings from the date of incident
4. All witness statements
5. All medical records in the possession of the agency
6. All internal investigations or reviews
7. All communications between agency personnel regarding this matter
8. All policies and procedures relevant to the incident
9. [ANY OTHER SPECIFIC RECORDS]

FEES

I request a fee waiver pursuant to [STATUTE] because this request is made
in the public interest and not for commercial purposes. The information
sought will contribute significantly to public understanding of government
operations and activities.

If a fee waiver is denied, please notify me of the estimated costs before
processing this request.

FORMAT

Please provide records in electronic format if available. If electronic
format is not available, please provide paper copies.

RESPONSE TIME

Pursuant to [STATUTE], please provide these records within the statutory
timeframe of [X] business days. If you cannot comply within this timeframe,
please notify me in writing of the reason for the delay and the date by
which the records will be provided.

CONTACT INFORMATION

{primary.name}
{primary.contact_info.get('address', '[ADDRESS]')}
{primary.contact_info.get('city', '[CITY]')}, {primary.contact_info.get('state', '[STATE]')} {primary.contact_info.get('zip', '[ZIP]')}
{primary.contact_info.get('phone', '[PHONE]')}
{primary.contact_info.get('email', '[EMAIL]')}

I declare under penalty of perjury that I am the person I claim to be and
that this request is made in good faith.

Sincerely,

_________________________
{primary.name}
{primary.relationship} of {case_obj.victim.name}

[ENCLOSURES: Copy of ID, Proof of Relationship if required]
"""
        return document
    
    def generate_cease_and_desist_letter(self, case_obj: FamilyAdvocacyCase,
                                          target: str, target_title: str,
                                          harmful_actions: List[str]) -> str:
        """
        Generate a cease and desist letter for harassment or other ongoing harm.
        """
        primary = case_obj.get_primary_advocate()
        if not primary:
            return "ERROR: No family member with legal standing found"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        actions_list = "\n".join([f"  {i+1}. {action}" for i, action in enumerate(harmful_actions)])
        
        document = f"""CEASE AND DESIST LETTER

[today]

VIA CERTIFIED MAIL - RETURN RECEIPT REQUESTED
VIA EMAIL: [EMAIL ADDRESS]

{target}
{target_title}
[AGENCY/ORGANIZATION]
[ADDRESS]

Re: Cease and Desist Demand - {case_obj.case_title}

{target}:

I, {primary.name}, {primary.relationship} of {case_obj.victim.name}, am
writing to formally demand that you IMMEDIATELY CEASE AND DESIST from all
harmful, harassing, or unlawful actions directed at {case_obj.victim.name}
and our family.

BACKGROUND

{case_obj.victim.name} (DOB: {case_obj.victim.date_of_birth}) is the victim of
{case_obj.victim.get_category_details()['description'].lower()} that occurred on
or about {case_obj.victim.incident_date}. The incident is described as follows:

{case_obj.victim.incident_description}

SPECIFIC ACTIONS TO CEASE

The following actions must cease immediately:

{actions_list}

LEGAL BASIS

Your actions violate:
- [SPECIFIC STATUTES - e.g., 42 U.S.C. § 1983, 18 U.S.C. § 241, etc.]
- [STATE LAWS]
- Constitutional rights to [LIST RIGHTS]
- [AGENCY POLICIES AND PROCEDURES]

DEMAND

I demand that you and all persons acting under your direction or control:

1. IMMEDIATELY CEASE all harassing, retaliatory, or harmful actions against
   {case_obj.victim.name} and all family members;
2. REFRAIN from any further contact with {case_obj.victim.name} or family
   members except through legal counsel;
3. PRESERVE all evidence related to this matter, including but not limited
   to records, communications, and other documentation;
4. PROVIDE written confirmation within FIVE (5) DAYS of receipt of this
   letter that you have complied with this demand.

WARNING

Be advised that if you fail to comply with this demand, I will pursue all
available legal remedies, including but not limited to:

- Filing criminal complaints for harassment, stalking, or other offenses
- Filing civil lawsuits for damages
- Seeking restraining orders and injunctive relief
- Reporting your conduct to oversight bodies and licensing authorities
- Public disclosure of your actions

This letter serves as formal notice and creates a record of your knowledge
of these demands. Your continued actions after receipt of this notice will
be considered willful and intentional, subjecting you to enhanced damages
and penalties.

Please govern yourself accordingly.

Sincerely,

_________________________
{primary.name}
{primary.relationship} of {case_obj.victim.name}

CC: [List of other recipients]
[Attorney if applicable]
[Oversight bodies]
"""
        return document
    
    def generate_media_press_release(self, case_obj: FamilyAdvocacyCase,
                                     headline: str) -> str:
        """
        Generate a press release to bring public attention to the case.
        
        Public pressure is a powerful tool for accountability.
        """
        primary = case_obj.get_primary_advocate()
        if not primary:
            return "ERROR: No family member with legal standing found"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        category_info = case_obj.victim.get_category_details()
        
        document = f"""FOR IMMEDIATE RELEASE

{headline}

{case_obj.jurisdiction} - {today}

FAMILY DEMANDS JUSTICE FOR {case_obj.victim.name.upper()}

{case_obj.jurisdiction} - The family of {case_obj.victim.name}, a
{case_obj.victim.date_of_birth} year-old [RACE/ETHNICITY IF RELEVANT] who was
{case_obj.victim.get_category_details()['description'].lower()}, is speaking out
demanding accountability and justice.

According to family spokesperson {primary.name}, {case_obj.victim.name}
was {case_obj.victim.get_category_details()['description'].lower()} on
{case_obj.victim.incident_date} at {case_obj.victim.current_location}.

"{case_obj.summary}" said {primary.name}.

DESCRIPTION OF INCIDENT:

{case_obj.victim.incident_description}

FAMILY DEMANDS:

The family is demanding:

1. Immediate [RELEASE/INVESTIGATION/OTHER ACTION] for {case_obj.victim.name}
2. Full transparency and accountability from all involved agencies
3. Independent investigation into the incident
4. Disciplinary action against those responsible
5. Compensation for the harm caused to {case_obj.victim.name} and the family

BACKGROUND:

{case_obj.victim.name} is a [BRIEF DESCRIPTION - e.g., "loving father of three," "hardworking community member," etc.].
[ADDITIONAL RELEVANT INFORMATION ABOUT THE VICTIM]

The incident has caused immense suffering for {case_obj.victim.name} and
their family, including [DESCRIBE IMPACT].

LEGAL ACTION:

The family has retained [OR: is seeking] legal counsel and is exploring
all available legal remedies, including [LIST POTENTIAL ACTIONS].

A [PETITION/FUNDRAISER/PUBLIC RECORDS REQUEST] has been initiated at
[LINK IF APPLICABLE].

MEDIA CONTACT:

{primary.name}
{primary.relationship} of {case_obj.victim.name}
{primary.contact_info.get('phone', '[PHONE]')}
{primary.contact_info.get('email', '[EMAIL]')}

###

ABOUT {case_obj.case_title}:

This case represents a broader pattern of [DESCRIBE SYSTEMIC ISSUE] in
{case_obj.jurisdiction}. The family of {case_obj.victim.name} is determined
to seek justice not only for their loved one, but for all victims of
similar abuses.

- END -

For more information, please contact {primary.name} at
{primary.contact_info.get('phone', '[PHONE]')} or
{primary.contact_info.get('email', '[EMAIL]')}.
"""
        return document


# =============================================================================
# SINGLETON ACCESSOR
# =============================================================================

def get_family_advocacy_engine() -> FamilyAdvocacyEngine:
    """Get the singleton instance of the Family Advocacy Engine."""
    return FamilyAdvocacyEngine.get_engine()


# =============================================================================
# QUICK START EXAMPLE
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("FAMILY ADVOCACY ENGINE - STANDALONE TEST")
    print("=" * 80)
    
    # Initialize engine
    engine = get_family_advocacy_engine()
    
    # Create a victim
    victim = Victim(
        name="Robert Hollis Talbert",
        date_of_birth="2010-07-08",
        current_location="Unknown Facility, Oklahoma",
        victim_category="framed",
        incident_date="2020-12-21",
        incident_description="Robert was taken from his family by government officials under false pretenses. The family has evidence of systemic child trafficking networks involved in his disappearance.",
        case_number="OK-2020-XXXX",
        facility_name="Unknown State Facility"
    )
    victim_id = engine.register_victim(victim)
    print(f"\n[+] Registered Victim: {victim.name} (ID: {victim_id})")
    
    # Create family member
    mother = FamilyMember(
        name="Sarah Talbert",
        relationship="mother",
        contact_info={
            "address": "[PROTECTED]",
            "city": "[PROTECTED]",
            "state": "OK",
            "zip": "[PROTECTED]",
            "phone": "[PROTECTED]",
            "email": "[PROTECTED]"
        },
        is_legal_guardian=True
    )
    mother_id = engine.register_family_member(mother)
    print(f"[+] Registered Family Member: {mother.name} (ID: {mother_id})")
    
    # Create case
    case_obj = engine.create_case(
        case_title="Talbert Family v. Oklahoma - Child Trafficking Investigation",
        family_members=[mother],
        victim=victim,
        jurisdiction="Oklahoma",
        summary="Investigation into the wrongful removal and trafficking of Robert Hollis Talbert and other children by government officials."
    )
    
    print(f"\n[+] Created Case: {case_obj.case_id}")
    print(f"[+] Case Title: {case_obj.case_title}")
    print(f"[+] Victim: {case_obj.victim.name}")
    print(f"[+] Primary Advocate: {case_obj.get_primary_advocate().name}")
    
    # Generate and display a document
    print("\n" + "=" * 80)
    print("SAMPLE PUBLIC RECORDS REQUEST")
    print("=" * 80)
    
    records_request = engine.generate_public_records_request(
        case_obj=case_obj,
        agency="Oklahoma Department of Human Services",
        records_description="All records related to the removal, placement, and current location of Robert Hollis Talbert (DOB: 2010-07-08)"
    )
    print(records_request[:2000] + "\n... [TRUNCATED]")
    
    # Show case info
    print("\n" + "=" * 80)
    print("CASE INFORMATION")
    print("=" * 80)
    print(f"Case ID: {case_obj.case_id}")
    print(f"Title: {case_obj.case_title}")
    print(f"Jurisdiction: {case_obj.jurisdiction}")
    print(f"Status: {case_obj.status}")
    print(f"Victim: {case_obj.victim.name} ({case_obj.victim.victim_category})")
    print(f"Primary Advocate: {mother.name} ({mother.get_standing_description()})")
    
    # List victim categories
    print("\n" + "=" * 80)
    print("SUPPORTED VICTIM CATEGORIES")
    print("=" * 80)
    for category in Victim.VICTIM_CATEGORIES:
        info = victim.get_category_details() if hasattr(victim, 'get_category_details') else {"title": category, "description": "", "key_action": ""}
        print(f"  - {category}: {info.get('title', category)}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
