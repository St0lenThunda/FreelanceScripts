import unittest
import os
import json
import csv
import tempfile
from pathlib import Path
from csv_json_converter.csv_to_json_converter_tool import csv_to_json, json_to_csv

class TestCSVJSONConverter(unittest.TestCase):
    def setUp(self):
        # Moderate sample data
        self.rows = [
            {'name': 'Alice', 'age': '30', 'city': 'NY'},
            {'name': 'Bob', 'age': '25', 'city': 'LA'},
            {'name': 'Charlie', 'age': '35', 'city': 'SF'},
            {'name': 'Dana', 'age': '28', 'city': 'CHI'},
            {'name': 'Eve', 'age': '40', 'city': 'SEA'}
        ]
        self.fieldnames = ['name', 'age', 'city']
        # Create temp CSV
        fd, self.csv_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)
        # Create temp JSON
        fd, self.json_path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.rows, f)

    def tearDown(self):
        for p in [self.csv_path, self.json_path,
                  self.csv_path.replace('.csv', '_out.json'),
                  self.json_path.replace('.json', '_out.csv')]:
            try:
                os.remove(p)
            except FileNotFoundError:
                pass

    def test_csv_to_json(self):
        out_json = self.csv_path.replace('.csv', '_out.json')
        csv_to_json(self.csv_path, out_json)
        self.assertTrue(Path(out_json).exists())
        with open(out_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data, self.rows)

    def test_json_to_csv(self):
        out_csv = self.json_path.replace('.json', '_out.csv')
        json_to_csv(self.json_path, out_csv)
        self.assertTrue(Path(out_csv).exists())
        with open(out_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows2 = list(reader)
        self.assertEqual(rows2, self.rows)

    def test_empty_json_to_csv(self):
        fd, empty_json = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        with open(empty_json, 'w', encoding='utf-8') as f:
            json.dump([], f)
        out_csv = empty_json.replace('.json', '_out.csv')
        json_to_csv(empty_json, out_csv)
        self.assertFalse(Path(out_csv).exists())
        os.remove(empty_json)

    def test_missing_csv_file(self):
        out_json = 'should_not_create.json'
        csv_to_json('nonexistent.csv', out_json)
        self.assertFalse(Path(out_json).exists())

    def test_missing_json_file(self):
        out_csv = 'should_not_create.csv'
        json_to_csv('nonexistent.json', out_csv)
        self.assertFalse(Path(out_csv).exists())

if __name__ == '__main__':
    unittest.main()
