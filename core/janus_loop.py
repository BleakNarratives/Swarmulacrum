import subprocess
import os
import sys
from core.security.guard import validate_call

def secure_execute(command_str):
    # Validate against our guard
    if not validate_call(command_str):
        return False, "Security Block: Command pattern rejected."
    
    # Use subprocess.run with list instead of os.system
    cmd = command_str.split()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Logic: use XDG_CONFIG_HOME if available, fallback to HOME
    BASE_DIR = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~"))
    print(f"Janus Loop initialized at {BASE_DIR}")
    
    if len(sys.argv) > 1:
        success, output = secure_execute(sys.argv[1])
        print(f"Result: {success}, {output}")
