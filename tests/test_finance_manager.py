from datetime import date
from pathlib import Path
import tempfile

import pytest

from personal_finance.finance_manager import FinanceManager
from personal_finance.storage import Storage
from personal_finance.transaction import Transaction


def test_empty_finance_manager():
    manager = FinanceManager()

    assert manager.transactions == {}
    assert manager.next_transaction_id == 1


def test_add_transaction():
    manager = FinanceManager()

    transaction = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21),
    )

    assert transaction is manager.transactions[1]
    assert transaction.transaction_id == 1
    assert transaction.amount == 500
    assert transaction.transaction_type == "expense"
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 21)
    assert manager.next_transaction_id == 2


def test_add_invalid_transaction():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.add_transaction(
            -500,
            "expense",
            "Food",
            "Dinner",
            date(2026, 9, 21),
        )

    assert manager.transactions == {}
    assert manager.next_transaction_id == 1


def test_get_transaction():
    manager = FinanceManager()

    transaction = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21),
    )

    result = manager.get_transaction(1)

    assert transaction is result


def test_get_non_existent_transaction():
    manager = FinanceManager()

    result = manager.get_transaction(999)

    assert result is None


def test_get_all_transactions_empty():
    manager = FinanceManager()

    result = manager.get_all_transactions()

    assert result == []


def test_get_all_transactions():
    manager = FinanceManager()

    transaction1 = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21),
    )

    transaction2 = manager.add_transaction(
        100000,
        "income",
        "Other",
        "Salary credited",
        date(2026, 9, 21),
    )

    result = manager.get_all_transactions()

    assert len(result) == 2
    assert result[0] is transaction1
    assert result[1] is transaction2


def test_update_transaction():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21),
    )

    updated_transaction = manager.update_transaction(
        1,
        amount=750,
    )

    assert updated_transaction.transaction_id == 1
    assert updated_transaction.amount == 750
    assert updated_transaction.transaction_type == "expense"
    assert updated_transaction.category == "Food"
    assert updated_transaction.description == "Dinner"
    assert updated_transaction.date == date(2026, 9, 21)


def test_update_multiple_fields():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21),
    )

    updated_transaction = manager.update_transaction(
        1,
        amount=750,
        category="Shopping",
        description="New Shoes",
    )

    assert updated_transaction.amount == 750
    assert updated_transaction.category == "Shopping"
    assert updated_transaction.description == "New Shoes"
    assert updated_transaction.transaction_type == "expense"
    assert updated_transaction.date == date(2026, 9, 21)
    assert updated_transaction.transaction_id == 1


def test_update_invalid_transaction():
    manager = FinanceManager()

    transaction = manager.add_transaction(
        amount=500,
        transaction_type="expense",
        category="Food",
        description="Dinner",
        date=date(2026, 9, 21),
    )

    with pytest.raises(ValueError):
        manager.update_transaction(
            transaction_id=1,
            amount=-100,
        )

    assert transaction.amount == 500
    assert manager.transactions[1] is transaction


def test_delete_existing_transaction():
    manager = FinanceManager()

    transaction = manager.add_transaction(
        750,
        "expense",
        "Entertainment",
        "Evening Movie",
        date(2026, 9, 22),
    )

    deleted_transaction = manager.delete_transaction(1)

    assert transaction is deleted_transaction
    assert manager.get_transaction(1) is None


def test_delete_nonexistent_transaction():
    manager = FinanceManager()

    result = manager.delete_transaction(999)

    assert result is None
    assert manager.transactions == {}


def test_delete_does_not_reuse_transaction_id():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22),
    )

    manager.delete_transaction(1)

    transaction2 = manager.add_transaction(
        2000,
        "expense",
        "Gym",
        "Workout",
        date(2026, 9, 22),
    )

    assert transaction2.transaction_id == 2
    assert manager.next_transaction_id == 3


def test_calculate_income_empty_manager():
    manager = FinanceManager()

    assert manager.calculate_income() == 0


def test_calculate_income():
    manager = FinanceManager()

    manager.add_transaction(
        1000,
        "income",
        "Other",
        "1 hour income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        300,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        500,
        "income",
        "Other",
        "0.5 hr income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        200,
        "expense",
        "Transport",
        "Cab charge",
        date(2026, 9, 22),
    )

    assert manager.calculate_income() == 1500


def test_calculate_expenses_empty_manager():
    manager = FinanceManager()

    assert manager.calculate_expenses() == 0


def test_calculate_expenses():
    manager = FinanceManager()

    manager.add_transaction(
        1000,
        "income",
        "Other",
        "1 hour income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        300,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        500,
        "income",
        "Other",
        "0.5 hr income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        200,
        "expense",
        "Transport",
        "Cab charge",
        date(2026, 9, 22),
    )

    assert manager.calculate_expenses() == 500


def test_calculate_balance_empty_manager():
    manager = FinanceManager()

    assert manager.calculate_balance() == 0


def test_calculate_balance():
    manager = FinanceManager()

    manager.add_transaction(
        1000,
        "income",
        "Other",
        "1 hour income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        300,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        500,
        "income",
        "Other",
        "0.5 hr income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        200,
        "expense",
        "Transport",
        "Cab charge",
        date(2026, 9, 22),
    )

    assert manager.calculate_balance() == 1000


def test_spending_by_category_empty_manager():
    manager = FinanceManager()

    assert manager.spending_by_category() == {}


def test_spending_by_category_mixed_transactions():
    manager = FinanceManager()

    manager.add_transaction(
        300,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        1000,
        "income",
        "Other",
        "1 hour income",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Breakfast",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        500,
        "income",
        "Other",
        "0.5 hour income",
        date(2026, 9, 22),
    )

    assert manager.spending_by_category() == {"Food": 800}


def test_spending_by_category():
    manager = FinanceManager()

    manager.add_transaction(
        300,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Breakfast",
        date(2026, 9, 22),
    )

    manager.add_transaction(
        200,
        "expense",
        "Transport",
        "Taxi Fare",
        date(2026, 9, 22),
    )

    assert manager.spending_by_category() == {
        "Food": 800,
        "Transport": 200,
    }


def test_to_dict_list_empty():
    manager = FinanceManager()

    result = manager.to_dict_list()

    assert result == []


def test_to_dict_list_single_transaction():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 23),
    )

    result = manager.to_dict_list()

    assert result == [
        {
            "transaction_id": 1,
            "amount": 500,
            "transaction_type": "expense",
            "category": "Food",
            "description": "Dinner",
            "date": "2026-09-23",
        }
    ]


def test_to_dict_list_multiple_transactions():
    manager = FinanceManager()

    manager.add_transaction(
        1000,
        "income",
        "Other",
        "per hour income",
        date(2026, 9, 23),
    )

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 23),
    )

    result = manager.to_dict_list()

    assert result == [
        {
            "transaction_id": 1,
            "amount": 1000,
            "transaction_type": "income",
            "category": "Other",
            "description": "per hour income",
            "date": "2026-09-23",
        },
        {
            "transaction_id": 2,
            "amount": 500,
            "transaction_type": "expense",
            "category": "Food",
            "description": "Dinner",
            "date": "2026-09-23",
        },
    ]


def test_save_to_storage():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)
        manager = FinanceManager()

        manager.add_transaction(
            500,
            "expense",
            "Food",
            "Dinner",
            date(2026, 9, 23),
        )

        manager.save_to_storage(storage)

        assert storage.file_path.exists()

        loaded_data = storage.load()

        assert loaded_data == [
            {
                "transaction_id": 1,
                "amount": 500,
                "transaction_type": "expense",
                "category": "Food",
                "description": "Dinner",
                "date": "2026-09-23",
            }
        ]


def test_load_from_storage():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)
        manager = FinanceManager()

        manager.load_from_storage(storage)

        assert manager.transactions == {}
        assert manager.next_transaction_id == 1


def test_load_from_storage_multiple_transactions():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)
        manager = FinanceManager()

        data = [
            {
                "transaction_id": 1,
                "amount": 1000,
                "transaction_type": "income",
                "category": "Other",
                "description": "Salary",
                "date": "2026-09-20",
            },
            {
                "transaction_id": 2,
                "amount": 500,
                "transaction_type": "expense",
                "category": "Food",
                "description": "Dinner",
                "date": "2026-09-21",
            },
            {
                "transaction_id": 5,
                "amount": 300,
                "transaction_type": "expense",
                "category": "Transport",
                "description": "Bus",
                "date": "2026-09-22",
            },
        ]

        storage.save(data)

        manager.load_from_storage(storage)

        assert len(manager.transactions) == 3
        assert list(manager.transactions.keys()) == [1, 2, 5]
        assert manager.next_transaction_id == 6
        assert isinstance(manager.transactions[2], Transaction)


def test_save_load_and_continue():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "transactions.json"
        storage = Storage(file_path)

        manager = FinanceManager()

        manager.add_transaction(
            500,
            "expense",
            "Food",
            "Dinner",
            date(2026, 9, 23),
        )

        manager.save_to_storage(storage)

        new_manager = FinanceManager()

        new_manager.load_from_storage(storage)

        new_transaction = new_manager.add_transaction(
            1000,
            "income",
            "Other",
            "Salary",
            date(2026, 9, 23),
        )

        assert new_transaction.transaction_id == 2
        assert len(new_manager.transactions) == 2


def test_search_transactions_by_category():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        800,
        "expense",
        "Transport",
        "Uber",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        2000,
        "expense",
        "Food",
        "Bought some Groceries",
        date(2026, 9, 25),
    )

    results = manager.search_transactions("food")

    assert len(results) == 2
    assert results[0].transaction_id == 1
    assert results[1].transaction_id == 3


def test_search_transactions_by_description():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner at restaurant",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        800,
        "expense",
        "Transport",
        "Uber to college",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        2000,
        "expense",
        "Shopping",
        "Bought new shoes",
        date(2026, 9, 25),
    )

    results = manager.search_transactions("dinner")

    assert len(results) == 1
    assert results[0].transaction_id == 1


def test_search_transactions_case_insensitive():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    results = manager.search_transactions("FOOD")

    assert len(results) == 1
    assert results[0].transaction_id == 1


def test_search_transactions_with_none_description():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        None,
        date(2026, 9, 25),
    )

    results = manager.search_transactions("dinner")

    assert len(results) == 0


def test_search_transactions_no_match():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    results = manager.search_transactions("laptop")

    assert results == []


def test_filter_by_category():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        800,
        "expense",
        "Transport",
        "Uber",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        2000,
        "expense",
        "Food",
        "Groceries",
        date(2026, 9, 25),
    )

    results = manager.filter_by_category("food")

    assert len(results) == 2
    assert results[0].transaction_id == 1
    assert results[1].transaction_id == 3


def test_filter_by_type():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        2000,
        "income",
        "Education",
        "Freelance work",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        800,
        "expense",
        "Transport",
        "Uber",
        date(2026, 9, 25),
    )

    results = manager.filter_by_type("EXPENSE")

    assert len(results) == 2
    assert results[0].transaction_id == 1
    assert results[1].transaction_id == 3


def test_filter_by_category_no_match():
    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    results = manager.filter_by_category("Shopping")

    assert results == []