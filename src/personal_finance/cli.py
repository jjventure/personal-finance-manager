from datetime import datetime


class CLI:
    """Command-line interface for the Personal Finance Manager."""

    def __init__(self, manager, storage):
        self.manager = manager
        self.storage = storage

    def run(self):
        """Run the main CLI loop."""

        while True:
            self.show_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.search_filter_menu()
            elif choice == "4":
                self.view_balance()
            elif choice == "5":
                self.spending_summary()
            elif choice == "6":
                self.save()
            elif choice == "7":
                self.save()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number from 1 to 7.")

    def show_menu(self):
        """Display the main menu."""

        print(
            "\n===== Personal Finance Manager =====\n"
            "1. Add transaction\n"
            "2. View transactions\n"
            "3. Search/filter transactions\n"
            "4. View balance\n"
            "5. Spending summary\n"
            "6. Save\n"
            "7. Exit\n"
        )

    def add_transaction(self):
        """Collect input and add a transaction."""

        while True:
            try:
                amount = float(input("Enter amount: "))
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

        transaction_type = input(
            "Enter transaction type (income/expense): "
        )
        category = input("Enter category: ")
        description = input("Enter description (optional): ")

        while True:
            try:
                date_input = input("Enter date (YYYY-MM-DD): ")
                transaction_date = datetime.strptime(
                    date_input,
                    "%Y-%m-%d",
                ).date()
                break
            except ValueError:
                print("Invalid date. Please use YYYY-MM-DD.")

        try:
            self.manager.add_transaction(
                amount,
                transaction_type,
                category,
                description,
                transaction_date,
            )
        except (ValueError, TypeError) as error:
            print(f"Could not add transaction: {error}")
            return

        print("Transaction added successfully!")

    def view_transactions(self):
        """Display all transactions."""

        transactions = self.manager.get_all_transactions()

        if not transactions:
            print("No transactions found.")
            return

        self.display_transactions(transactions)

    def search_filter_menu(self):
        """Display the search and filter submenu."""

        while True:
            print(
                "\n===== Search / Filter =====\n"
                "1. Search\n"
                "2. Filter by category\n"
                "3. Filter by type\n"
                "4. Back\n"
            )

            choice = input("Enter your choice: ")

            if choice == "1":
                self.search_transactions()
            elif choice == "2":
                self.filter_by_category()
            elif choice == "3":
                self.filter_by_type()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please select a number from 1 to 4.")

    def search_transactions(self):
        """Search transactions by category or description."""

        keyword = input("Enter search keyword: ")

        results = self.manager.search_transactions(keyword)

        if not results:
            print("No matching transactions found.")
            return

        self.display_transactions(results)

    def display_transactions(self, transactions):
        """Display a collection of transactions."""

        for transaction in transactions:
            print(f"ID: {transaction.transaction_id}")
            print(f"Amount: ₹{transaction.amount:.2f}")
            print(f"Type: {transaction.transaction_type}")
            print(f"Category: {transaction.category}")
            print(f"Description: {transaction.description}")
            print(f"Date: {transaction.date}")
            print("-------------------------")

    def filter_by_category(self):
        """Filter transactions by category."""

        category = input("Enter category: ")

        results = self.manager.filter_by_category(category)

        if not results:
            print("No matching transactions found.")
            return

        self.display_transactions(results)

    def filter_by_type(self):
        """Filter transactions by transaction type."""

        transaction_type = input(
            "Enter transaction type (income/expense): "
        )

        results = self.manager.filter_by_type(transaction_type)

        if not results:
            print("No matching transactions found.")
            return

        self.display_transactions(results)

    def view_balance(self):
        """Display income, expenses, and current balance."""

        income = self.manager.calculate_income()
        expenses = self.manager.calculate_expenses()
        balance = self.manager.calculate_balance()

        print("===== Balance =====")
        print(f"Total Income: ₹{income:.2f}")
        print(f"Total Expenses: ₹{expenses:.2f}")
        print(f"Balance: ₹{balance:.2f}")

    def spending_summary(self):
        """Display spending grouped by category."""

        summary = self.manager.spending_by_category()

        if not summary:
            print("No expenses found.")
            return

        print("===== Spending Summary =====")

        for category, amount in summary.items():
            print(f"{category}: ₹{amount:.2f}")

    def save(self):
        """Save transactions to storage."""

        self.manager.save_to_storage(self.storage)
        print("Transactions saved successfully!")