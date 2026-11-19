import json
import tempfile
import pytest

from pathlib import Path

from personal_finance.storage import Storage


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
                "date": "2026-09-23",
            }
        ]

        storage.save(data)

        assert storage.file_path.exists()

        with open(storage.file_path, "r") as file:
            saved_data = json.load(file)

        assert saved_data == data


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
                "date": "2026-09-23",
            }
        ]

        storage.save(data)

        loaded_data = storage.load()

        assert loaded_data == data


def test_load_missing_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)

        assert storage.load() == []


def test_save_creates_missing_directories():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "nested" / "data" / "transactions.json"
        storage = Storage(file_path)

        storage.save([])

        assert file_path.exists()
        assert storage.load() == []


def test_save_and_load_unicode():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)

        data = [{"description": "Groceries – കേരളം"}]

        storage.save(data)

        assert storage.load() == data


def test_load_corrupted_json():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        file_path.write_text("{invalid json", encoding="utf-8")

        storage = Storage(file_path)

        with pytest.raises(ValueError, match="Invalid JSON data"):
            storage.load()