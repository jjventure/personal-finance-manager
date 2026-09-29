from datetime import date

import pytest

from personal_finance.transaction import Transaction


def test_valid_transaction():
    transaction = Transaction(
        1,
        500,
        "EXPENSE",
        "fOoD",
        "  Dinner  ",
        date(2026, 9, 19),
    )

    assert transaction.transaction_id == 1
    assert transaction.amount == 500
    assert transaction.transaction_type == "expense"
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 19)


def test_invalid_amount():
    with pytest.raises(ValueError):
        Transaction(
            1,
            -500,
            "EXPENSE",
            "fOoD",
            "  Dinner  ",
            date(2026, 9, 19),
        )


def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        Transaction(
            1,
            500,
            "return",
            "fOoD",
            "  Dinner  ",
            date(2026, 9, 19),
        )


def test_invalid_category():
    with pytest.raises(ValueError):
        Transaction(
            1,
            500,
            "EXPENSE",
            "Travel",
            "  Dinner  ",
            date(2026, 9, 19),
        )


def test_invalid_date():
    with pytest.raises(TypeError):
        Transaction(
            1,
            500,
            "EXPENSE",
            "fOoD",
            "  Dinner  ",
            "19/09/2026",
        )


def test_description_none():
    transaction = Transaction(
        1,
        500,
        "expense",
        "Food",
        None,
        date(2026, 9, 19),
    )

    assert transaction.description is None


def test_description_empty():
    transaction = Transaction(
        1,
        500,
        "expense",
        "Food",
        "",
        date(2026, 9, 19),
    )

    assert transaction.description == ""


def test_description_whitespace_only():
    with pytest.raises(ValueError):
        Transaction(
            1,
            500,
            "expense",
            "Food",
            "   ",
            date(2026, 9, 19),
        )


def test_to_dict():
    transaction = Transaction(
        1,
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 23),
    )

    result = transaction.to_dict()

    assert result == {
        "transaction_id": 1,
        "amount": 500,
        "transaction_type": "expense",
        "category": "Food",
        "description": "Dinner",
        "date": "2026-09-23",
    }


def test_from_dict():
    data = {
        "transaction_id": 1,
        "amount": 500,
        "transaction_type": "expense",
        "category": "Food",
        "description": "Dinner",
        "date": "2026-09-23",
    }

    transaction = Transaction.from_dict(data)

    assert transaction.transaction_id == 1
    assert transaction.amount == 500
    assert transaction.transaction_type == "expense"
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 23)