# 👀 Watch Automation Tool

> ## Purpose
> A utility that automatically updates your main project README tool table whenever any tool's `README.md` is changed.

---

## 🚦 Purpose

> - Monitors all tool directories for changes to their `README.md` files.
> - Automatically runs the `readme_updater_tool.py` to keep the main tool table in sync.
> - Logs all activity to both the terminal and a log file for easy auditing.
> - Excludes any tool directory containing a `.excluded` marker file.

---

## ⚙️ How It Works

- Scans all tool directories (excluding hidden/system and `.excluded` ones) for `README.md` files.
- Watches for changes (modifications or new files) every 2 seconds.
- When a change is detected, runs the `readme_updater_tool.py` script to regenerate the tool table in the main `README.md`.
- Logs all events and updater output to `watch_automation/watch_automation.log` and the terminal.

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

## 📜 License

MIT — use, modify, and share freely.
