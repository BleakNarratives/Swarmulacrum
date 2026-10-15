"""
[DNA_TAG]
ORIGIN: Moto4_A9
PILLAR: valet_concierge
PATH: model_spar_simulator.py
LAST_SYNC: 2026-08-02T01:13:30Z
[/DNA_TAG]
"""
#!/usr/bin/env python3
"""
ModelSparSimulator — multi-angle adversarial spar for legal narratives.

Recovered from orphan cpython-314 bytecode (ghost module had no .py),
then upgraded: one model stub became a full spar ring.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# --- persona blades (each "model" is a spar angle, not a cloud call) ---
PERSONAS: Dict[str, Dict[str, str]] = {
    "scalia_text": {
        "label": "Textualist Blade",
        "bias": "If the statute does not say it, authority does not exist.",
        "attack": "Demand the exact clause granting power; deny freestanding 'policy' justifications.",
    },
    "bailey_cross": {
        "label": "Cross-Exam Blade",
        "bias": "Timeline and record contradictions destroy credibility.",
        "attack": "Pin every official statement against body-cam, dispatch, docket, and prior sworn words.",
    },
    "bugliosi_close": {
        "label": "Closing Blade",
        "bias": "Immunity talk is smoke when oath + willful breach are on the table.",
        "attack": "Walk the jury/judge through motive, means, opportunity, and color-of-law chain.",
    },
    "spence_open": {
        "label": "Narrative Blade",
        "bias": "The human story of rights deprivation must land before jargon.",
        "attack": "Open with the right taken, the actor who took it, and the power they wore while doing it.",
    },
    "texas_prosecutor": {
        "label": "Malfeasance Blade",
        "bias": "Ministerial duty ignored is not 'discretion' — it is breach.",
        "attack": "Separate discretionary judgment from non-discretionary mandates; document the bypass.",
    },
}


@dataclass
class SparResult:
    model: str
    label: str
    reaction: str
    disagreements: List[str]
    gaps: List[str]
    attack_line: str
    statutes_hint: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ModelSparSimulator:
    """
    Original recovered API:
      ModelSparSimulator(model_name) -> simulate_reaction(target) -> dict

    Extended:
      spar_all(target, facts=None) -> multi-persona clash report
    """

    DEFAULT_STATUTES = [
        "42 U.S.C. § 1983",
        "18 U.S.C. § 241",
        "18 U.S.C. § 242",
        "U.S. Const. amend. IV / XIV",
    ]

    def __init__(self, model_name: str = "scalia_text"):
        self.model_name = model_name
        key = model_name if model_name in PERSONAS else "scalia_text"
        self._persona = PERSONAS[key]
        if model_name not in PERSONAS:
            # custom name still works (recovered behavior)
            self._persona = {
                "label": model_name,
                "bias": f"Adversarial analysis under persona '{model_name}'.",
                "attack": "Force the opposing narrative to cite record, statute, and duty — or fold.",
            }

    def simulate_reaction(self, target: str) -> Dict[str, Any]:
        """Bytecode-faithful shape + richer fields for the breakfast pack."""
        label = self._persona.get("label", self.model_name)
        reaction = (
            f"Legal analysis for {target} by {self.model_name}. "
            f"{self._persona.get('bias', '')}"
        ).strip()
        disagreements = self._disagreements(target)
        gaps = self._gaps(target)
        return {
            "model": self.model_name,
            "label": label,
            "reaction": reaction,
            "disagreements": disagreements if disagreements else ["None"],
            "gaps": gaps if gaps else ["Requires more discovery material."],
            "attack_line": self._persona.get("attack", ""),
            "statutes_hint": list(self.DEFAULT_STATUTES),
        }

    def _disagreements(self, target: str) -> List[str]:
        t = target.lower()
        out: List[str] = []
        if "immun" in t:
            out.append("Qualified immunity is not a free pass for willful or clearly established rights violations.")
        if "discretion" in t or "policy" in t:
            out.append("Discretion cannot invent power the enabling statute never granted.")
        if "good faith" in t:
            out.append("'Good faith' is a fact question — not a magic word that erases the record.")
        if not out:
            out.append("Opposing narrative fails to tether each act to a specific lawful grant of authority.")
        return out

    def _gaps(self, target: str) -> List[str]:
        return [
            "Requires more discovery material.",
            f"Need primary record for: {target[:80]}",
            "Need oath/commission, duty manual excerpt, and contemporaneous logs.",
        ]

    @classmethod
    def spar_all(
        cls,
        target: str,
        personas: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        keys = personas or list(PERSONAS.keys())
        rounds = [cls(name).simulate_reaction(target) for name in keys]
        return {
            "target": target,
            "rounds": rounds,
            "synthesis": cls._synthesize(target, rounds),
        }

    @staticmethod
    def _synthesize(target: str, rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        attacks = [r.get("attack_line", "") for r in rounds if r.get("attack_line")]
        gaps: List[str] = []
        for r in rounds:
            for g in r.get("gaps") or []:
                if g not in gaps:
                    gaps.append(g)
        return {
            "headline": f"SPAR COMPLETE — {target}",
            "pressure_points": attacks,
            "discovery_stack": gaps,
            "breakfast_line": (
                "Opposing counsel's comfort narrative does not survive multi-blade spar: "
                "text, cross, close, story, and malfeasance all demand the same thing — "
                "record + statute + duty, or concession."
            ),
        }


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        target = "Civil Rights Litigation"
        report = ModelSparSimulator.spar_all(target)
    elif argv[0] == "--one":
        model = argv[1] if len(argv) > 1 else "TestModel"
        target = " ".join(argv[2:]) if len(argv) > 2 else "Civil Rights Litigation"
        report = ModelSparSimulator(model).simulate_reaction(target)
    else:
        target = " ".join(argv)
        report = ModelSparSimulator.spar_all(target)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
