import sys, ast, json

def parse_ast(filepath):
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}
    try:
        with open(filepath, "r") as f:
            tree = ast.parse(f.read())
        return {
            "file": filepath,
            "classes": [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)],
            "functions": [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import os
        print(json.dumps(parse_ast(sys.argv[1]), indent=2))
