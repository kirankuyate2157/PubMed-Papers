import pytest
import csv
import os
from pubmed_fetcher.utils import save_to_csv

def test_save_to_csv():
    """Test saving data to CSV."""
    data = [{"id": "12345", "title": "Test Article"}]
    file_path = "test_output.csv"
    
    save_to_csv(data, file_path)

    with open(file_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 1
    assert rows[0]["id"] == "12345"
    assert rows[0]["title"] == "Test Article"

    os.remove(file_path)
