from pathlib import Path

from personal_finance.storage import Storage
from personal_finance.finance_manager import FinanceManager
from personal_finance.cli import CLI


def main():
    """Set up the application's components and start the Personal Finance Manager."""

    storage_path = Path("data") / "transactions.json"
    storage = Storage(storage_path)
    manager = FinanceManager()

    try:
        manager.load_from_storage(storage)

    except (OSError, ValueError, TypeError) as error:
        print(f"Could not load saved transactions: {error}")
        return

    cli = CLI(manager, storage)
    cli.run()


if __name__ == "__main__":
    main()