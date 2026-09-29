from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from personal_finance.cli import CLI
from personal_finance.finance_manager import FinanceManager
from personal_finance.storage import Storage


def create_cli():
    manager = FinanceManager()
    temp_dir = TemporaryDirectory()
    storage = Storage(Path(temp_dir.name) / "transactions.json")
    cli = CLI(manager, storage)

    return manager, cli, temp_dir


def test_save():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    cli.save()

    data = cli.storage.load()

    assert len(data) == 1
    assert data[0]["amount"] == 500
    assert data[0]["transaction_type"] == "expense"
    assert data[0]["category"] == "Food"


def test_add_transaction():
    manager, cli, temp_dir = create_cli()

    with patch(
        "builtins.input",
        side_effect=[
            "500",
            "expense",
            "Food",
            "Dinner",
            "2026-09-25",
        ],
    ):
        cli.add_transaction()

    assert len(manager.transactions) == 1

    transaction = manager.transactions[1]

    assert transaction.amount == 500.0
    assert transaction.transaction_type == "expense"
    assert transaction.category == "Food"
    assert transaction.description == "Dinner"
    assert transaction.date == date(2026, 9, 25)


def test_run_add_transaction():
    manager, cli, temp_dir = create_cli()

    with patch(
        "builtins.input",
        side_effect=[
            "1",
            "500",
            "expense",
            "Food",
            "Dinner",
            "2026-09-25",
            "7",
        ],
    ):
        cli.run()

    assert len(manager.transactions) == 1


def test_view_transactions_empty():
    manager, cli, temp_dir = create_cli()

    with patch("builtins.print") as mock_print:
        cli.view_transactions()

    mock_print.assert_called_once_with("No transactions found.")


def test_view_transactions():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch("builtins.print") as mock_print:
        cli.view_transactions()

    mock_print.assert_any_call("ID: 1")
    mock_print.assert_any_call("Amount: ₹500.00")
    mock_print.assert_any_call("Type: expense")
    mock_print.assert_any_call("Category: Food")
    mock_print.assert_any_call("Description: Dinner")
    mock_print.assert_any_call("Date: 2026-09-25")


def test_view_multiple_transactions():
    manager, cli, temp_dir = create_cli()

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
        date(2026, 9, 24),
    )

    with patch("builtins.print") as mock_print:
        cli.view_transactions()

    mock_print.assert_any_call("ID: 1")
    mock_print.assert_any_call("Amount: ₹500.00")
    mock_print.assert_any_call("ID: 2")
    mock_print.assert_any_call("Amount: ₹2000.00")


def test_run_view_transactions():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch(
        "builtins.input",
        side_effect=["2", "7"],
    ):
        cli.run()

    assert len(manager.transactions) == 1


def test_search_filter_menu_back():
    manager, cli, temp_dir = create_cli()

    with patch("builtins.input", side_effect=["4"]):
        cli.search_filter_menu()


def test_run_search_filter_menu():
    manager, cli, temp_dir = create_cli()

    with patch(
        "builtins.input",
        side_effect=["3", "4", "7"],
    ):
        cli.run()


def test_search_transactions():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch("builtins.input", side_effect=["dinner"]):
        cli.search_transactions()


def test_search_transactions_no_results():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch("builtins.input", side_effect=["laptop"]):
        with patch("builtins.print") as mock_print:
            cli.search_transactions()

    mock_print.assert_called_once_with(
        "No matching transactions found."
    )


def test_filter_by_category():
    manager, cli, temp_dir = create_cli()

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

    with patch("builtins.input", side_effect=["Food"]):
        with patch("builtins.print") as mock_print:
            cli.filter_by_category()

    mock_print.assert_any_call("ID: 1")
    mock_print.assert_any_call("Category: Food")


def test_filter_by_category_no_results():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch("builtins.input", side_effect=["Shopping"]):
        with patch("builtins.print") as mock_print:
            cli.filter_by_category()

    mock_print.assert_called_once_with(
        "No matching transactions found."
    )


def test_filter_by_type():
    manager, cli, temp_dir = create_cli()

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

    with patch("builtins.input", side_effect=["expense"]):
        with patch("builtins.print") as mock_print:
            cli.filter_by_type()

    mock_print.assert_any_call("ID: 1")
    mock_print.assert_any_call("Type: expense")


def test_filter_by_type_no_results():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch("builtins.input", side_effect=["income"]):
        with patch("builtins.print") as mock_print:
            cli.filter_by_type()

    mock_print.assert_called_once_with(
        "No matching transactions found."
    )


def test_view_balance():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        5000,
        "income",
        "Education",
        "Freelance work",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        1500,
        "expense",
        "Food",
        "Groceries",
        date(2026, 9, 25),
    )

    with patch("builtins.print") as mock_print:
        cli.view_balance()

    mock_print.assert_any_call("Total Income: ₹5000.00")
    mock_print.assert_any_call("Total Expenses: ₹1500.00")
    mock_print.assert_any_call("Balance: ₹3500.00")


def test_run_view_balance():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        5000,
        "income",
        "Education",
        "Freelance work",
        date(2026, 9, 25),
    )

    with patch(
        "builtins.input",
        side_effect=["4", "7"],
    ):
        cli.run()


def test_spending_summary():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        1000,
        "expense",
        "Food",
        "Groceries",
        date(2026, 9, 25),
    )

    manager.add_transaction(
        800,
        "expense",
        "Transport",
        "Uber",
        date(2026, 9, 25),
    )

    with patch("builtins.print") as mock_print:
        cli.spending_summary()

    mock_print.assert_any_call("Food: ₹1500.00")
    mock_print.assert_any_call("Transport: ₹800.00")


def test_spending_summary_no_expenses():
    manager, cli, temp_dir = create_cli()

    with patch("builtins.print") as mock_print:
        cli.spending_summary()

    mock_print.assert_called_once_with("No expenses found.")


def test_run_spending_summary():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch(
        "builtins.input",
        side_effect=["5", "7"],
    ):
        cli.run()


def test_run_save():
    manager, cli, temp_dir = create_cli()

    manager.add_transaction(
        500,
        "expense",
        "Food",
        "Dinner",
        date(2026, 9, 25),
    )

    with patch(
        "builtins.input",
        side_effect=["6", "7"],
    ):
        cli.run()

    data = cli.storage.load()

    assert len(data) == 1
    assert data[0]["amount"] == 500


def test_exit_saves_transactions():
    """Test that exiting the CLI saves transactions."""

    manager, cli, temp_dir = create_cli()

    with patch.object(cli, "save") as mock_save:
        with patch("builtins.input", return_value="7"):
            cli.run()

        mock_save.assert_called_once_with()