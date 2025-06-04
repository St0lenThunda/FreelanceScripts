#!/usr/bin/env python3
"""
toolkit_runner_tool.py

A unifying script to run all tools in the FreelanceScripts project. This script provides a menu-based interface for selecting and running any tool interactively.

Key Features:
- Lists all available tools dynamically.
- Provides descriptions and usage instructions for each tool.
- Allows users to run tools directly from the menu.
- Handles errors gracefully and provides feedback.
- Supports interactive argument selection for tools.
- Includes a help option to display detailed usage information for each tool.

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""
import subprocess
from pathlib import Path

# Define the root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the tools directory
TOOLS_DIR = PROJECT_ROOT

# Define a mapping of tool names to their script paths and descriptions
TOOLS = {
    "CSV ⇄ JSON Converter": {
        "script": TOOLS_DIR / "csv_json_converter/csv_to_json_converter_tool.py",
        "description": "Converts CSV files to JSON format and vice versa."
    },
    "Scraper Debug Demo": {
        "script": TOOLS_DIR / "debug_demo/scraper_bugfix_tool.py",
        "description": "Demonstrates debugging and refactoring of a web scraper."
    },
    "Executioner Tool": {
        "script": TOOLS_DIR / "executioner/executioner_tool.py",
        "description": "Automates making Python scripts executable and symlinking them into a bin directory."
    },
    "Package Toolkit": {
        "script": TOOLS_DIR / "package_toolkit/package_toolkit_tool.py",
        "description": "Packages all tools into a single zip archive."
    },
    "README Updater": {
        "script": TOOLS_DIR / "readme_updater/readme_updater_tool.py",
        "description": "Updates the main project README and tool READMEs dynamically."
    },
    "Watch Automation Tool": {
        "script": TOOLS_DIR / "watch_automation/watch_automation_tool.py",
        "description": "Automatically updates the main project README tool table when tool READMEs change."
    }
}

def display_menu():
    print("\nAvailable Tools:")
    for idx, (tool_name, tool_info) in enumerate(TOOLS.items(), start=1):
        print(f"{idx}. {tool_name} - {tool_info['description']}")

def run_tool(choice, help_option=False, args=None):
    try:
        tool_name = list(TOOLS.keys())[choice - 1]
        tool_script = TOOLS[tool_name]["script"]
        print(f"\nRunning {tool_name}...")
        command = ["python", tool_script]
        if help_option:
            command.append("--help")
        if args:
            command.extend(args.split())
        subprocess.run(command, check=True)
    except IndexError:
        print("Invalid choice. Please select a valid tool.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {tool_name}: {e}")

def main():
    while True:
        display_menu()
        try:
            choice = int(input("\nEnter the number of the tool to run (or 0 to exit, or -1 for help): "))
            if choice == 0:
                print("Exiting Tool Runner. Goodbye!")
                break
            elif choice == -1:
                help_choice = int(input("\nEnter the number of the tool to get help for: "))
                run_tool(help_choice, help_option=True)
            else:
                print("\nInteractive Argument Selection:")
                args = []
                while True:
                    arg = input("Enter an argument (or press Enter to finish): ")
                    if not arg:
                        break
                    args.append(arg)
                run_tool(choice, args=" ".join(args))
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
