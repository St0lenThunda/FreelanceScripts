from nbformat import v4 as nbf
import nbformat

# Create notebook cells
cells = []

cells.append(nbf.new_markdown_cell("# 🔍 Log Analyzer + Alert Generator\n\nA simple Python-based log analyzer that summarizes event types and raises alerts when thresholds are crossed. Useful for demonstrating debugging, performance monitoring, and modular design."))

cells.append(nbf.new_code_cell("""import pandas as pd
import numpy as np
import logging
from datetime import datetime
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
"""))

cells.append(nbf.new_markdown_cell("## 📁 Load Sample Logs"))

cells.append(nbf.new_code_cell("""sample_data = [
    {"timestamp": "2025-07-20 12:01", "event": "login_success", "user": "alice"},
    {"timestamp": "2025-07-20 12:02", "event": "login_failure", "user": "bob"},
    {"timestamp": "2025-07-20 12:03", "event": "error_500", "user": "system"},
    {"timestamp": "2025-07-20 12:04", "event": "login_failure", "user": "bob"},
    {"timestamp": "2025-07-20 12:05", "event": "login_success", "user": "charlie"},
]

df = pd.DataFrame(sample_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.head()
"""))

cells.append(nbf.new_markdown_cell("## 📊 Visualize Event Distribution"))

cells.append(nbf.new_code_cell("""event_counts = df['event'].value_counts()
event_counts.plot(kind='bar', title='Event Distribution', figsize=(8, 4))
plt.xlabel('Event Type')
plt.ylabel('Count')
plt.grid(True)
plt.tight_layout()
plt.show()
"""))

cells.append(nbf.new_markdown_cell("## 🚨 Detect Basic Anomalies"))

cells.append(nbf.new_code_cell("""def detect_anomalies(df, event="login_failure", threshold=2):
    failures = df[df["event"] == event]
    if len(failures) >= threshold:
        logging.warning(f"High volume of {event}: {len(failures)} events")
        return True
    return False

anomaly = detect_anomalies(df)
print("Anomaly Detected:", anomaly)
"""))

cells.append(nbf.new_markdown_cell("## 📦 Modularize Log Analysis"))

cells.append(nbf.new_code_cell("""def analyze_log(dataframe, alert_thresholds=None):
    alert_thresholds = alert_thresholds or {"login_failure": 3, "error_500": 1}
    summary = dataframe['event'].value_counts().to_dict()
    alerts_triggered = {}
    
    for event, threshold in alert_thresholds.items():
        count = summary.get(event, 0)
        if count >= threshold:
            alerts_triggered[event] = count
            logging.warning(f"[ALERT] {event.upper()} occurred {count} times!")

    return summary, alerts_triggered

summary, alerts = analyze_log(df)
summary, alerts
"""))

# Build notebook
nb = nbf.new_notebook(cells=cells)
notebook_path = "../notebooks/Log_Analyzer_Demo.ipynb"

# Save notebook to file
with open(notebook_path, "w") as f:
    nbformat.write(nb, f)

notebook_path
