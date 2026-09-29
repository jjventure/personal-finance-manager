from pathlib import Path 

from personal_finance.storage import Storage
from personal_finance.finance_manager import FinanceManager
from personal_finance.cli import CLI


def main():
    """Set up the application's components and start the Personal Finance Manager."""

    storage_path = Path("data") / "transactions.json"
    storage = Storage(storage_path)
    manager = FinanceManager()

    manager.load_from_storage(storage)

    cli = CLI(manager, storage)
    cli.run()


if __name__ == "__main__":
    main()