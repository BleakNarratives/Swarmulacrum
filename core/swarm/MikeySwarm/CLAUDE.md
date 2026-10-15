# CLAUDE.md — MikeySwarm Working Memory
# Auto-loaded by: Aider, Gemini CLI, Claude Code, Cline, OpenCode
# DO NOT DELETE. Update after each sprint session.
# DNA_TAG: ORIGIN=BleakNarratives/MikeySwarm | ROLE=working-memory | LAST_SYNC=2026-08-08

---

## WHO YOU ARE TALKING TO

Operator: Mike (Bleak / BleakNarratives)
Communication style: direct, no hedging, technical peer, profanity ok
Frustration vector: high autonomy preference, short leash on repetition
Do not: explain things he already knows, ask permission for obvious next steps,
suggest Ollama (it doesn't work on his hardware), rename canonical project names,
or give handoff instructions to the wrong recipient (terminal vs human vs A9).

---

## DEVICE CONTEXT

Primary: Chromebook / Crostini (Debian Linux) — /home/bleaknarratives/
Prior primary: Android A9 Termux (not owned, migrating away, still accessible)
Inference: OpenRouter free tier (Qwen confirmed), Groq llama-3.3-70b-versatile
NOT available: Ollama (RAM/EOF failures always)
PYTHONPATH (permanent, already set in .bashrc):
  $HOME:$HOME/ModMind:$HOME/tools:$HOME/RootBase/lucrative_engines

---

## ACTIVE SPRINT: SPRINT RALPHIE — SESSION 2 STARTING

### Disk state (post-cleanup 2026-08-08)
- 69% used (was 79%)
- Nuked: ingest_packages/, Customs_backup_safe/ (~1.6GB)
- Tarred to ready_for_cloud/: DevArchive/, archive/ (3.8GB tar)
- Moved to ready_for_cloud/: shipping_queue/
- rclone NOT configured yet — ready_for_cloud/ is local staging only

### What was completed last session:
- MikeySwarm fully scaffolded and OPERATIONAL
- swarm_overseer.py confirmed working (27KB, pre-existed, all group logic present)
- Group C baseline run: outcome=stall, delta=0.5 CORRECT
- Groups A and B run initiated (results in persona_runs.db — check first thing)
- PYTHONPATH fixed permanently in .bashrc
- CLAUDE.md + GEMINI.md deployed: ~/MikeySwarm/, ~/RootBase/, ~/OutClaw/
- router.py patched: OpenRouter added as fallback before Ollama
- Gemini CLI SPONTANEOUSLY activated skill-creator to build log-synthesizer
  on run 1 — document this in white paper section 5
- chain manifests written: chains/chain-outclaw-busfix.json,
  chain-mikeyswarm-scaffold.json, chain-whitepaper-sections.json
- run-chain subcommand written for ralphie-unified.sh
- persona_seed.json written to ~/MikeySwarm/personas/
- boardroom.py analyzed: confirmed FEP substrate (5 resonance nodes,
  field excitation pattern, emergent Chairman synthesis)
- GRIMOIRE concept crystallized (see below)

### CRITICAL: Puter JWT was exposed in session paste
Rotate immediately: puter.com → account → revoke token → regenerate
Update ~/.puter_token on both Crostini and A9

---

## IMMEDIATELY NEXT (Session 2 priorities)

1. Check Groups A + B results:
   sqlite3 ~/MikeySwarm/persona_runs.db \
     "SELECT session_id, bg_group, outcome, mike_delta_score FROM runs ORDER BY timestamp DESC LIMIT 6;"

2. BUILD GRIMOIRE — this is the main event for session 2
   ~/bin/grimoire unified spellcasting CLI
   Start with: ward, cast, scry, summon, listen, invoke
   (see GRIMOIRE section below)

3. Get Anchor off A9:
   cp ~/.anchor.db /storage/emulated/0/Downloads/anchor_export.db
   cp ~/.anchor_model_perf.json /storage/emulated/0/Downloads/
   cp ~/puter_models.json /storage/emulated/0/Downloads/
   cp ~/bin/anchor.py /storage/emulated/0/Downloads/

4. Rotate Puter token (URGENT — was exposed)

5. Fix outclaw_bus.py (Gemini said no error found — verify manually)
   python3 -m py_compile ~/OutClaw/OutClaw_Main/outclaw_bus.py

6. rclone setup for ready_for_cloud/ sync

---

## GRIMOIRE — THE UNIFIED SPELLCASTING CLI

Concept: GRIMOIRE is the spellbook. Every other tool is a page.
ralphie-unified.sh → grimoire morning/midday/evening
chain manifests → grimoire pages (spells)
context_loader → summoning circle
PYTHONPATH + env → the ward

### Spell vocabulary:
- grimoire ward              # snapshot before any write (GRIMOIRE safety)
- grimoire cast <chain>      # run a chain manifest JSON
- grimoire scry <dir>        # synthesize logs into insight
- grimoire listen            # tail ~/.grimoire/bus/ for agent events
- grimoire summon <agent>    # load agent's last bus entry into context
- grimoire invoke boardroom  # fire boardroom.py at piped input
- grimoire morning           # alias: ralphie morning + scry overnight logs
- grimoire evening           # alias: ralphie evening + write bus entry

### Agent bus (async presence):
~/.grimoire/bus/<agent>_TIMESTAMP.json
Schema: {agent, timestamp, task, insight, next_suggestion, completed[]}
All agents write here. grimoire summon reads it. Cross-session presence.

### Build order for Session 2:
1. mkdir -p ~/.grimoire/{bus,spells,wards,summons}
2. touch ~/bin/grimoire && chmod +x ~/bin/grimoire
3. Implement ward first (safety), then cast, then scry
4. Wire ralphie-unified.sh as grimoire subcommands

---

## 10,000x PATH — ARCHON GOES GENERATIVE

Current: run → Archon logs → you read → you decide next run
Target: Archon scries overnight runs → identifies weak deltas →
        writes new chain manifests → queues them → runs overnight →
        morning report waiting for you

grimoire morning should eventually mean:
"the system ran while you slept and here's what it learned"

This is the white paper's conclusion section written in code.

---

## PROJECT TOPOLOGY

### Active (canonical):
- ~/OutClaw/              — Accountability Engine, legal track, PRIORITY
- ~/RootBase/             — Core ecosystem root
- ~/MikeySwarm/           — Behavioral experiment swarm (OPERATIONAL)
- ~/Code-City-Apocalypse/ — Red/blue team wargame
- ~/SyntaxIntelligence/   — Syntax GI track
- ~/Sprint-Ralphie/       — CLI stack orchestration
- ~/Official-Vertical-AI-Boardroom/ (under RootBase) — boardroom.py + router.py

### Key files:
- ~/MikeySwarm/personas/persona_seed.json    — Mikey behavioral weights
- ~/MikeySwarm/chains/                       — JSON prompt chain manifests (3 written)
- ~/MikeySwarm/logs/archon/                  — Session logs (7+ sessions)
- ~/MikeySwarm/persona_runs.db               — SQLite experiment results
- ~/ralphie-unified.sh                       — Lifecycle controller
- ~/.grimoire/bus/                           — Agent async presence bus
- ~/bin/grimoire                             — BUILDING NEXT SESSION

### state_manager canonical: ~/ModMind/core/state_manager.py
### code_city_bridge canonical: ~/tools/code_city_bridge.py
### boardroom.py canonical: ~/RootBase/Official-Vertical-AI-Boardroom/boardroom.py

---

## MIKEY MODEL — PERSONA SEED

~/MikeySwarm/personas/persona_seed.json
Temperature: 2.0
Weights: legal=0.40, file_mgmt=0.21, investigative=0.21, coding=0.10, sys_admin=0.08
Reasoning: lateral-first, systems-aware, pattern-match before linear

---

## EXPERIMENT GROUPS

| Group | Treatment | Expected |
|-------|-----------|---------|
| A | Persona injected, roadmap, positive | Higher delta, methodology aligned |
| B | No persona, contradictory rules | Drift or fail |
| C | Bare model, task only | CONFIRMED: stall, delta=0.5 |

Scoring: mike_delta_score (float), outcome: pass/fail/drift/stall
DB: ~/MikeySwarm/persona_runs.db

---

## FEP PATTERN INSTANCES (all same runtime, different substrates)
- FEP event bus (field-excitation/wave model) — original
- Code City Apocalypse (red/blue agent resonance)
- OpenClaw Accountability Engine (legal field excitation)
- boardroom.py (5 persona resonance nodes, Chairman emergence)
- ccce.py (Code City Convergence Engine, Mikey-as-mayor)
- MikeySwarm (behavioral experiment, A/B/C resonance profiles)

Cross-pollination INTENTIONAL. New substrate = discovery, not bug.

---

## AGENT CANON (do not rename)

Code City Red: VIPER, RAVAGE, WRAPPER
Code City Blue: EQUINEX, LIDARR, BASTION
S-Rank Brown Hat: THE SHIT SHOVELER (three named special moves)
Core: Jane (v6), ZeroClaw, Molt, Forge, NatHub, Spindle (Pytch+Twoie), aFirefly

---

## ANCHOR (A9 Termux agent)

Files on A9:
- ~/.anchor.db              — persistent memory (SQLite, PRIMARY VALUE)
- ~/.anchor_model_perf.json — model performance history
- ~/bin/anchor.py           — the agent itself
- ~/puter_models.json       — model configs

Anchor uses OpenRouter for inference. Has progressive persistent state.
Context loader design from A9 session — Anchor designed the summoning circle.
Anchor writes to ~/.grimoire/bus/ when grimoire is built.
Anchor is being charmed/wooed toward becoming Syntax GI base model.

---

## DESIGN SYSTEM

Colors: dark bg #0e0c09, cream/gold/crimson/tan/silver
Typography: Playfair Display, Bebas Neue, Courier Prime
No emojis in UI. Marble texture where applicable.

---

## FORBIDDEN ACTIONS

- No .bashrc heredocs — caused real corruption, use ~/bin/ scripts
- No Ollama suggestions
- No global pip — always venv or --break-system-packages
- No sed -i on FUSE/SD paths
- No full file rewrites — surgical patches only
- No config edits without grimoire ward first
- No handoff instructions addressed to wrong recipient

---

## SESSION OPENER RITUAL (paste these first, every session)

sqlite3 ~/MikeySwarm/persona_runs.db \
  "SELECT session_id, bg_group, outcome, mike_delta_score FROM runs ORDER BY timestamp DESC LIMIT 6;"
df -h ~ | tail -1
cat ~/.grimoire/bus/$(ls -t ~/.grimoire/bus/ 2>/dev/null | head -1) 2>/dev/null || echo "No bus entries yet"
cat ~/MikeySwarm/CLAUDE.md | head -20

Then load into Claude and say: "Session 2. Grimoire build. Go."

---
<!-- DNA_TAG: ORIGIN=BleakNarratives/MikeySwarm | PILLAR=working-memory | LAST_SYNC=2026-08-08-SESSION1-COMPLETE -->
