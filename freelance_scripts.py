import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: freelance_scripts.py <tool_name> [args...]")
        print("Available tools:")
        tools_dir = Path(__file__).parent
        for tool_path in tools_dir.rglob("*_tool.py"):
            tool_name = tool_path.stem.replace("_tool", "")
            print(f"  {tool_name}")
        sys.exit(1)

    tool_name = sys.argv[1]
    tool_args = sys.argv[2:]

    tools_dir = Path(__file__).parent
    tool_path = None
    for path in tools_dir.rglob("*_tool.py"):
        if path.stem.replace("_tool", "") == tool_name:
            tool_path = path
            break

    if tool_path:
        command = ["python3", str(tool_path)] + tool_args
        subprocess.run(command)
    else:
        print(f"Tool '{tool_name}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()