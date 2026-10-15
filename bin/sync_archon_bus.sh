#!/bin/bash
# Sync Archon log status to Gemini CLI bus
ARCHON_LOG="/data/data/com.termux/files/home/MikeySwarm/logs/archon"
BUS_FILE="/storage/emulated/0/RootBase/modules/ccb_workbench_v1/.grimoire/bus/gemini-cli"

if [ -f "$ARCHON_LOG" ]; then
    LAST_ENTRY=$(tail -n 1 "$ARCHON_LOG" | sed 's/"/\\"/g')
    echo "{\"status\": \"online\", \"model\": \"gemini-3.1-flash-lite-preview\", \"last_archon_log\": \"$LAST_ENTRY\"}" > "$BUS_FILE"
fi
