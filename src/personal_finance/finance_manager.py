''' 

FinanceManager
│
├── State
│   ├── transactions = {}
│   └── next_transaction_id = 1
│
├── CREATE
│   └── add_transaction()
│
├── READ
│   ├── get_transaction()
│   └── get_all_transactions()
│
├── UPDATE
│   └── update_transaction()
│
├── DELETE
│   └── delete_transaction()
│
├── ANALYTICS
│   ├── calculate_balance()
│   ├── calculate_income()
│   ├── calculate_expenses()
│   └── spending_by_category()
│
└── ID MANAGEMENT
    └── Generate unique, non-reusable IDs    

'''

from .transaction import Transaction

class FinanceManager:

    ### Initializes FinanceManager
    def __init__(self):

        self.transactions = {} 
        self.next_transaction_id = 1



    ### Add transactions | Create 
    def add_transaction(self, amount, transaction_type, category, description, date):

        transaction_id = self.next_transaction_id
        transaction = Transaction(
            transaction_id,
            amount,
            transaction_type,
            category,
            description,
            date
        )
        self.transactions[transaction_id] = transaction
        self.next_transaction_id += 1 
        return transaction 



    ### Get a single transaction | Read
    def get_transaction(self, transaction_id):
        return self.transactions.get(transaction_id)   # .get() --> Give me this key if it exists; otherwise return None.



    ### Get all transactions | all | Read 
    def get_all_transactions(self):

        result = []

        for transaction in self.transactions.values():
            result.append(transaction)

        return result 



    ### Update transaction | Update 
    def update_transaction(self, transaction_id, amount=None, transaction_type=None, category=None, description=None, date=None):
        transaction = self.transactions.get(transaction_id) 

        if transaction is None:
            return None 

        new_amount = amount if amount is not None else transaction.amount
        new_transaction_type = transaction_type if transaction_type is not None else transaction.transaction_type
        new_category = category if category is not None else transaction.category
        new_description = description if description is not None else transaction.description
        new_date = date if date is not None else transaction.date

        updated_transaction = Transaction(
            transaction.transaction_id,
            new_amount,
            new_transaction_type,
            new_category,
            new_description,
            new_date
        )

        self.transactions[transaction_id] = updated_transaction
        return updated_transaction 

    

    ### Delete transaction | Delete 
    def delete_transaction(self, transaction_id):

        if transaction_id in self.transactions:
            transaction = self.get_transaction(transaction_id)
            del self.transactions[transaction_id] 
            return transaction
        
        else:
            return None   