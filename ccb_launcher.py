import sys
import os
import subprocess

CORE_ENGINE = "/storage/emulated/0/RootBase/modules/ccb_workbench_v1/core/janus_loop.py"

def run_cmd(args):
    command = args[0]
    script = args[1] if len(args) > 1 else None
    
    if command == "run" or command == "heal":
        subprocess.run(['python3', CORE_ENGINE, script])
    elif command == "status":
        print("Janus Engine Status: Active")
        print(f"Log Path: /data/data/com.termux/files/home/MikeySwarm/logs/archon")
    else:
        print("Unknown command. Usage: ccb-launch [run|heal|status] [script]")

if __name__ == "__main__":
    run_cmd(sys.argv[1:])
