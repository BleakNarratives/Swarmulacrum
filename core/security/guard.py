import sys, json, os

def validate_command(cmd):
    forbidden = ["rm -rf /", "mkfs", "dd if=/dev/zero"]
    for pattern in forbidden:
        if pattern in cmd:
            return False, f"OutClaw Security Block: Forbidden pattern '{pattern}' detected."
    return True, "Passed OutClaw Guard."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        valid, msg = validate_command(cmd)
        print(json.dumps({"valid": valid, "message": msg}))
