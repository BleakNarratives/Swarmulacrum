"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: test_validation.py
LAST_SYNC: 2026-08-02T01:13:31Z
[/DNA_TAG]
"""
import pytest
from outclaw_orchestrator import OutClawOrchestrator
import time

def test_run_full_analysis_validation():
    # Initialize orchestrator
    orch = OutClawOrchestrator(agent_name="test_agent")
    
    # Run full analysis
    case_description = "The government official violated my rights under color of law. Case ID: " + str(time.time())
    results = orch.run_full_analysis(case_description)
    
    # Check for validation
    assessment = results.get('assessment', {})
    validation = assessment.get('validation')
    
    assert validation is not None, "Validation result not found in assessment"
    assert 'pass' in validation, "Validation result is missing 'pass' key"
