# 🛠️ Tool Runner

> ## Purpose
> A unifying script to run all tools in the FreelanceScripts project. This script provides a menu-based interface for selecting and running any tool interactively.
>
> Key Features:
> - Lists all available tools dynamically.
> - Provides descriptions and usage instructions for each tool.
> - Allows users to run tools directly from the menu.
> - Handles errors gracefully and provides feedback.
> - Supports interactive argument selection for tools.
> - Includes a help option to display detailed usage information for each tool.
>
> Intended as a learning resource: code is heavily commented to explain each step and concept.
### Use Cases
- Quickly access and run any tool in the project.
- Provide a unified interface for managing tools.
- Simplify tool usage for non-technical users.
- Demonstrate menu-based CLI design.

## 🚀 Usage

```bash
python toolkit_runner_tool.py
```

- Run the script to see a menu of all available tools.
- Select a tool by entering its corresponding number.
- Use the `-1` option to display help for a specific tool.
- Follow the instructions provided by the tool.
- Enter arguments interactively when prompted.

## Notes

- Ensure all tools are properly configured and executable.
- This script is designed for Unix-like systems (Linux, macOS, WSL).

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **Dynamic Tool Discovery:** Lists tools dynamically based on the project structure.
- **Menu-Based CLI:** Provides an interactive menu for tool selection and execution.
- **Error Handling:** Gracefully handles invalid inputs and tool execution errors.
- **Extensibility:** Designed to easily add new tools and features.

## License

MIT License. Use freely and modify as needed.
