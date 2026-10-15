"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: test_document_labels.py
LAST_SYNC: 2026-08-02T01:13:31Z
[/DNA_TAG]
"""
import pytest
from outclaw_orchestrator import OutClawOrchestrator

def test_generate_document_draft_label():
    # Initialize orchestrator
    orch = OutClawOrchestrator(agent_name="test_agent")
    
    # Generate document
    case_data = {
        "plaintiff": "John Doe",
        "defendant": "Officer Smith",
        "facts": "On January 1, 2024, Defendant entered Plaintiff's home without a warrant."
    }
    
    result = orch.generate_document("complaint_1983", case_data)
    
    # Check for draft label
    content = result.get('content', '')
    assert content.startswith("DRAFT — NOT REVIEWED, DO NOT FILE"), "Document is NOT labeled as DRAFT"
