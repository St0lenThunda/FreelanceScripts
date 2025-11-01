# GEMINI.md

## Project Overview

This project is a collection of Python scripts designed as a "starter pack" for freelancers. The scripts are standalone, interactive, and well-documented, making them suitable for both practical use and learning. The project emphasizes clear, commented code and consistent structure.

The main technologies used are:

*   **Python 3.8+**
*   Standard Python libraries such as `argparse`, `csv`, `json`, `pathlib`, and `os`.
*   Third-party libraries like `requests`, `BeautifulSoup`, and `watchdog` (though no `requirements.txt` is provided).

The project is organized into a series of directories, each containing a specific tool. Each tool has its own `README.md` file with detailed instructions. A central `executioner.py` script is provided to make the tools executable and add them to the system's PATH.

## Building and Running

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/St0lenThunda/FreelanceScripts
    cd FreelanceScripts
    ```

2.  Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install dependencies (if any):
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is not currently present in the project, but this is the standard way to install dependencies if it were added.)*

### Running the Tools

To make all tools executable and accessible from the command line, run the `executioner.py` script:

```bash
python executioner/executioner_tool.py
```

This will create a `bin` directory with symlinks to all the tools. You can then run any tool by its name, for example:

```bash
csv_to_json_converter_tool.py --help
```

Alternatively, you can run each tool directly using the Python interpreter:

```bash
python csv_json_converter/csv_to_json_converter_tool.py
```

## Development Conventions

*   **Structure:** Each tool is contained in its own directory.
*   **Naming:** Tool scripts are named with a `_tool.py` suffix (e.g., `csv_json_converter_tool.py`).
*   **Documentation:** Each tool has its own `README.md` file that explains its purpose, usage, and the Python concepts it demonstrates.
*   **Excluding Tools:** To exclude a tool from the build process, create an empty file named `.excluded` in the tool's directory.
*   **Code Style:** The code is heavily commented to be educational.
