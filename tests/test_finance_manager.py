from personal_finance.finance_manager import FinanceManager
from datetime import date



### Test: empty finance manager
def test_empty_finance_manager():

    manager = FinanceManager()

    assert manager.transactions == {}
    assert manager.next_transaction_id == 1 


test_empty_finance_manager()



### Test method: add transaction
def test_add_transaction():

    manager = FinanceManager()

    transaction = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21)
    )

    assert transaction is manager.transactions[1]
    assert transaction.transaction_id == 1 
    assert transaction.amount == 500 
    assert transaction.transaction_type == "expense"  
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 21)
    assert manager.next_transaction_id == 2 

test_add_transaction()



### Test: if invalid transaction is added 
def test_add_invalid_transaction():

    manager = FinanceManager()

    error_occurred = False 

    try:
        manager.add_transaction(
            -500,
            "expense",
            "Food",
            "Dinner",
            date(2026, 9, 21)
        ) 
    except ValueError:
        error_occurred = True 

    assert error_occurred
    assert manager.transactions == {}
    assert manager.next_transaction_id == 1 

test_add_invalid_transaction()



### Test: get_transaction | single transaction | Read 
def test_get_transaction():

    manager = FinanceManager()

    transaction = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21)
    )

    result = manager.get_transaction(1)

    assert transaction is result 

test_get_transaction()



### Test: Get non-existent transaction | single transaction | Read
def test_get_non_existent_transaction():

    manager = FinanceManager()

    result = manager.get_transaction(999)

    assert result is None 

test_get_non_existent_transaction()



### Test: Get all transactions if empty | all | Read 
def test_get_all_transactions_empty():

    manager = FinanceManager()

    result = manager.get_all_transactions()

    assert result == []    

test_get_all_transactions_empty()



### Test: Get all transactions | all | Read 
def test_get_all_transactions():

    manager = FinanceManager()

    transaction1 = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21)
    )

    transaction2 = manager.add_transaction(
        100000,
        "income",
        "Other",
        "Salary credited",
        date(2026, 9, 21)
    )

    result = manager.get_all_transactions()

    assert len(result) == 2 
    assert result[0] is transaction1 
    assert result[1] is transaction2

test_get_all_transactions()



### Test: Update transaction | Update 
def test_update_transaction():

    manager = FinanceManager()

    transaction = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21)
    )

    updated_transaction = manager.update_transaction(
        1,
        amount = 750
    )

    assert updated_transaction.transaction_id == 1 
    assert updated_transaction.amount == 750 
    assert updated_transaction.transaction_type == "expense"
    assert updated_transaction.category == "Food"
    assert updated_transaction.description == "Dinner"
    assert updated_transaction.date == date(2026, 9, 21)

test_update_transaction()



### Test: Update multiple fields | Update
def test_update_multiple_fields():

    manager = FinanceManager()

    transaction = manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 21)
    )

    updated_transaction = manager.update_transaction(
        1,
        amount = 750,
        category = "Shopping",
        description = "New Shoes"
    ) 

    assert updated_transaction.amount == 750
    assert updated_transaction.category == "Shopping"
    assert updated_transaction.description == "New Shoes"

    assert updated_transaction.transaction_type == "expense"
    assert updated_transaction.date == date(2026, 9, 21)
    assert updated_transaction.transaction_id == 1 

test_update_multiple_fields()



### Test: Update invalid transaction | Update 
def test_update_invalid_transaction():

    manager = FinanceManager()

    error_occurred = False

    transaction = manager.add_transaction(
        amount = 500,
        transaction_type = "expense",
        category = "Food",
        description = "Dinner",
        date = date(2026, 9, 21)
    )

    try:
        updated_transaction = manager.update_transaction(
            transaction_id = 1,
            amount = -100
        )
    except ValueError:
        error_occurred = True 

    assert error_occurred
    assert transaction.amount == 500 
    assert manager.transactions[1] is transaction 

test_update_invalid_transaction()



### Test: Delete existing transaction | Delete 
def test_delete_existing_transaction():

    manager = FinanceManager()

    transaction = manager.add_transaction(
        750,
        "expense",
        "Entertainment",
        "Evening Movie",
        date(2026, 9, 22)
    )

    deleted_transaction = manager.delete_transaction(1)
    
    assert transaction is deleted_transaction 
    assert manager.get_transaction(1) is None 

test_delete_existing_transaction()



### Test: Delete nonexistent transaction | Delete
def test_delete_nonexistent_transaction():

    manager = FinanceManager()

    result = manager.delete_transaction(999)

    assert result is None 
    assert manager.transactions == {}

test_delete_nonexistent_transaction()



### Test: Delete doesn't reuse transaction_id | Delete 
def test_delete_does_not_reuse_transaction_id():

    manager = FinanceManager()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 22)
    )

    manager.delete_transaction(1)

    transaction2 = manager.add_transaction(
        2000,
        "expense",
        "Gym",
        "Workout",
        date(2026, 9, 22)
    )

    assert transaction2.transaction_id == 2 
    assert manager.next_transaction_id == 3 

test_delete_does_not_reuse_transaction_id()