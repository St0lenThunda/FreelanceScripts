"""
This script creates a NiceGUI dashboard for managing and running various tools stored in
different directories, with each tool having its own specific functionality and interface elements.

:param path: The `path` parameter in the provided code refers to a file path represented as a `Path`
object from the `pathlib` module. This parameter is used in various functions within the script to
interact with files and directories, such as checking if a file is a valid tool, reading the README
:type path: Path
:return: The code you provided is a Python script that creates a NiceGUI dashboard for managing and
running various tools. The script defines functions for finding valid tools, reading README files,
launching tools, and rendering tool-specific UI elements based on the tool's type.
"""
import os
import subprocess
from pathlib import Path

# Try/catch for robustness
try:
    from nicegui import ui, app, context
    from nicegui.element import Element
    from importlib.util import spec_from_file_location, module_from_spec
except ImportError as e:
    print("ImportError detected:", e)
    print("Attempting to install missing dependencies...")
    subprocess.check_call(['pip', 'install', 'nicegui'])
    from nicegui import ui, app, context
    from nicegui.element import Element
    from importlib.util import spec_from_file_location, module_from_spec

TOOL_SUFFIX = '_tool.py'
EXCLUDED_MARKER = '.excluded'


def is_valid_tool(path: Path) -> bool:
    if not path.name.endswith(TOOL_SUFFIX):
        return False
    if any((path.parent / EXCLUDED_MARKER).exists() for _ in [0]):
        return False
    return True


def get_tools():
    tools = []
    for dirpath, dirnames, filenames in os.walk("."):
        for file in filenames:
            if file.endswith(TOOL_SUFFIX):
                full_path = Path(dirpath) / file
                if is_valid_tool(full_path):
                    tools.append(full_path)
    return tools



def read_readme(path: Path):
    """
    Extracts the first heading and the 'Purpose' section from the README.md file in the tool's directory.
    Returns (heading, purpose) tuple. If not found, returns fallback values.
    """
    readme_path = path.parent / 'README.md'
    if not readme_path.exists():
        return ("(No README found)", "(No Purpose found)")
    heading = None
    purpose = None
    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find first heading (e.g. '# ...' or '## ...')
    for line in lines:
        if line.strip().startswith('#'):
            heading = line.strip().lstrip('#').strip()
            break
    # Find Purpose section
    in_purpose = False
    purpose_lines = []
    for line in lines:
        if line.strip().lower().startswith('> ## purpose'):
            in_purpose = True
            continue
        if in_purpose:
            if line.strip().startswith('> ##') and not line.strip().lower().startswith('> ## purpose'):
                break
            # Stop at next heading or empty line after content
            if line.strip() == '' and purpose_lines:
                break
            if line.strip() != '':
                purpose_lines.append(line.strip())
    if purpose_lines:
        purpose = '\n'.join(purpose_lines)
    if not heading:
        heading = "(No Heading found)"
    if not purpose:
        purpose = "(No Purpose found)"
    return (heading, purpose)


def launch_tool(path: Path):
    try:
        subprocess.Popen(['python', str(path)], cwd=path.parent)
    except Exception as e:
        print(f"Error launching {path.name}: {e}")



def render_tool(tool_path: Path):
    heading, purpose = read_readme(tool_path)
    # The line `with ui.card().classes("m-2 p-4 bg-slate-800 text-white w-3/4"):` is creating a card
    # element in the NiceGUI interface with specific styling classes applied to it. Here's a breakdown
    # of what each part of the line is doing:
    with ui.card().classes("m-2 p-4 bg-slate-800 text-white w-3/4"):
        ui.label(f"{heading}").classes("text-lg font-semibold")
        ui.label(f"📁 Folder: {tool_path.parent}").classes("text-sm text-gray-400")
        ui.markdown(f"📝 {purpose}") #.classes("text-sm italic mb-2")

        stem = tool_path.stem
        if 'csv_json_converter' in stem:
            ui.upload(label='Upload File').on_upload(lambda e: print("Uploaded", e.name))
            ui.select(['CSV to JSON', 'JSON to CSV'], value='CSV to JSON')
            ui.button('Convert')
            ui.label('🧾 Input Preview (TBD)').classes("text-sm")
            ui.label('📄 Output Preview (TBD)').classes("text-sm")

        elif 'simple_scraper' in stem:
            url_input = ui.input("Enter URL to scrape")
            ui.button("Scrape", on_click=lambda: print(f"Scraping: {url_input.value}"))
            ui.checkbox("Download JSON")

        elif 'scraper_buggy' in stem or 'scraper_bugfix' in stem:
            ui.button("Run Both Versions (Buggy/Fix)", on_click=lambda: print("Running both versions"))
            ui.label("🔍 Compare output/errors side-by-side below").classes("text-sm")

        elif 'executioner' in stem:
            tools = get_tools()
            dropdown = ui.select([t.name for t in tools])
            ui.button("Run Selected", on_click=lambda: launch_tool(next(t for t in tools if t.name == dropdown.value)))

        elif 'package_toolkit' in stem:
            ui.button("📦 Package Toolkit", on_click=lambda: print("Packaging..."))
            ui.label("🧾 Included/Skipped Files (TBD)").classes("text-sm")

        elif 'readme_updater' in stem:
            ui.button("📝 Update README", on_click=lambda: print("Updating README..."))
            ui.label("🔁 Preview Changes (TBD)")

        elif 'watch_automation' in stem:
            ui.button("▶ Start Watching", on_click=lambda: print("Watching..."))
            ui.button("⏹ Stop Watching", on_click=lambda: print("Stopped."))
            ui.label("📜 Event Log Console (TBD)")

        else:
            ui.button("▶️ Run Tool", on_click=lambda p=tool_path: launch_tool(p)).classes("bg-blue-600 hover:bg-blue-700 text-white")





tools = get_tools()
tab_info = []
for tool in tools:
    heading, _ = read_readme(tool)
    tab_info.append((tool, heading))

# Sidebar layout with selection
selected_idx = 0

def set_selected(idx):
    global selected_idx
    selected_idx = idx
    show_selected.refresh()

with ui.row().classes("w-full"):
    with ui.column().classes("w-1/4 bg-slate-900 text-white h-screen p-4 sticky top-0"):
        ui.label("🧰 Available Tools").classes("text-xl font-bold mb-4")
        for i, (_, heading) in enumerate(tab_info):
            with ui.row().classes(f"items-center cursor-pointer p-2 rounded {'bg-slate-700' if i == selected_idx else 'hover:bg-slate-700'}"):
                # ui.icon("description")
                ui.label(heading).on("click", lambda v=i: set_selected(v))

    with ui.column().classes("w-3/4 p-6"):
        def show_selected():
            if tab_info:
                tool, _ = tab_info[selected_idx]
                render_tool(tool)
            else:
                ui.label("No tools found.").classes("text-gray-400 italic")
        show_selected = ui.refreshable(show_selected)
        show_selected()





ui.run(title="FreelanceScripts NiceGUI Dashboard")