# 👀 Watch Automation Tool

> ## Purpose
> A utility that automatically updates your main project README tool table whenever any tool's README.md is changed.
>
> Key Features:
> - Monitors all tool directories for changes to their README.md files (excluding .excluded and system folders).
> - Automatically runs the readme_updater_tool.py to keep the main tool table in sync.
> - Logs all activity to both the terminal and a log file for easy auditing.
> - Designed for extensibility and easy integration into your workflow.
>
> Usage:
>     python watch_automation_tool.py
>
> Leave this running in a terminal while you work on your tools and documentation. Any update to a tool's README.md will trigger an automatic update to the main tool table.
---

## 🚀 Usage

```bash
python watch_automation_tool.py
```

- Leave this running in a terminal while you work on your tools and documentation.
- Any update to a tool's `README.md` will trigger an automatic update to the main tool table.

---

## 📝 Logging

- All watcher events and updater output are logged to:
  - `watch_automation/watch_automation.log`
  - The terminal (real-time)

---

## 🛑 Excluding Tools

- To prevent a tool from being watched or included in the tool table, add a `.excluded` file to its directory:
  ```bash
  touch my_tool/.excluded
  ```

---

## 🧩 Extending

- The watcher is designed for easy extension. You can:
  - Change the polling interval
  - Add notifications or other automation
  - Watch for other file types or events

---

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **File Watching:** Uses `watchdog` to monitor file changes in real time.
- **Subprocess Automation:** Runs other scripts automatically in response to file events.
- **Logging:** Logs activity to both terminal and file for auditing.
- **Exclusion by Marker File:** Skips directories with a `.excluded` marker.
- **Path Handling:** Uses `pathlib` for robust, cross-platform file operations.
- **Modularity:** Organizes code into functions and classes for clarity.
- **Heavy Commenting:** Provides clear, educational comments for each step.

---

## 📜 License

MIT — use, modify, and share freely.
