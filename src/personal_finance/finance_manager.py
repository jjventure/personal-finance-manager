from .transaction import Transaction


class FinanceManager:
    """Manages transactions and provides finance-related operations."""

    def __init__(self):
        self.transactions = {}
        self.next_transaction_id = 1

    # --------------------
    # CRUD
    # --------------------

    def add_transaction(
        self,
        amount,
        transaction_type,
        category,
        description,
        date,
    ):
        """Create and store a new transaction."""

        transaction_id = self.next_transaction_id

        transaction = Transaction(
            transaction_id,
            amount,
            transaction_type,
            category,
            description,
            date,
        )

        self.transactions[transaction_id] = transaction
        self.next_transaction_id += 1

        return transaction

    def get_transaction(self, transaction_id):
        """Return a transaction by ID, or None if it does not exist."""

        return self.transactions.get(transaction_id)

    def get_all_transactions(self):
        """Return all transactions as a list."""

        return list(self.transactions.values())

    def update_transaction(
        self,
        transaction_id,
        amount=None,
        transaction_type=None,
        category=None,
        description=None,
        date=None,
    ):
        """Update an existing transaction."""

        transaction = self.transactions.get(transaction_id)

        if transaction is None:
            return None

        new_amount = amount if amount is not None else transaction.amount
        new_transaction_type = (
            transaction_type
            if transaction_type is not None
            else transaction.transaction_type
        )
        new_category = (
            category
            if category is not None
            else transaction.category
        )
        new_description = (
            description
            if description is not None
            else transaction.description
        )
        new_date = date if date is not None else transaction.date

        updated_transaction = Transaction(
            transaction.transaction_id,
            new_amount,
            new_transaction_type,
            new_category,
            new_description,
            new_date,
        )

        self.transactions[transaction_id] = updated_transaction

        return updated_transaction

    def delete_transaction(self, transaction_id):
        """Delete and return a transaction, or return None if not found."""

        transaction = self.transactions.get(transaction_id)

        if transaction is None:
            return None

        del self.transactions[transaction_id]

        return transaction

    # --------------------
    # Analytics
    # --------------------

    def calculate_income(self):
        """Return total income."""

        total = 0

        for transaction in self.transactions.values():
            if transaction.transaction_type == "income":
                total += transaction.amount

        return total

    def calculate_expenses(self):
        """Return total expenses."""

        total = 0

        for transaction in self.transactions.values():
            if transaction.transaction_type == "expense":
                total += transaction.amount

        return total

    def calculate_balance(self):
        """Return income minus expenses."""

        return self.calculate_income() - self.calculate_expenses()

    def spending_by_category(self):
        """Return total expenses grouped by category."""

        expenses_by_category = {}

        for transaction in self.transactions.values():
            if transaction.transaction_type != "expense":
                continue

            category = transaction.category

            if category in expenses_by_category:
                expenses_by_category[category] += transaction.amount
            else:
                expenses_by_category[category] = transaction.amount

        return expenses_by_category

    # --------------------
    # Persistence
    # --------------------

    def to_dict_list(self):
        """Convert all transactions into JSON-friendly dictionaries."""

        return [
            transaction.to_dict()
            for transaction in self.transactions.values()
        ]

    def save_to_storage(self, storage):
        """Save all transactions using the provided storage."""

        storage.save(self.to_dict_list())

    def load_from_storage(self, storage):
        """Load transactions from storage."""

        data = storage.load()

        self.transactions = {}

        for transaction_data in data:
            transaction = Transaction.from_dict(transaction_data)
            self.transactions[transaction.transaction_id] = transaction

        if not self.transactions:
            self.next_transaction_id = 1
        else:
            self.next_transaction_id = max(self.transactions) + 1

    # --------------------
    # Search and filtering
    # --------------------

    def search_transactions(self, keyword):
        """Search transactions by category or description."""

        keyword = keyword.lower()
        result = []

        for transaction in self.transactions.values():
            description = transaction.description or ""

            if (
                keyword in transaction.category.lower()
                or keyword in description.lower()
            ):
                result.append(transaction)

        return result

    def filter_by_category(self, category):
        """Return transactions matching a category."""

        category = category.lower()

        return [
            transaction
            for transaction in self.transactions.values()
            if category == transaction.category.lower()
        ]

    def filter_by_type(self, transaction_type):
        """Return transactions matching a transaction type."""

        transaction_type = transaction_type.lower()

        return [
            transaction
            for transaction in self.transactions.values()
            if transaction_type == transaction.transaction_type.lower()
        ]