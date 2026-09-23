from datetime import date
from personal_finance.transaction import Transaction

### Test valid transaction
def test_valid_transaction():
    transaction = Transaction(
        1,
        500,
        "EXPENSE",
        "fOoD",
        "  Dinner  ",
        date(2026, 9, 19)
    )

    assert transaction.transaction_id == 1 
    assert transaction.amount == 500 
    assert transaction.transaction_type == "expense"
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 19)

test_valid_transaction()



### Test invalid amount 
def test_invalid_amount():
    error_occurred = False 

    try:    
        transaction = Transaction(
            1,
            -500,   # <-- invalid amount
            "EXPENSE",
            "fOoD",
            "  Dinner  ",
            date(2026, 9, 19)
        )

    except ValueError:
        error_occurred = True 

    assert error_occurred 

test_invalid_amount()



### Test invalid transaction type
def test_invalid_transaction_type():
    error_occurred = False 

    try:
        transaction = Transaction(
            1, 
            500,
            "return",   # <-- invalid transaction type
            "fOoD",
            "  Dinner  ",
            date(2026, 9, 19)
        )

    except ValueError:
        error_occurred = True 

    assert error_occurred 

test_invalid_transaction_type()



### Test invalid category 
def test_invalid_category():
    error_occurred = False 

    try:
        transaction = Transaction(
            1,
            500,
            "EXPENSE",
            "Travel",   # <-- invalid category  
            "  Dinner  ",
            date(2026, 9, 19)
        )

    except ValueError:
        error_occurred = True 

    assert error_occurred

test_invalid_category()



### Test invalid date 
def test_invalid_date():
    error_occurred = False 

    try:
        transaction = Transaction(
            1,
            500,
            "EXPENSE",
            "fOoD",
            "  Dinner  ",
            "19/09/2026"   # <- invalid date type
        )

    except TypeError:
        error_occurred = True 

    assert error_occurred 

test_invalid_date()



### description cases.

## 1️⃣ None should be accepted
def test_description_none():
    transaction = Transaction(
        1,
        500,
        "expense",
        "Food",
        None,   # <--
        date(2026, 9, 19)
    )

    assert transaction.description is None

test_description_none()


## 2️⃣ Empty string should be accepted
def test_description_empty():
    transaction = Transaction(
        1,
        500,
        "expense",
        "Food",
        "",   # <--
        date(2026, 9, 19)
    )

    assert transaction.description == ""

test_description_empty()


## 3️⃣ Whitespace-only should be rejected
def test_description_whitespace_only():
    error_occurred = False 

    try:
        Transaction(
            1,
            500,
            "expense",
            "Food",
            "   ",
            date(2026, 9, 19)
        )

    except ValueError:
        error_occurred = True 

    assert error_occurred 

test_description_whitespace_only()



### Test: to_dict | Convert transaction to dictionary
def test_to_dict():

    transaction = Transaction(
        1,
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 23)
    )

    result = transaction.to_dict()

    assert result == {
    "transaction_id": 1,
    "amount": 500,
    "transaction_type": "expense",
    "category": "Food",
    "description": "Dinner",
    "date": "2026-09-23"
}

test_to_dict()



### Test: from_dict() | Convert dictionary to transaction
def test_from_dict():

    data = {
    "transaction_id": 1,
    "amount": 500,
    "transaction_type": "expense",
    "category": "Food",
    "description": "Dinner",
    "date": "2026-09-23"
}

    transaction = Transaction.from_dict(data)

    assert transaction.transaction_id == 1 
    assert transaction.amount == 500 
    assert transaction.transaction_type == "expense"
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 23)

test_from_dict()