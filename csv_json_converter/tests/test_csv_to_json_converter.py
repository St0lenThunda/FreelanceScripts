import subprocess
import json
import os

def test_csv_to_json_valid(tmp_path):
    """Test CSV to JSON conversion with a valid CSV file."""
    output_file = tmp_path / "output.json"
    result = subprocess.run(["python3", "csv_json_converter/csv_to_json_converter_tool.py", "--csv-to-json", "csv_json_converter/tests/test_data/valid.csv", str(output_file)], capture_output=True, text=True)
    assert result.returncode == 0
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == [{"name": "John", "age": "30", "city": "New York"}, {"name": "Peter", "age": "40", "city": "San Francisco"}]

def test_csv_to_json_non_existent():
    """Test CSV to JSON conversion with a non-existent CSV file."""
    result = subprocess.run(["python3", "csv_json_converter/csv_to_json_converter_tool.py", "--csv-to-json", "non_existent.csv", "output.json"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "file not found" in result.stdout.lower()

def test_csv_to_json_empty(tmp_path):
    """Test CSV to JSON conversion with an empty CSV file."""
    output_file = tmp_path / "output.json"
    result = subprocess.run(["python3", "csv_json_converter/csv_to_json_converter_tool.py", "--csv-to-json", "csv_json_converter/tests/test_data/empty.csv", str(output_file)], capture_output=True, text=True)
    assert result.returncode == 0
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == []

def test_json_to_csv_valid(tmp_path):
    """Test JSON to CSV conversion with a valid JSON file."""
    output_file = tmp_path / "output.csv"
    result = subprocess.run(["python3", "csv_json_converter/csv_to_json_converter_tool.py", "--json-to-csv", "csv_json_converter/tests/test_data/valid.json", str(output_file)], capture_output=True, text=True)
    assert result.returncode == 0
    with open(output_file, 'r') as f:
        data = f.read()
    expected_data = "name,age,city" + os.linesep + "John,30,New York" + os.linesep + "Peter,40,San Francisco" + os.linesep
    assert data == expected_data

def test_json_to_csv_non_existent():
    """Test JSON to CSV conversion with a non-existent JSON file."""
    result = subprocess.run(["python3", "csv_json_converter/csv_to_json_converter_tool.py", "--json-to-csv", "non_existent.json", "output.csv"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "file not found" in result.stdout.lower()

def test_json_to_csv_empty(tmp_path):
    """Test JSON to CSV conversion with an empty JSON file."""
    output_file = tmp_path / "output.csv"
    result = subprocess.run(["python3", "csv_json_converter/csv_to_json_converter_tool.py", "--json-to-csv", "csv_json_converter/tests/test_data/empty.json", str(output_file)], capture_output=True, text=True)
    assert result.returncode == 0
    assert output_file.exists()
    with open(output_file, 'r') as f:
        data = f.read()
    assert data == ""