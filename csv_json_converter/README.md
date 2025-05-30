

# 🧮 CSV ⇄ JSON Tool

A two-way data converter built in Python. Use it to transform:

- CSV → JSON (`c2j`)
- JSON → CSV (`j2c`)

Supports:
- Smart default filenames
- CLI or interactive usage
- Graceful error handling + logging

---

## 🚀 Usage

```bash
# Interactive mode
python csv_json_tool.py

# CSV → JSON
python csv_json_tool.py c2j example.csv

# JSON → CSV
python csv_json_tool.py j2c example.json

# With custom output
python csv_json_tool.py c2j input.csv output.json
```

## 📤 Input Example

```csv
name,age
Alice,30
Bob,25
```

## 📥 Output

```json
[
  { "name": "Alice", "age": "30" },
  { "name": "Bob", "age": "25" }
]
```

---

## 📜 License

MIT — use freely!

