from pathlib import Path 
from personal_finance.storage import Storage
import tempfile   # standard library tool for a temporary directory
import json

# Test: save method | save 
def test_save():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)
        data = [
    {
        "transaction_id": 1,
        "amount": 500,
        "transaction_type": "expense",
        "category": "Food",
        "description": "Dinner",
        "date": "2026-09-23"
    }
]

        storage.save(data)

        assert storage.file_path.exists()

        with open(storage.file_path, 'r') as file:
            saved_data = json.load(file)

        assert saved_data == data

test_save()



# Test: load method | load
def test_load():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)
        data = [
            {
                "transaction_id": 1,
                "amount": 500,
                "transaction_type": "expense",
                "category": "Food",
                "description": "Dinner",
                "date": "2026-09-23"
            }
        ]
        storage.save(data)
        loaded_data = storage.load()

        assert loaded_data == data 

test_load()



# Test: load missing file | load
def test_load_missing_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)

        assert storage.load() == []

test_load_missing_file()