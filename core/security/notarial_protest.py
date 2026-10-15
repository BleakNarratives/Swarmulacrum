"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: notarial_protest.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
OUTCLAW NOTARIAL PROTEST ENGINE

The Mail-Based Court System - Holding Court Through the Mail

KEY INSIGHT: A Notary Public is a deputized Secretary of State with equal or greater
authority than a ministerial judge. When notarizing court documents, the notary acts
as an officer of the Court. Judges in administrative capacity are merely clerks
of the executive branch - selected by local attorneys, never truly elected.

THE THREE-LETTER NUCLEAR OPTION:
1. Notice of Intent - First class mail, return receipt requested
2. Notice and Opportunity - Sworn under penalty of perjury, clear claim of harm
3. Final Notice - With proper time served (typically 10-30 days per notice)

After THREE non-responses, tacit admission through silence is established.
You can then appear and request a declaratory judgment.

The entire case can be won with a few stamps and the help of a notary.

"He who does not deny, admits." - Legal Maxim
"Silence is consent." - Tacit Admission Doctrine

"""

import json
import sqlite3
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

DB_PATH = "/storage/emulated/0/RootBase/OutClaw/case_matrix.db"


class NotaryAuthority:
    """
    Represents the authority of a Notary Public as a deputized Secretary of State.
    
    A notary has the authority to:
    - Administer oaths and affirmations
    - Take acknowledgments and proofs
    - Certify copies of documents
    - Act as an officer of the court when notarizing court documents
    - Create a court of record through proper documentation
    
    This authority is superior to administrative judges who act as mere clerks
    of the executive branch.
    """
    
    def __init__(self, notary_name: str, commission_number: str, state: str, 
                 commission_expiry: str, county: str):
        self.notary_name = notary_name
        self.commission_number = commission_number
        self.state = state
        self.commission_expiry = commission_expiry
        self.county = county
        self.authority_seal = f"Notary Public, {state} - Commission #{commission_number}"
    
    def get_authority_statement(self) -> str:
        """Generate formal authority statement for documents."""
        return (
            f"I, {self.notary_name}, Notary Public in and for the County of {self.county}, "
            f"State of {self.state}, duly commissioned and sworn, with Commission "
            f"#{self.commission_number} expiring {self.commission_expiry}, do hereby "
            f"certify that I am a deputized officer of the Secretary of State and an "
            f"officer of the Court, acting in my official capacity."
        )
    
    def get_seal(self) -> str:
        """Generate the notarial seal statement."""
        return self.authority_seal
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for storage."""
        return {
            "notary_name": self.notary_name,
            "commission_number": self.commission_number,
            "state": self.state,
            "commission_expiry": self.commission_expiry,
            "county": self.county
        }


class Notice:
    """
    Represents a single notice in the notarial protest sequence.
    
    Each notice must be:
    - Sent via First Class Mail with Return Receipt Requested (Certified)
    - Sworn under the pains and penalties of perjury
    - Include a clear claim of harm, damage, injury, or loss
    - Provide proper notice and opportunity to respond
    """
    
    NOTICE_TYPES = [
        "notice_of_intent",
        "notice_and_opportunity", 
        "final_notice_before_action"
    ]
    
    def __init__(self, notice_id: str, sequence_id: str, notice_type: str,
                 sender: str, recipient: str, recipient_title: str,
                 claims: List[str], harm_description: str,
                 response_deadline_days: int = 10,
                 mail_tracking_number: Optional[str] = None,
                 sent_date: Optional[str] = None,
                 return_receipt_received: bool = False,
                 response_received: bool = False):
        
        self.notice_id = notice_id
        self.sequence_id = sequence_id
        self.notice_type = notice_type
        self.sender = sender
        self.recipient = recipient
        self.recipient_title = recipient_title
        self.claims = claims
        self.harm_description = harm_description
        self.response_deadline_days = response_deadline_days
        self.mail_tracking_number = mail_tracking_number
        self.sent_date = sent_date or datetime.now().strftime("%Y-%m-%d")
        self.return_receipt_received = return_receipt_received
        self.response_received = response_received
        
        # Calculate deadline
        self.deadline_date = self._calculate_deadline()
    
    def _calculate_deadline(self) -> str:
        """Calculate the response deadline based on sent date."""
        sent = datetime.strptime(self.sent_date, "%Y-%m-%d")
        deadline = sent + timedelta(days=self.response_deadline_days)
        return deadline.strftime("%Y-%m-%d")
    
    def is_overdue(self) -> bool:
        """Check if the notice response period has expired."""
        deadline = datetime.strptime(self.deadline_date, "%Y-%m-%d")
        return datetime.now() > deadline
    
    def is_non_response(self) -> bool:
        """Check if this constitutes a non-response (overdue and no response)."""
        return self.is_overdue() and not self.response_received
    
    def mark_sent(self, tracking_number: str) -> None:
        """Mark notice as sent with tracking number."""
        self.mail_tracking_number = tracking_number
        self.sent_date = datetime.now().strftime("%Y-%m-%d")
        self.deadline_date = self._calculate_deadline()
    
    def mark_response_received(self, response_text: str) -> None:
        """Mark that a response was received."""
        self.response_received = True
        self.response_text = response_text
        self.response_date = datetime.now().strftime("%Y-%m-%d")
    
    def mark_return_receipt_received(self, receipt_date: str) -> None:
        """Mark that return receipt was received."""
        self.return_receipt_received = True
        self.receipt_date = receipt_date
    
    def get_status(self) -> str:
        """Get current status of the notice."""
        if self.response_received:
            return "RESPONDED"
        elif self.is_overdue():
            return "NON_RESPONSE"
        elif self.mail_tracking_number:
            return "SENT"
        else:
            return "DRAFT"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "notice_id": self.notice_id,
            "sequence_id": self.sequence_id,
            "notice_type": self.notice_type,
            "sender": self.sender,
            "recipient": self.recipient,
            "recipient_title": self.recipient_title,
            "claims": json.dumps(self.claims),
            "harm_description": self.harm_description,
            "response_deadline_days": self.response_deadline_days,
            "mail_tracking_number": self.mail_tracking_number,
            "sent_date": self.sent_date,
            "deadline_date": self.deadline_date,
            "return_receipt_received": int(self.return_receipt_received),
            "response_received": int(self.response_received),
            "status": self.get_status()
        }


class ProtestSequence:
    """
    Manages a complete three-notice protest sequence.
    
    After THREE non-responses to properly served notices, tacit admission
    through silence is established. The sender can then:
    - Appear in court
    - Request declaratory judgment
    - Win the case by default
    
    This is the mail-based court system in action.
    """
    
    def __init__(self, sequence_id: str, sender: str, recipient: str, 
                 recipient_title: str, case_title: str, harm_description: str,
                 claims: List[str], notary: Optional[NotaryAuthority] = None):
        
        self.sequence_id = sequence_id
        self.sender = sender
        self.recipient = recipient
        self.recipient_title = recipient_title
        self.case_title = case_title
        self.harm_description = harm_description
        self.claims = claims
        self.notary = notary
        self.notices: List[Notice] = []
        self.created_date = datetime.now().strftime("%Y-%m-%d")
        self.completed = False
        self.tacit_admission_established = False
    
    def create_notice_of_intent(self) -> Notice:
        """Create the first notice: Notice of Intent."""
        notice_id = f"{self.sequence_id}_notice_01"
        notice = Notice(
            notice_id=notice_id,
            sequence_id=self.sequence_id,
            notice_type="notice_of_intent",
            sender=self.sender,
            recipient=self.recipient,
            recipient_title=self.recipient_title,
            claims=self.claims,
            harm_description=self.harm_description,
            response_deadline_days=10
        )
        self.notices.append(notice)
        return notice
    
    def create_notice_and_opportunity(self) -> Notice:
        """Create the second notice: Notice and Opportunity."""
        notice_id = f"{self.sequence_id}_notice_02"
        notice = Notice(
            notice_id=notice_id,
            sequence_id=self.sequence_id,
            notice_type="notice_and_opportunity",
            sender=self.sender,
            recipient=self.recipient,
            recipient_title=self.recipient_title,
            claims=self.claims,
            harm_description=self.harm_description,
            response_deadline_days=10
        )
        self.notices.append(notice)
        return notice
    
    def create_final_notice(self) -> Notice:
        """Create the third notice: Final Notice Before Action."""
        notice_id = f"{self.sequence_id}_notice_03"
        notice = Notice(
            notice_id=notice_id,
            sequence_id=self.sequence_id,
            notice_type="final_notice_before_action",
            sender=self.sender,
            recipient=self.recipient,
            recipient_title=self.recipient_title,
            claims=self.claims,
            harm_description=self.harm_description,
            response_deadline_days=10
        )
        self.notices.append(notice)
        return notice
    
    def get_notice_count(self) -> int:
        """Get total number of notices in sequence."""
        return len(self.notices)
    
    def get_non_response_count(self) -> int:
        """Count how many notices have resulted in non-response."""
        return sum(1 for n in self.notices if n.is_non_response())
    
    def check_tacit_admission(self) -> bool:
        """
        Check if tacit admission through silence has been established.
        
        Requires THREE properly served notices with non-responses.
        """
        if len(self.notices) < 3:
            return False
        
        non_responses = sum(1 for n in self.notices 
                          if n.is_non_response() and n.return_receipt_received)
        
        self.tacit_admission_established = non_responses >= 3
        return self.tacit_admission_established
    
    def can_request_declaratory_judgment(self) -> bool:
        """Check if conditions are met for declaratory judgment."""
        return self.check_tacit_admission() and self.notary is not None
    
    def get_next_notice_type(self) -> Optional[str]:
        """Get the type of the next notice to create."""
        if len(self.notices) == 0:
            return "notice_of_intent"
        elif len(self.notices) == 1:
            return "notice_and_opportunity"
        elif len(self.notices) == 2:
            return "final_notice_before_action"
        else:
            return None
    
    def is_complete(self) -> bool:
        """Check if the sequence is complete (all notices sent)."""
        return len(self.notices) >= 3 and all(n.mail_tracking_number for n in self.notices)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "sequence_id": self.sequence_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "recipient_title": self.recipient_title,
            "case_title": self.case_title,
            "harm_description": self.harm_description,
            "claims": json.dumps(self.claims),
            "notary": json.dumps(self.notary.to_dict()) if self.notary else None,
            "created_date": self.created_date,
            "completed": int(self.completed),
            "tacit_admission_established": int(self.tacit_admission_established)
        }


class NotarialProtestEngine:
    """
    The complete Notarial Protest Engine.
    
    Implements the mail-based court system where:
    1. Notary acts as officer of the court
    2. Three notices create a court of record
    3. Silence = tacit admission
    4. Non-response = default victory
    
    This is the ultimate tool for self-represented litigants to force
    corrupt officials into court without traditional process.
    """
    
    # Singleton instance
    _instance = None
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()
    
    @classmethod
    def get_engine(cls) -> 'NotarialProtestEngine':
        """Get singleton instance of the engine."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _init_db(self) -> None:
        """Initialize database tables for notarial protest tracking."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Notary authorities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notary_authorities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    notary_name TEXT NOT NULL,
                    commission_number TEXT NOT NULL,
                    state TEXT NOT NULL,
                    county TEXT NOT NULL,
                    commission_expiry TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(notary_name, commission_number, state)
                )
            ''')
            
            # Protest sequences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS protest_sequences (
                    sequence_id TEXT PRIMARY KEY,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    recipient_title TEXT,
                    case_title TEXT NOT NULL,
                    harm_description TEXT NOT NULL,
                    claims TEXT NOT NULL,
                    notary_id INTEGER,
                    created_date TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    tacit_admission_established INTEGER DEFAULT 0,
                    FOREIGN KEY (notary_id) REFERENCES notary_authorities(id)
                )
            ''')
            
            # Individual notices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notices (
                    notice_id TEXT PRIMARY KEY,
                    sequence_id TEXT NOT NULL,
                    notice_type TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    recipient_title TEXT,
                    claims TEXT NOT NULL,
                    harm_description TEXT NOT NULL,
                    response_deadline_days INTEGER DEFAULT 10,
                    mail_tracking_number TEXT,
                    sent_date TEXT,
                    deadline_date TEXT,
                    return_receipt_received INTEGER DEFAULT 0,
                    response_received INTEGER DEFAULT 0,
                    response_text TEXT,
                    response_date TEXT,
                    receipt_date TEXT,
                    status TEXT DEFAULT 'DRAFT',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sequence_id) REFERENCES protest_sequences(sequence_id)
                )
            ''')
            
            # Declaratory judgment requests
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS declaratory_judgments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sequence_id TEXT NOT NULL,
                    court_name TEXT NOT NULL,
                    case_number TEXT,
                    filing_date TEXT,
                    judgment_text TEXT,
                    judgment_date TEXT,
                    status TEXT DEFAULT 'PENDING',
                    FOREIGN KEY (sequence_id) REFERENCES protest_sequences(sequence_id)
                )
            ''')
            
            conn.commit()
    
    # =========================================================================
    # NOTARY AUTHORITY MANAGEMENT
    # =========================================================================
    
    def register_notary(self, notary: NotaryAuthority) -> int:
        """Register a notary authority in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO notary_authorities 
                (notary_name, commission_number, state, county, commission_expiry)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                notary.notary_name,
                notary.commission_number,
                notary.state,
                notary.county,
                notary.commission_expiry
            ))
            conn.commit()
            
            # Get the ID
            cursor.execute('''
                SELECT id FROM notary_authorities 
                WHERE notary_name = ? AND commission_number = ? AND state = ?
            ''', (notary.notary_name, notary.commission_number, notary.state))
            result = cursor.fetchone()
            return result[0] if result else -1
    
    def get_notary_by_id(self, notary_id: int) -> Optional[NotaryAuthority]:
        """Retrieve a notary by database ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT notary_name, commission_number, state, county, commission_expiry
                FROM notary_authorities WHERE id = ?
            ''', (notary_id,))
            row = cursor.fetchone()
            
            if row:
                return NotaryAuthority(
                    notary_name=row[0],
                    commission_number=row[1],
                    state=row[2],
                    county=row[3],
                    commission_expiry=row[4]
                )
            return None
    
    def list_notaries(self) -> List[Dict[str, str]]:
        """List all registered notaries."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, notary_name, commission_number, state, county, commission_expiry
                FROM notary_authorities ORDER BY notary_name
            ''')
            return [
                {
                    "id": row[0],
                    "notary_name": row[1],
                    "commission_number": row[2],
                    "state": row[3],
                    "county": row[4],
                    "commission_expiry": row[5]
                }
                for row in cursor.fetchall()
            ]
    
    # =========================================================================
    # PROTEST SEQUENCE MANAGEMENT
    # =========================================================================
    
    def create_sequence(self, sender: str, recipient: str, recipient_title: str,
                       case_title: str, harm_description: str, claims: List[str],
                       notary_id: Optional[int] = None) -> ProtestSequence:
        """
        Create a new notarial protest sequence.
        
        Args:
            sender: Name of the person sending the notices
            recipient: Name of the target (official, attorney, etc.)
            recipient_title: Official title of the recipient
            case_title: Short title for the case/matter
            harm_description: Clear statement of harm, damage, injury, or loss
            claims: List of specific claims/violations
            notary_id: Optional notary ID to associate with sequence
            
        Returns:
            New ProtestSequence object
        """
        sequence_id = self._generate_sequence_id(sender, recipient, case_title)
        
        sequence = ProtestSequence(
            sequence_id=sequence_id,
            sender=sender,
            recipient=recipient,
            recipient_title=recipient_title,
            case_title=case_title,
            harm_description=harm_description,
            claims=claims,
            notary=self.get_notary_by_id(notary_id) if notary_id else None
        )
        
        # Save to database
        self._save_sequence(sequence)
        
        return sequence
    
    def _generate_sequence_id(self, sender: str, recipient: str, case_title: str) -> str:
        """Generate a unique sequence ID."""
        import hashlib
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_string = f"{sender}_{recipient}_{case_title}_{timestamp}"
        return f"NP_{hashlib.md5(unique_string.encode()).hexdigest()[:8]}"
    
    def _save_sequence(self, sequence: ProtestSequence) -> None:
        """Save a protest sequence to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            notary_id = None
            if sequence.notary:
                # Check if notary exists, register if not
                existing = cursor.execute('''
                    SELECT id FROM notary_authorities 
                    WHERE notary_name = ? AND commission_number = ? AND state = ?
                ''', (
                    sequence.notary.notary_name,
                    sequence.notary.commission_number,
                    sequence.notary.state
                )).fetchone()
                
                if existing:
                    notary_id = existing[0]
                else:
                    cursor.execute('''
                        INSERT INTO notary_authorities 
                        (notary_name, commission_number, state, county, commission_expiry)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        sequence.notary.notary_name,
                        sequence.notary.commission_number,
                        sequence.notary.state,
                        sequence.notary.county,
                        sequence.notary.commission_expiry
                    ))
                    notary_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT OR REPLACE INTO protest_sequences 
                (sequence_id, sender, recipient, recipient_title, case_title, 
                 harm_description, claims, notary_id, created_date, completed, 
                 tacit_admission_established)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sequence.sequence_id,
                sequence.sender,
                sequence.recipient,
                sequence.recipient_title,
                sequence.case_title,
                sequence.harm_description,
                json.dumps(sequence.claims),
                notary_id,
                sequence.created_date,
                int(sequence.completed),
                int(sequence.tacit_admission_established)
            ))
            
            # Save all notices
            for notice in sequence.notices:
                cursor.execute('''
                    INSERT OR REPLACE INTO notices 
                    (notice_id, sequence_id, notice_type, sender, recipient, 
                     recipient_title, claims, harm_description, response_deadline_days,
                     mail_tracking_number, sent_date, deadline_date, 
                     return_receipt_received, response_received, response_text,
                     response_date, receipt_date, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ''', (
                    notice.notice_id,
                    notice.sequence_id,
                    notice.notice_type,
                    notice.sender,
                    notice.recipient,
                    notice.recipient_title,
                    json.dumps(notice.claims),
                    notice.harm_description,
                    notice.response_deadline_days,
                    notice.mail_tracking_number,
                    notice.sent_date,
                    notice.deadline_date,
                    int(notice.return_receipt_received),
                    int(notice.response_received),
                    getattr(notice, 'response_text', None),
                    getattr(notice, 'response_date', None),
                    getattr(notice, 'receipt_date', None),
                    notice.get_status()
                ))
            
            conn.commit()
    
    def get_sequence(self, sequence_id: str) -> Optional[ProtestSequence]:
        """Retrieve a protest sequence by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT sequence_id, sender, recipient, recipient_title, 
                       case_title, harm_description, claims, notary_id, 
                       created_date, completed, tacit_admission_established
                FROM protest_sequences WHERE sequence_id = ?
            ''', (sequence_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            sequence = ProtestSequence(
                sequence_id=row[0],
                sender=row[1],
                recipient=row[2],
                recipient_title=row[3],
                case_title=row[4],
                harm_description=row[5],
                claims=json.loads(row[6]),
                notary=self.get_notary_by_id(row[7])
            )
            sequence.created_date = row[8]
            sequence.completed = bool(row[9])
            sequence.tacit_admission_established = bool(row[10])
            
            # Load notices
            cursor.execute('''
                SELECT notice_id, sequence_id, notice_type, sender, recipient,
                       recipient_title, claims, harm_description, response_deadline_days,
                       mail_tracking_number, sent_date, deadline_date,
                       return_receipt_received, response_received, response_text,
                       response_date, receipt_date
                FROM notices WHERE sequence_id = ? ORDER BY notice_id
            ''', (sequence_id,))
            
            for notice_row in cursor.fetchall():
                notice = Notice(
                    notice_id=notice_row[0],
                    sequence_id=notice_row[1],
                    notice_type=notice_row[2],
                    sender=notice_row[3],
                    recipient=notice_row[4],
                    recipient_title=notice_row[5],
                    claims=json.loads(notice_row[6]),
                    harm_description=notice_row[7],
                    response_deadline_days=notice_row[8],
                    mail_tracking_number=notice_row[9],
                    sent_date=notice_row[10],
                )
                notice.deadline_date = notice_row[11]
                notice.return_receipt_received = bool(notice_row[12])
                notice.response_received = bool(notice_row[13])
                
                if notice_row[14]:
                    notice.response_text = notice_row[14]
                if notice_row[15]:
                    notice.response_date = notice_row[15]
                if notice_row[16]:
                    notice.receipt_date = notice_row[16]
                
                sequence.notices.append(notice)
            
            return sequence
    
    def list_sequences(self, sender: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all protest sequences, optionally filtered by sender."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT sequence_id, sender, recipient, recipient_title, 
                       case_title, created_date, completed, tacit_admission_established
                FROM protest_sequences
            '''
            params = []
            
            if sender:
                query += " WHERE sender = ?"
                params.append(sender)
            
            query += " ORDER BY created_date DESC"
            
            cursor.execute(query, params)
            
            sequences = []
            for row in cursor.fetchall():
                sequences.append({
                    "sequence_id": row[0],
                    "sender": row[1],
                    "recipient": row[2],
                    "recipient_title": row[3],
                    "case_title": row[4],
                    "created_date": row[5],
                    "completed": bool(row[6]),
                    "tacit_admission_established": bool(row[7])
                })
            
            return sequences
    
    def update_notice(self, notice_id: str, **kwargs) -> bool:
        """Update a notice in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get sequence ID first
            cursor.execute('SELECT sequence_id FROM notices WHERE notice_id = ?', (notice_id,))
            result = cursor.fetchone()
            if not result:
                return False
            
            sequence_id = result[0]
            
            # Build update query
            set_clauses = []
            values = []
            
            for key, value in kwargs.items():
                if key == "mail_tracking_number":
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
                elif key == "return_receipt_received":
                    set_clauses.append(f"{key} = ?")
                    values.append(int(value))
                elif key == "response_received":
                    set_clauses.append(f"{key} = ?")
                    values.append(int(value))
                elif key == "sent_date":
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
                    # Recalculate deadline
                    set_clauses.append("deadline_date = ?")
                    sent = datetime.strptime(value, "%Y-%m-%d")
                    deadline = sent + timedelta(days=kwargs.get("response_deadline_days", 10))
                    values.append(deadline.strftime("%Y-%m-%d"))
            
            if not set_clauses:
                return False
            
            values.append(notice_id)
            query = f"UPDATE notices SET {', '.join(set_clauses)} WHERE notice_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            return cursor.rowcount > 0
    
    # =========================================================================
    # NOTICE GENERATION (DOCUMENT TEMPLATES)
    # =========================================================================
    
    def generate_notice_of_intent(self, sequence: ProtestSequence, 
                                   notary: Optional[NotaryAuthority] = None) -> str:
        """
        Generate a Notice of Intent document.
        
        This is the first notice in the sequence, establishing intent to hold
        the recipient accountable through the mail-based court system.
        """
        notary_name = notary.notary_name if notary else "[NOTARY NAME]"
        notary_state = notary.state if notary else "[STATE]"
        notary_county = notary.county if notary else "[COUNTY]"
        
        claims_text = "\n".join([f"  {i+1}. {claim}" for i, claim in enumerate(sequence.claims)])
        
        today = datetime.now().strftime("%B %d, %Y")
        
        document = f"""NOTICE OF INTENT

STATE OF {notary_state.upper()}
COUNTY OF {notary_county.upper()}

I, {sequence.sender}, do hereby serve this NOTICE OF INTENT upon:

{sequence.recipient}
{sequence.recipient_title}

TAKE NOTICE that I, {sequence.sender}, intend to hold you accountable for
violations of law and causes of action arising from the following:

HARM/INJURY SUSTAINED:
{sequence.harm_description}

SPECIFIC CLAIMS:
{claims_text}

You are hereby given NOTICE and OPPORTUNITY to respond to these claims
within TEN (10) DAYS from the date of service.

This notice is sent via First Class Mail, Return Receipt Requested,
and is sworn under the pains and penalties of perjury.

Failure to respond within the specified timeframe will be deemed tacit
admission of the facts herein stated.

DATED: {today}

_________________________
{sequence.sender}
Sender

NOTARY ACKNOWLEDGMENT:

On this {today}, before me, {notary_name}, Notary Public in and for
{notary_county} County, State of {notary_state}, personally appeared
{sequence.sender}, known to me to be the person who executed the foregoing
instrument, and acknowledged that they executed the same as their free act
and deed.

IN TESTIMONY WHEREOF, I have hereunto set my hand and affixed my official
seal the day and year first above written.

_________________________
{notary_name}
Notary Public, {notary_state}
Commission #{notary.commission_number if notary else '[COMMISSION #]'}
Expiring: {notary.commission_expiry if notary else '[EXPIRY DATE]'}

[NOTARY SEAL]
"""
        return document
    
    def generate_notice_and_opportunity(self, sequence: ProtestSequence,
                                        notary: Optional[NotaryAuthority] = None) -> str:
        """
        Generate a Notice and Opportunity document.
        
        This is the second notice, providing formal opportunity to cure
        the violations before final action.
        """
        notary_name = notary.notary_name if notary else "[NOTARY NAME]"
        notary_state = notary.state if notary else "[STATE]"
        notary_county = notary.county if notary else "[COUNTY]"
        
        claims_text = "\n".join([f"  {i+1}. {claim}" for i, claim in enumerate(sequence.claims)])
        
        today = datetime.now().strftime("%B %d, %Y")
        
        document = f"""NOTICE AND OPPORTUNITY

STATE OF {notary_state.upper()}
COUNTY OF {notary_county.upper()}

CASE TITLE: {sequence.case_title}

TO: {sequence.recipient}
    {sequence.recipient_title}

FROM: {sequence.sender}

DATE: {today}

PURSUANT TO: The authority vested in the Notary Public as an officer of
the Court and deputized officer of the Secretary of State.

TAKE NOTICE that you have previously been served with NOTICE OF INTENT
regarding the following harm and violations:

HARM/INJURY SUSTAINED:
{sequence.harm_description}

SPECIFIC VIOLATIONS:
{claims_text}

You were provided TEN (10) DAYS to respond to the initial notice. Having
failed to do so, or having responded inadequately, you are now given a
second and FINAL OPPORTUNITY to cure these violations.

You have TEN (10) DAYS from the date of service of this notice to:

1. Admit or deny each of the above-stated claims in writing
2. Provide evidence of cure or remedial action taken
3. Demonstrate good faith effort to resolve the matters herein

Failure to properly respond within TEN (10) DAYS will result in:
- Tacit admission of all facts through silence and acquiescence
- Proceeding to final notice and potential court action
- Use of your non-response as evidence in any subsequent proceeding

This notice is sent via First Class Mail, Return Receipt Requested,
and is sworn under the pains and penalties of perjury.

DATED: {today}

_________________________
{sequence.sender}
Sender

NOTARY ACKNOWLEDGMENT:

On this {today}, before me, {notary_name}, Notary Public in and for
{notary_county} County, State of {notary_state}, personally appeared
{sequence.sender}, known to me to be the person who executed the foregoing
instrument, and acknowledged that they executed the same as their free act
and deed.

IN TESTIMONY WHEREOF, I have hereunto set my hand and affixed my official
seal the day and year first above written.

_________________________
{notary_name}
Notary Public, {notary_state}
Commission #{notary.commission_number if notary else '[COMMISSION #]'}
Expiring: {notary.commission_expiry if notary else '[EXPIRY DATE]'}

[NOTARY SEAL]
"""
        return document
    
    def generate_final_notice(self, sequence: ProtestSequence,
                              notary: Optional[NotaryAuthority] = None) -> str:
        """
        Generate the Final Notice Before Action.
        
        This is the third notice. After this, with non-response,
        tacit admission is established and declaratory judgment can be sought.
        """
        notary_name = notary.notary_name if notary else "[NOTARY NAME]"
        notary_state = notary.state if notary else "[STATE]"
        notary_county = notary.county if notary else "[COUNTY]"
        
        claims_text = "\n".join([f"  {i+1}. {claim}" for i, claim in enumerate(sequence.claims)])
        
        today = datetime.now().strftime("%B %d, %Y")
        
        document = f"""FINAL NOTICE BEFORE ACTION
AND DECLARATION OF TACIT ADMISSION

STATE OF {notary_state.upper()}
COUNTY OF {notary_county.upper()}

CASE TITLE: {sequence.case_title}

TO: {sequence.recipient}
    {sequence.recipient_title}

FROM: {sequence.sender}

DATE: {today}

PURSUANT TO: 
- The authority of the Notary Public as officer of the Court
- The doctrine of tacit admission through silence and acquiescence
- The principle that "He who does not deny, admits"

TAKE NOTICE that you have been served with TWO (2) prior notices:

1. NOTICE OF INTENT - Served on [DATE OF FIRST NOTICE]
2. NOTICE AND OPPORTUNITY - Served on [DATE OF SECOND NOTICE]

Both notices provided you with specific information regarding:

HARM/INJURY SUSTAINED:
{sequence.harm_description}

SPECIFIC VIOLATIONS:
{claims_text}

You have FAILED TO RESPOND or FAILED TO ADEQUATELY RESPOND to either
of these notices, despite being given proper notice and opportunity.

THIS CONSTITUTES TACIT ADMISSION THROUGH SILENCE AND ACQUIESCENCE.

Your continued silence for TEN (10) DAYS from the date of service of
this FINAL NOTICE will establish:

1. Irrefutable admission of all facts stated in the prior notices
2. Waiver of any and all defenses to the claims herein
3. Acceptance of liability for the harm, damage, injury, and loss caused
4. The right of the undersigned to seek declaratory judgment without
   further notice or proceeding

After TEN (10) DAYS from service of this notice, the undersigned may:
- Appear in any court of competent jurisdiction
- Request declaratory judgment based on your tacit admissions
- Seek all available remedies at law and equity

This notice is sent via First Class Mail, Return Receipt Requested,
and is sworn under the pains and penalties of perjury.

BY YOUR SILENCE, YOU HAVE SPOKEN.

DATED: {today}

_________________________
{sequence.sender}
Sender

NOTARY ACKNOWLEDGMENT:

On this {today}, before me, {notary_name}, Notary Public in and for
{notary_county} County, State of {notary_state}, personally appeared
{sequence.sender}, known to me to be the person who executed the foregoing
instrument, and acknowledged that they executed the same as their free act
and deed.

IN TESTIMONY WHEREOF, I have hereunto set my hand and affixed my official
seal the day and year first above written.

_________________________
{notary_name}
Notary Public, {notary_state}
Commission #{notary.commission_number if notary else '[COMMISSION #]'}
Expiring: {notary.commission_expiry if notary else '[EXPIRY DATE]'}

[NOTARY SEAL]
"""
        return document
    
    def generate_affidavit_of_service(self, notice: Notice, 
                                      service_date: str, 
                                      tracking_number: str,
                                      notary: Optional[NotaryAuthority] = None) -> str:
        """
        Generate an Affidavit of Service for a notice.
        
        This documents that the notice was properly served via certified mail.
        """
        notary_name = notary.notary_name if notary else "[NOTARY NAME]"
        notary_state = notary.state if notary else "[STATE]"
        notary_county = notary.county if notary else "[COUNTY]"
        
        document = f"""AFFIDAVIT OF SERVICE

STATE OF {notary_state.upper()}
COUNTY OF {notary_county.upper()}

I, {notice.sender}, being first duly sworn upon oath, do hereby depose
and state as follows:

1. That I am the sender of a certain notice addressed to:
   
   {notice.recipient}
   {notice.recipient_title}

2. That on {service_date}, I deposited said notice in the United States
   Postal Service, First Class Mail, Return Receipt Requested, addressed
   as aforesaid.

3. That the certified mail tracking number for said notice is: {tracking_number}

4. That the notice was: [DESCRIBE NOTICE TYPE - Notice of Intent/Notice and Opportunity/Final Notice]

5. That the notice contained claims of harm, damage, injury, or loss
   and provided the recipient with notice and opportunity to respond.

6. That I have been advised that if the recipient fails to respond within
   the time specified, such failure will constitute tacit admission through
   silence and acquiescence.

I declare under the pains and penalties of perjury that the foregoing is
true and correct.

DATED: {service_date}

_________________________
{notice.sender}

SUBSCRIBED AND SWORN to before me this {service_date}.

_________________________
{notary_name}
Notary Public, {notary_state}
Commission #{notary.commission_number if notary else '[COMMISSION #]'}

[NOTARY SEAL]
"""
        return document
    
    def generate_declaration_of_default(self, sequence: ProtestSequence,
                                        notary: Optional[NotaryAuthority] = None) -> str:
        """
        Generate a Declaration of Default after three non-responses.
        
        This document establishes that tacit admission has been achieved
        and can be filed with a court to request declaratory judgment.
        """
        notary_name = notary.notary_name if notary else "[NOTARY NAME]"
        notary_state = notary.state if notary else "[STATE]"
        notary_county = notary.county if notary else "[COUNTY]"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        # Get dates from notices
        notice_dates = []
        for notice in sequence.notices:
            if notice.mail_tracking_number:
                notice_dates.append(notice.sent_date)
        
        dates_str = ", ".join(notice_dates) if notice_dates else "[DATES OF NOTICES]"
        
        claims_text = "\n".join([f"  {i+1}. {claim}" for i, claim in enumerate(sequence.claims)])
        
        document = f"""DECLARATION OF DEFAULT AND TACIT ADMISSION

STATE OF {notary_state.upper()}
COUNTY OF {notary_county.upper()}

CASE TITLE: {sequence.case_title}

I, {sequence.sender}, being first duly sworn upon oath, do hereby declare:

1. That I am the sender of THREE (3) separate notices to:
   
   {sequence.recipient}
   {sequence.recipient_title}

2. That said notices were served on the following dates: {dates_str}

3. That each notice was sent via United States Postal Service, First Class
   Mail, Return Receipt Requested.

4. That each notice was properly addressed and contained:
   - Clear identification of the recipient
   - Specific claims of harm, damage, injury, or loss
   - Notice and opportunity to respond
   - Statement that it was sworn under penalty of perjury

5. That the recipient FAILED TO RESPOND to any of the THREE (3) notices
   within the time periods specified (TEN (10) DAYS each).

6. That said non-responses constitute TACIT ADMISSION through silence
   and acquiescence pursuant to the legal maxim "He who does not deny,
   admits" and the doctrine of tacit admission.

7. That by operation of law, the recipient has admitted:
   - All facts stated in the notices
   - Liability for the harm, damage, injury, and loss caused
   - Waiver of all defenses
   
   Specifically, the following claims are deemed admitted:
   
   {claims_text}

8. That the harm described in the notices is: {sequence.harm_description}

9. That I am now entitled to seek declaratory judgment from any court
   of competent jurisdiction based on the recipient's tacit admissions.

WHEREFORE, I request that this Declaration be accepted as prima facie
evidence of the recipient's admissions and that declaratory judgment be
entered in my favor.

I declare under the pains and penalties of perjury that the foregoing is
true and correct to the best of my knowledge and belief.

DATED: {today}

_________________________
{sequence.sender}

SUBSCRIBED AND SWORN to before me this {today}.

_________________________
{notary_name}
Notary Public, {notary_state}
Commission #{notary.commission_number if notary else '[COMMISSION #]'}

[NOTARY SEAL]
"""
        return document
    
    def generate_motion_for_declaratory_judgment(self, sequence: ProtestSequence,
                                                 court_name: str, 
                                                 notary: Optional[NotaryAuthority] = None) -> str:
        """
        Generate a Motion for Declaratory Judgment.
        
        This is the final document to file with a court after establishing
        tacit admission through three non-responses.
        """
        notary_name = notary.notary_name if notary else "[NOTARY NAME]"
        notary_state = notary.state if notary else "[STATE]"
        notary_county = notary.county if notary else "[COUNTY]"
        
        today = datetime.now().strftime("%B %d, %Y")
        
        claims_text = "\n".join([f"  {i+1}. {claim}" for i, claim in enumerate(sequence.claims)])
        
        document = f"""MOTION FOR DECLARATORY JUDGMENT

IN THE [DISTRICT/CIRCUIT/SUPERIOR] COURT OF {court_name}

{sequence.sender},
    Plaintiff,
    
    vs.
    
{sequence.recipient},
{sequence.recipient_title},
    Defendant.

)  CASE NO.: [TO BE ASSIGNED]

PLANTIFF'S MOTION FOR DECLARATORY JUDGMENT

TO THE HONORABLE COURT:

Comes now the Plaintiff, {sequence.sender}, and respectfully moves this
Honorable Court for entry of declaratory judgment in Plaintiff's favor
based on the Defendant's tacit admissions through silence and
acquiescence, and in support states as follows:

1. That Plaintiff served THREE (3) separate notices upon Defendant
   via First Class Mail, Return Receipt Requested, on the following dates:
   [LIST DATES FROM NOTICES]

2. That each notice contained specific claims of harm, damage, injury,
   or loss, and provided Defendant with notice and opportunity to respond.

3. That each notice was sworn under the pains and penalties of perjury
   and properly notarized by a Notary Public acting as an officer of the Court.

4. That Defendant FAILED TO RESPOND to any of the THREE (3) notices
   within the time periods specified.

5. That said non-responses constitute TACIT ADMISSION through silence
   and acquiescence, a well-established principle of law.

6. That by operation of law, Defendant has admitted:
   - All facts stated in the notices
   - Liability for the harm, damage, injury, and loss caused
   - Waiver of all defenses

7. The claims at issue are:
   
   {claims_text}

8. The harm sustained by Plaintiff is: {sequence.harm_description}

9. Plaintiff is entitled to declaratory judgment establishing:
   - Defendant's liability for the harm caused
   - The validity of Plaintiff's claims
   - Plaintiff's right to remedies at law and equity

WHEREFORE, Plaintiff respectfully requests that this Honorable Court:

1. Grant this Motion for Declaratory Judgment;
2. Declare that Defendant has tacitly admitted all claims through silence;
3. Declare that Defendant is liable to Plaintiff for the harm described;
4. Grant such other and further relief as the Court deems just and proper.

Respectfully submitted,

DATED: {today}

_________________________
{sequence.sender}
Plaintiff, Pro Se

VERIFICATION

I, {sequence.sender}, declare under penalty of perjury that the foregoing
is true and correct to the best of my knowledge and belief.

DATED: {today}

_________________________
{sequence.sender}

NOTARY ACKNOWLEDGMENT:

On this {today}, before me, {notary_name}, Notary Public in and for
{notary_county} County, State of {notary_state}, personally appeared
{sequence.sender}, known to me to be the person who executed the foregoing
instrument.

_________________________
{notary_name}
Notary Public, {notary_state}
Commission #{notary.commission_number if notary else '[COMMISSION #]'}

[NOTARY SEAL]
"""
        return document
    
    # =========================================================================
    # WORKFLOW HELPERS
    # =========================================================================
    
    def create_complete_sequence(self, sender: str, recipient: str, 
                                  recipient_title: str, case_title: str,
                                  harm_description: str, claims: List[str],
                                  notary: NotaryAuthority) -> ProtestSequence:
        """
        Create a complete three-notice sequence with all documents.
        
        This is a convenience method that creates the sequence and generates
        all three notice documents ready for mailing.
        """
        sequence = self.create_sequence(
            sender=sender,
            recipient=recipient,
            recipient_title=recipient_title,
            case_title=case_title,
            harm_description=harm_description,
            claims=claims,
            notary_id=None  # Will be set when we save
        )
        
        # Create all three notices
        notice1 = sequence.create_notice_of_intent()
        notice2 = sequence.create_notice_and_opportunity()
        notice3 = sequence.create_final_notice()
        
        # Associate notary
        sequence.notary = notary
        
        # Save to database
        self._save_sequence(sequence)
        
        return sequence
    
    def get_next_action(self, sequence_id: str) -> Dict[str, Any]:
        """
        Determine the next action needed for a protest sequence.
        
        Returns:
            Dictionary with action type and any relevant data
        """
        sequence = self.get_sequence(sequence_id)
        if not sequence:
            return {"action": "error", "message": "Sequence not found"}
        
        # Check if sequence is complete
        if sequence.check_tacit_admission():
            return {
                "action": "ready_for_judgment",
                "message": "Tacit admission established. Ready to file for declaratory judgment.",
                "next_notice": None
            }
        
        # Check notices
        notice_count = len(sequence.notices)
        
        if notice_count == 0:
            return {
                "action": "create_notice_of_intent",
                "message": "Create and send Notice of Intent",
                "next_notice_type": "notice_of_intent"
            }
        
        if notice_count == 1:
            notice = sequence.notices[0]
            if not notice.mail_tracking_number:
                return {
                    "action": "send_notice_01",
                    "message": f"Send Notice of Intent (ID: {notice.notice_id})",
                    "notice_id": notice.notice_id
                }
            elif not notice.return_receipt_received:
                return {
                    "action": "await_receipt_01",
                    "message": f"Await return receipt for Notice of Intent",
                    "notice_id": notice.notice_id
                }
            elif not notice.is_overdue():
                return {
                    "action": "wait_for_response_01",
                    "message": f"Waiting for response to Notice of Intent. Deadline: {notice.deadline_date}",
                    "notice_id": notice.notice_id
                }
            else:
                return {
                    "action": "create_notice_and_opportunity",
                    "message": "Create and send Notice and Opportunity",
                    "next_notice_type": "notice_and_opportunity"
                }
        
        if notice_count == 2:
            notice = sequence.notices[1]
            if not notice.mail_tracking_number:
                return {
                    "action": "send_notice_02",
                    "message": f"Send Notice and Opportunity (ID: {notice.notice_id})",
                    "notice_id": notice.notice_id
                }
            elif not notice.return_receipt_received:
                return {
                    "action": "await_receipt_02",
                    "message": f"Await return receipt for Notice and Opportunity",
                    "notice_id": notice.notice_id
                }
            elif not notice.is_overdue():
                return {
                    "action": "wait_for_response_02",
                    "message": f"Waiting for response to Notice and Opportunity. Deadline: {notice.deadline_date}",
                    "notice_id": notice.notice_id
                }
            else:
                return {
                    "action": "create_final_notice",
                    "message": "Create and send Final Notice Before Action",
                    "next_notice_type": "final_notice_before_action"
                }
        
        if notice_count >= 3:
            notice = sequence.notices[2]
            if not notice.mail_tracking_number:
                return {
                    "action": "send_notice_03",
                    "message": f"Send Final Notice (ID: {notice.notice_id})",
                    "notice_id": notice.notice_id
                }
            elif not notice.return_receipt_received:
                return {
                    "action": "await_receipt_03",
                    "message": "Await return receipt for Final Notice",
                    "notice_id": notice.notice_id
                }
            elif not notice.is_overdue():
                return {
                    "action": "wait_for_response_03",
                    "message": f"Waiting for response to Final Notice. Deadline: {notice.deadline_date}",
                    "notice_id": notice.notice_id
                }
            else:
                # All three notices sent and overdue
                non_responses = sequence.get_non_response_count()
                if non_responses >= 3:
                    return {
                        "action": "ready_for_judgment",
                        "message": "All three notices have non-responses. Tacit admission established.",
                        "next_notice": None
                    }
        
        return {"action": "unknown", "message": "Unable to determine next action"}
    
    def get_sequence_status(self, sequence_id: str) -> Dict[str, Any]:
        """Get comprehensive status of a protest sequence."""
        sequence = self.get_sequence(sequence_id)
        if not sequence:
            return {"error": "Sequence not found"}
        
        notices = []
        for notice in sequence.notices:
            notices.append({
                "notice_id": notice.notice_id,
                "type": notice.notice_type,
                "status": notice.get_status(),
                "sent_date": notice.sent_date,
                "deadline": notice.deadline_date,
                "overdue": notice.is_overdue(),
                "non_response": notice.is_non_response(),
                "tracking_number": notice.mail_tracking_number,
                "return_receipt_received": notice.return_receipt_received,
                "response_received": notice.response_received
            })
        
        return {
            "sequence_id": sequence.sequence_id,
            "case_title": sequence.case_title,
            "sender": sequence.sender,
            "recipient": sequence.recipient,
            "recipient_title": sequence.recipient_title,
            "created_date": sequence.created_date,
            "notices": notices,
            "notices_sent": len(sequence.notices),
            "non_responses": sequence.get_non_response_count(),
            "tacit_admission_established": sequence.check_tacit_admission(),
            "can_request_judgment": sequence.can_request_declaratory_judgment(),
            "next_action": self.get_next_action(sequence_id)
        }


# =============================================================================
# SINGLETON ACCESSOR
# =============================================================================

def get_notarial_protest_engine() -> NotarialProtestEngine:
    """Get the singleton instance of the Notarial Protest Engine."""
    return NotarialProtestEngine.get_engine()


# =============================================================================
# QUICK START EXAMPLE
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("NOTARIAL PROTEST ENGINE - STANDALONE TEST")
    print("=" * 80)
    
    # Initialize engine
    engine = get_notarial_protest_engine()
    
    # Register a notary
    notary = NotaryAuthority(
        notary_name="Jane Doe",
        commission_number="CA1234567",
        state="California",
        county="Los Angeles",
        commission_expiry="2028-12-31"
    )
    notary_id = engine.register_notary(notary)
    print(f"\n[+] Registered Notary: {notary.notary_name} (ID: {notary_id})")
    
    # Create a protest sequence
    sequence = engine.create_complete_sequence(
        sender="John Smith",
        recipient="Officer John Jones",
        recipient_title="Police Officer, Badge #4567",
        case_title="Smith v. Jones - Unlawful Detention",
        harm_description="On January 15, 2024, Officer Jones unlawfully detained John Smith without probable cause, causing emotional distress, loss of liberty, and damage to reputation.",
        claims=[
            "Violation of 42 U.S.C. § 1983 - Deprivation of rights under color of law",
            "False imprisonment",
            "Violation of Fourth Amendment - Unreasonable seizure",
            "Violation of Fourteenth Amendment - Due process",
            "Intentional infliction of emotional distress"
        ],
        notary=notary
    )
    
    print(f"\n[+] Created Protest Sequence: {sequence.sequence_id}")
    print(f"[+] Case Title: {sequence.case_title}")
    print(f"[+] Sender: {sequence.sender}")
    print(f"[+] Recipient: {sequence.recipient} ({sequence.recipient_title})")
    
    # Generate and display the first notice
    print("\n" + "=" * 80)
    print("NOTICE OF INTENT (First Notice)")
    print("=" * 80)
    notice_01 = engine.generate_notice_of_intent(sequence, notary)
    print(notice_01)
    
    # Show status
    print("\n" + "=" * 80)
    print("SEQUENCE STATUS")
    print("=" * 80)
    status = engine.get_sequence_status(sequence.sequence_id)
    for key, value in status.items():
        if key != "notices":
            print(f"{key:30s}: {value}")
    
    print("\nNOTICES:")
    for notice in status["notices"]:
        print(f"  - {notice['type']}: {notice['status']}")
    
    print("\nNEXT ACTION:")
    next_action = status.get("next_action", {})
    print(f"  Action: {next_action.get('action', 'N/A')}")
    print(f"  Message: {next_action.get('message', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
