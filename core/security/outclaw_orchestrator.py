"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: outclaw_orchestrator.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
OUTCLAW ORCHESTRATOR - Master Coordination System

This is the central intelligence that coordinates all OutClaw components,
ensures multi-agent collaboration (Mistral Vibe + Gemini CLI), and
orchestrates the full legal accountability engine.

"A republic, if you can keep it." - Benjamin Franklin

The responsibility to remain free is something that a man or woman fights for
every day of their life. No one else can do it for you.

This orchestrator:
1. Coordinates with other AI agents via the event bus
2. Manages the workflow of legal analysis and case preparation
3. Tracks tasks and prevents duplication
4. Provides a unified interface to all OutClaw capabilities

"""

import json
import os
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime

# Import OutClaw modules
from event_bus import get_bus, EventBus
from case_db_core import CaseDatabase
from outclaw_engine import OutClawEngine
from outclaw_boardroom_core import OutClawBoardroomEngine, LEGAL_AGENTS
from predicate_core import PredicateEngine
from rebuttal_engine import generate_rebuttal_brief
from bleak_playbook import RealLegalAnalyzer
from prose_tactics_library import get_tactics_library
from constitutional_core import get_constitutional_core
from outclaw_validator import validate_session


class OutClawOrchestrator:
    """
    Master orchestrator for the OutClaw legal analysis engine.
    Coordinates all components and multi-agent collaboration.
    """
    
    def __init__(self, agent_name="mistral_vibe"):
        self.agent_name = agent_name
        self.bus = get_bus(agent_name)
        self.base_dir = "/storage/emulated/0/RootBase/OutClaw"
        
        # Register agent capabilities
        self.capabilities = [
            "legal_analysis",
            "document_processing",
            "constitutional_analysis",
            "tactics_recommendation",
            "case_management",
            "evidence_analysis",
            "motion_generation",
            "rebuttal_generation",
            "precedent_research",
            "deadline_tracking"
        ]
        self.bus.register_agent(capabilities=self.capabilities)
        
        # Initialize components
        self._initialize_components()
        
        # Task registry for internal coordination
        self.active_tasks = {}
        self.completed_tasks = {}
        
        print(f"[+] OutClaw Orchestrator initialized for {agent_name}")
        print(f"[+] Capabilities: {len(self.capabilities)}")
    
    def _initialize_components(self):
        """Initialize all OutClaw components."""
        self.components = {
            "database": CaseDatabase(),
            "engine": OutClawEngine(),
            "boardroom": OutClawBoardroomEngine(),
            "predicate": PredicateEngine(),
            "tactics": get_tactics_library(),
            "constitution": get_constitutional_core(),
            "analyzer": RealLegalAnalyzer()
        }
        print(f"[+] Loaded {len(self.components)} core components")
    
    def check_other_agents(self):
        """Check for other active agents and coordinate."""
        other_agents = self.bus.list_active_agents()
        active_others = {k: v for k, v in other_agents.items() if k != self.agent_name}
        
        print(f"\n[*] Active Agents in Swarm:")
        for name, info in active_others.items():
            print(f"  - {name}: {info.get('capabilities', [])}")
        
        return active_others
    
    def claim_task(self, task_name: str, description: str, priority="high") -> bool:
        """
        Claim a task for this agent to execute.
        Checks with other agents first to avoid duplication.
        """
        # Check if another agent is already working on this
        task_status = self.bus.get_task_status(task_name)
        
        if task_status:
            if task_status.get('status') == 'completed':
                print(f"[-] Task '{task_name}' already completed by {task_status.get('assigned_to')}")
                return False
            if task_status.get('assigned_to') != self.agent_name:
                print(f"[-] Task '{task_name}' claimed by {task_status.get('assigned_to')}")
                return False
        
        # Claim the task
        success, msg = self.bus.claim_task(task_name, description)
        if success:
            self.active_tasks[task_name] = {
                "description": description,
                "started": datetime.now().isoformat(),
                "status": "in_progress",
                "priority": priority
            }
            print(f"[+] Claimed task: {task_name}")
            self.bus.emit_event("task_claimed", {
                "task": task_name,
                "agent": self.agent_name,
                "description": description
            })
            return True
        else:
            print(f"[-] Failed to claim task: {msg}")
            return False
    
    def complete_task(self, task_name: str, result: Any) -> bool:
        """Mark a task as completed."""
        if task_name not in self.active_tasks:
            print(f"[-] Task '{task_name}' not found in active tasks")
            return False
        
        # Update bus
        success, msg = self.bus.complete_task(task_name, result)
        
        if success:
            # Move to completed
            task_data = self.active_tasks.pop(task_name)
            self.completed_tasks[task_name] = {
                **task_data,
                "completed": datetime.now().isoformat(),
                "result": result
            }
            print(f"[+] Completed task: {task_name}")
            self.bus.emit_event("task_completed", {
                "task": task_name,
                "agent": self.agent_name,
                "result": str(result)[:500]  # Truncate for event log
            })
            return True
        else:
            print(f"[-] Failed to complete task: {msg}")
            return False
    
    def run_full_analysis(self, case_description: str, doc_path: str = None) -> Dict:
        """
        Run a comprehensive legal analysis on a case.
        This coordinates multiple components for maximum insight.
        """
        import hashlib
        task_name = f"analysis_{hashlib.md5(case_description.encode()).hexdigest()[:8]}"
        
        if not self.claim_task(task_name, f"Full analysis: {case_description[:50]}"):
            return {"status": "error", "message": "Task already claimed by another agent"}
        
        try:
            results = {
                "case_description": case_description,
                "timestamp": datetime.now().isoformat(),
                "agent": self.agent_name,
                "components": {}
            }
            
            # 1. Predicate Analysis (CAN/CANNOT)
            print("\n[*] Running Predicate Core Analysis...")
            predicate = self.components['predicate']
            # Extract basic facts from description
            color_of_law = "official" in case_description.lower() or "government" in case_description.lower()
            deprivation = "right" in case_description.lower() or "violation" in case_description.lower()
            duty = "oath" in case_description.lower() or "official" in case_description.lower()
            misconduct = "violation" in case_description.lower() or "misconduct" in case_description.lower()
            
            results['components']['predicate'] = predicate.evaluate_scenario(
                color_of_law=color_of_law,
                deprivation=deprivation,
                duty=duty,
                misconduct=misconduct
            )
            
            # 2. Constitutional Analysis
            print("[*] Running Constitutional Core Analysis...")
            results['components']['constitutional'] = self.components['constitution'].analyze_law(case_description)
            
            # 3. Tactics Recommendation
            print("[*] Running Tactics Recommendation...")
            # Determine case type from description
            case_type = self._determine_case_type(case_description)
            stage = "pre-filing"  # Default
            results['components']['tactics'] = self.components['tactics'].get_strategy_recommendation(
                case_type, stage
            )[:5]  # Top 5 recommendations
            
            # 4. Boardroom Deliberation
            print("[*] Running Vertical Boardroom Analysis...")
            results['components']['boardroom'] = self._run_boardroom(case_description)
            
            # 5. Document Analysis (if doc provided)
            if doc_path and os.path.exists(doc_path):
                print("[*] Running Document Analysis...")
                results['components']['document'] = self.components['analyzer'].process_case_document(doc_path)
            
            # Compile final assessment
            results['assessment'] = self._compile_assessment(results['components'])
            
            self.complete_task(task_name, results)
            return results
            
        except Exception as e:
            self.complete_task(task_name, {"status": "error", "error": str(e)})
            raise
    
    def _determine_case_type(self, description: str) -> str:
        """Determine case type from description."""
        desc_lower = description.lower()
        
        if any(w in desc_lower for w in ['cps', 'child protective', 'family court', 'child']):
            return 'cps'
        elif any(w in desc_lower for w in ['1983', 'civil rights', 'section 1983', 'police']):
            return '1983'
        elif any(w in desc_lower for w in ['federal', 'agency', 'administrative', 'departments']):
            return 'administrative'
        elif any(w in desc_lower for w in ['criminal', 'prosecution', 'arrest', 'charges']):
            return 'criminal'
        elif any(w in desc_lower for w in ['family', 'divorce', 'custody', 'support']):
            return 'family'
        else:
            return 'general'
    
    def _run_boardroom(self, user_input: str) -> Dict:
        """Run the vertical boardroom analysis."""
        # This would normally use the boardroom engine
        # For now, we'll simulate it
        boardroom = self.components['boardroom']
        
        # Capture the output
        import io
        import sys
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                boardroom.execute_session(user_input)
            except:
                pass
        
        output = f.getvalue()
        
        return {
            "input": user_input,
            "deliberation": output,
            "agents": list(LEGAL_AGENTS.keys())
        }
    
    def _compile_assessment(self, components: Dict) -> Dict:
        """Compile final assessment from all component analyses."""
        assessment = {
            "summary": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "priority_actions": []
        }
        
        # Analyze predicate results
        if 'predicate' in components:
            for result in components['predicate']:
                if result.startswith('[CAN HAPPEN]'):
                    assessment['strengths'].append(result)
                    assessment['summary'].append(result)
                else:
                    assessment['weaknesses'].append(result)
                    assessment['summary'].append(result)
        
        # Analyze constitutional results
        if 'constitutional' in components:
            const = components['constitutional']
            assessment['summary'].append(f"Constitutional Assessment: {const.get('assessment', 'Unknown')}")
            
            if const.get('assessment') == "UNCONSTITUTIONAL - Exceeds enumerated powers":
                assessment['priority_actions'].append(
                    "FILE MOTION TO DISMISS - Challenge lack of constitutional authority"
                )
        
        # Analyze tactics
        if 'tactics' in components:
            for tactic in components['tactics']:
                assessment['recommendations'].append(
                    f"Consider: {tactic.get('name', 'Unknown')} ({tactic.get('category', 'N/A')})"
                )
        
        # Analyze boardroom
        if 'boardroom' in components:
            boardroom = components['boardroom']
            if 'deliberation' in boardroom:
                # Extract key insights
                deliberation = boardroom['deliberation']
                if "COLOR OF LAW" in deliberation:
                    assessment['strengths'].append("Color of law elements present")
                if "SHIELD WARNING" in deliberation:
                    assessment['weaknesses'].append("Immunity shield may be active - needs piercing strategy")
        
        # Analyze document
        if 'document' in components:
            doc = components['document']
            if doc and 'matches_found' in doc:
                for category, matches in doc['matches_found'].items():
                    assessment['recommendations'].append(
                        f"Document contains {len(matches)} {category} references - use these as statutory anchors"
                    )
        
        # Validate assessment
        question = components.get('boardroom', {}).get('input', 'Full analysis')
        answer = "\n".join(assessment['summary'])
        result = validate_session(question, answer)
        assessment['validation'] = result
        
        return assessment
    
    def generate_document(self, doc_type: str, case_data: Dict) -> Dict:
        """
        Generate legal documents (complaints, motions, etc.).
        """
        generators = {
            "complaint_1983": self._generate_1983_complaint,
            "motion_dismiss": self._generate_motion_to_dismiss,
            "motion_compel": self._generate_motion_to_compel,
            "affidavit": self._generate_affidavit,
            "discovery_request": self._generate_discovery_request,
            "rebuttal": self._generate_rebuttal
        }
        
        if doc_type in generators:
            result = generators[doc_type](case_data)
            # Prepend DRAFT notice to content if it exists
            if "content" in result:
                result["content"] = "DRAFT — NOT REVIEWED, DO NOT FILE\n\n" + result["content"]
            return result
        else:
            return {"status": "error", "message": f"Unknown document type: {doc_type}"}
    
    def _generate_1983_complaint(self, case_data: Dict) -> Dict:
        """Generate a 42 USC 1983 complaint."""
        # This would use templates and case data to generate a complaint
        complaint = f"""
UNITED STATES DISTRICT COURT
[DISTRICT]

{case_data.get('plaintiff', 'Plaintiff')}, )
    Plaintiff,         )
                        )  Case No.: [TO BE ASSIGNED]
vs.                     )
                        )
{case_data.get('defendant', 'Defendant')}, )
    Defendant.         )

COMPLAINT FOR VIOLATION OF 42 U.S.C. SECTION 1983

JURY DEMAND

Plaintiff alleges as follows:

JURISDICTION
1. This action arises under 42 U.S.C. Section 1983 for deprivation of rights 
   secured by the Constitution and laws of the United States.

PARTIES
2. Plaintiff is [description].
3. Defendant is [description].

FACTS
{case_data.get('facts', 'Facts to be added')}

CAUSES OF ACTION
First Cause of Action - 42 U.S.C. Section 1983
4. Defendant, acting under color of state law, deprived Plaintiff of rights 
   secured by the Constitution and laws of the United States.
5. Defendant's conduct was done willfully, intentionally, and under color of law.
6. Plaintiff has suffered damages as a result of Defendant's conduct.

WHEREFORE, Plaintiff demands:
A. Compensatory damages in the amount of $[amount]
B. Punitive damages
C. Attorney's fees and costs under 42 U.S.C. Section 1988
D. Such other relief as the Court deems just and proper

Respectfully submitted,

{case_data.get('plaintiff', 'Plaintiff')}
"""
        
        return {
            "document_type": "1983_complaint",
            "content": complaint,
            "instructions": [
                "Fill in all bracketed information",
                "File with court clerk",
                "Serve on all defendants",
                "Pay filing fee or file IFP motion"
            ]
        }
    
    def _generate_motion_to_dismiss(self, case_data: Dict) -> Dict:
        """Generate a motion to dismiss."""
        motion = f"""
UNITED STATES DISTRICT COURT
[DISTRICT]

{case_data.get('plaintiff', 'Plaintiff')}, )
    Plaintiff,         )
                        )  Case No.: {case_data.get('case_number', '[NUMBER]')}
vs.                     )
                        )
{case_data.get('defendant', 'Defendant')}, )
    Defendant.         )

DEFENDANT'S MOTION TO DISMISS PURSUANT TO FEDERAL RULE OF CIVIL PROCEDURE 12(b)(6)

TO THE HONORABLE COURT:

Comes now Defendant, by and through undersigned counsel, and moves this Court 
to dismiss Plaintiff's Complaint for failure to state a claim upon which relief 
can be granted, pursuant to Federal Rule of Civil Procedure 12(b)(6).

In support thereof, Defendant states as follows:

{case_data.get('arguments', 'Arguments to be added')}

WHEREFORE, Defendant respectfully requests that this Court:
1. Grant this Motion to Dismiss; and
2. Award Defendant its costs and attorney's fees incurred herein.

Respectfully submitted,

{case_data.get('defendant', 'Defendant')}
"""
        
        return {
            "document_type": "motion_to_dismiss",
            "content": motion,
            "instructions": [
                "Customize arguments based on specific legal deficiencies",
                "File with court and serve on all parties",
                "Schedule hearing date"
            ]
        }
    
    def _generate_rebuttal(self, case_data: Dict) -> Dict:
        """Generate a rebuttal using the rebuttal engine."""
        # Use the existing rebuttal engine
        keyword = case_data.get('keyword', case_data.get('issue', 'general'))
        
        import io
        import sys
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            try:
                generate_rebuttal_brief(keyword)
            except:
                pass
        
        output = f.getvalue()
        
        return {
            "document_type": "rebuttal",
            "content": output,
            "prompt": f"Use this system prompt with external LLM for full rebuttal generation"
        }
    
    def _generate_affidavit(self, case_data: Dict) -> Dict:
        """Generate an affidavit template."""
        affidavit = f"""
STATE OF {case_data.get('state', '[STATE]')}
COUNTY OF {case_data.get('county', '[COUNTY]')}

I, {case_data.get('name', '[NAME]')}, being first duly sworn upon oath, depose and state as follows:

1. My name is {case_data.get('name', '[NAME]')}. I am of legal age and competent to testify.
2. I have personal knowledge of the facts set forth herein.
3. If called as a witness, I could testify competently thereto.

{case_data.get('facts', 'Facts to be added - each paragraph should be numbered')}

I declare under penalty of perjury under the laws of the United States of America 
that the foregoing is true and correct.

Executed on {datetime.now().strftime('%B %d, %Y')}

_________________________
{case_data.get('name', '[NAME]')}

Notary acknowledgment section to be added
"""
        
        return {
            "document_type": "affidavit",
            "content": affidavit,
            "instructions": [
                "Sign before a notary public",
                "Each paragraph should be based on personal knowledge",
                "Number each paragraph",
                "Be specific with dates, times, and locations"
            ]
        }
    
    def _generate_motion_to_compel(self, case_data: Dict) -> Dict:
        """Generate a motion to compel discovery."""
        motion = f"""
UNITED STATES DISTRICT COURT
[DISTRICT]

{case_data.get('plaintiff', 'Plaintiff')}, )
    Plaintiff,         )
                        )  Case No.: {case_data.get('case_number', '[NUMBER]')}
vs.                     )
                        )
{case_data.get('defendant', 'Defendant')}, )
    Defendant.         )

PLAINTIFF'S MOTION TO COMPEL DISCOVERY RESPONSES

TO THE HONORABLE COURT:

Comes now Plaintiff and moves this Court for an Order compelling Defendant 
to provide complete and responsive answers to Plaintiff's discovery requests, 
pursuant to Federal Rule of Civil Procedure 37.

In support thereof, Plaintiff states as follows:

1. On {case_data.get('request_date', '[DATE]')}, Plaintiff served Defendant with 
   [type of discovery - e.g., Interrogatories, Requests for Production, etc.].
2. Defendant's responses, served on {case_data.get('response_date', '[DATE]')}, 
   are incomplete, evasive, and non-responsive.
3. Plaintiff has attempted to resolve this matter informally but has been unsuccessful.

{case_data.get('specific_issues', 'Specific issues to be added')}

WHEREFORE, Plaintiff respectfully requests that this Court:
1. Order Defendant to serve complete and responsive answers within 14 days;
2. Award Plaintiff costs and attorney's fees incurred in bringing this motion;
3. Grant such other relief as the Court deems just and proper.

Respectfully submitted,

{case_data.get('plaintiff', 'Plaintiff')}
"""
        
        return {
            "document_type": "motion_to_compel",
            "content": motion,
            "instructions": [
                "Specify exact discovery requests that are deficient",
                "Cite specific rules violated",
                "File with certificate of service",
                "Schedule hearing if required by local rules"
            ]
        }
    
    def _generate_discovery_request(self, case_data: Dict) -> Dict:
        """Generate discovery requests."""
        request_type = case_data.get('type', 'interrogatories')
        
        if request_type == 'interrogatories':
            content = self._generate_interrogatories(case_data)
        elif request_type == 'requests_for_production':
            content = self._generate_rfps(case_data)
        elif request_type == 'requests_for_admission':
            content = self._generate_rfas(case_data)
        else:
            content = "Specify request type"
        
        # Prepend DRAFT notice
        content = "DRAFT — NOT REVIEWED, DO NOT FILE\n\n" + content
        
        return {
            "document_type": f"discovery_{request_type}",
            "content": content,
            "instructions": [
                "Number each request",
                "Limit to [local rule limit, typically 25-35]",
                "Serve with certificate of service",
                "Allow 30-33 days for response"
            ]
        }
    
    def _generate_interrogatories(self, case_data: Dict) -> str:
        """Generate sample interrogatories."""
        return """
INTERROGATORIES TO DEFENDANT

INSTRUCTIONS: Answer each interrogatory separately and fully in writing under 
oath. Object to any interrogatory to which you object and state the grounds for the 
objection. Sign the answers under oath.

DEFINITIONS:
1. "You" or "your" means Defendant [Name].
2. "Plaintiff" means [Plaintiff Name].
3. "The Incident" means the events described in Plaintiff's Complaint.

INTERROGATORIES:

1. State your full name, address, and telephone number.
2. State the name and address of each person who has knowledge of the facts of this case.
3. Describe in detail all events surrounding the Incident.
4. State the date, time, and location of the Incident.
5. Identify all documents in your possession related to this case.
"""
    
    def _generate_rfps(self, case_data: Dict) -> str:
        """Generate requests for production."""
        return """
REQUESTS FOR PRODUCTION OF DOCUMENTS

INSTRUCTIONS: Produce all responsive documents in your possession, custody, 
or control. Organize and label documents to correspond with these requests.

REQUESTS:

1. All documents related to the Incident described in Plaintiff's Complaint.
2. All policies, procedures, or guidelines in effect at the time of the Incident.
3. All communications (emails, letters, memos, texts) between you and any other 
   person regarding the Incident.
4. All training materials you received related to your duties.
5. All reports, statements, or notes made by you or anyone else regarding the Incident.
"""
    
    def _generate_rfas(self, case_data: Dict) -> str:
        """Generate requests for admission."""
        return """
REQUESTS FOR ADMISSION

INSTRUCTIONS: Admit or deny each request. If you cannot truthfully admit or deny, 
state the reason. If you deny, state the basis for the denial.

REQUESTS:

1. Admit that the Incident described in Plaintiff's Complaint occurred.
2. Admit that you were acting in your official capacity at the time of the Incident.
3. Admit that Plaintiff's version of events, as stated in the Complaint, is accurate.
4. Admit that you violated Plaintiff's constitutional rights.
5. Admit that your actions were intentional.
"""
    
    def get_status(self) -> Dict:
        """Get current status of the orchestrator."""
        return {
            "agent": self.agent_name,
            "status": "active",
            "capabilities": self.capabilities,
            "active_tasks": list(self.active_tasks.keys()),
            "completed_tasks": list(self.completed_tasks.keys())[:10],  # Last 10
            "components": list(self.components.keys()),
            "last_updated": datetime.now().isoformat()
        }
    
    def emit_event(self, event_type: str, data: Any, priority: str = "normal") -> Dict:
        """Emit an event to the bus."""
        return self.bus.emit_event(event_type, data, priority)
    
    def get_events(self, event_type: str = None) -> List[Dict]:
        """Get events from the bus."""
        return self.bus.get_unread_events(
            agent_name=None if self.agent_name == "mistral_vibe" else "mistral_vibe",
            event_type=event_type
        )


# Singleton instance
_orchestrator = None


def get_orchestrator(agent_name="mistral_vibe"):
    """Get or create the singleton orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OutClawOrchestrator(agent_name)
    return _orchestrator


if __name__ == "__main__":
    print("=" * 80)
    print("OUTCLAW ORCHESTRATOR - MASTER COORDINATION SYSTEM")
    print("=" * 80)
    print()
    print("'A republic, if you can keep it.' - Benjamin Franklin")
    print("The responsibility to remain free is something we fight for every day.")
    print()
    print("=" * 80)
    
    orchestrator = get_orchestrator()
    
    # Check for other agents
    other_agents = orchestrator.check_other_agents()
    print(f"\n[+] Other agents detected: {len(other_agents)}")
    
    # Get status
    status = orchestrator.get_status()
    print(f"\n[+] Orchestrator Status:")
    print(f"  - Agent: {status['agent']}")
    print(f"  - Capabilities: {len(status['capabilities'])}")
    print(f"  - Components: {', '.join(status['components'])}")
    
    # Example: Run a quick analysis
    print("\n" + "=" * 80)
    print("EXAMPLE: Running Quick Analysis")
    print("=" * 80)
    
    test_case = "A police officer acting under color of law violated my 4th Amendment rights by searching my house without a warrant"
    print(f"\nCase: {test_case}")
    
    analysis = orchestrator.run_full_analysis(test_case)
    
    print("\nAnalysis Results:")
    assessment = analysis.get('assessment', {})
    if assessment:
        print(f"  Summary: {assessment.get('summary', ['N/A'])[0] if assessment.get('summary') else 'N/A'}")
        validation = assessment.get('validation')
        if validation:
            if validation.get('pass'):
                print("  [+] Validation Passed")
            else:
                print("  [-] Validation Failed:")
                for issue in validation.get('issues', []):
                    print(f"    - {issue}")
    
    if 'components' in analysis:
        if 'predicate' in analysis['components']:
            print(f"\n  Predicate Analysis:")
            for result in analysis['components']['predicate']:
                print(f"    - {result}")
        
        if 'constitutional' in analysis['components']:
            print(f"\n  Constitutional Analysis:")
            print(f"    - {analysis['components']['constitutional'].get('assessment', 'N/A')}")
        
        if 'tactics' in analysis['components']:
            print(f"\n  Recommended Tactics:")
            for tactic in analysis['components']['tactics'][:3]:
                print(f"    - {tactic.get('name', 'N/A')}")
    
    # Example: Generate a document
    print("\n" + "=" * 80)
    print("EXAMPLE: Document Generation")
    print("=" * 80)
    
    case_data = {
        "plaintiff": "John Doe",
        "defendant": "Officer Smith",
        "case_number": "1:24-cv-00123",
        "facts": "On January 1, 2024, Defendant entered Plaintiff's home without a warrant and seized property."
    }
    
    complaint = orchestrator.generate_document("complaint_1983", case_data)
    print(f"\nGenerated: {complaint.get('document_type')}")
    print(f"Instructions: {len(complaint.get('instructions', []))} steps")
    
    print("\n" + "=" * 80)
    print("[+] OutClaw Orchestrator Operational")
    print("[+] Multi-agent coordination active")
    print("[+] Ready for the swarm")
    print("=" * 80)
