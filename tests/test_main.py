from unittest.mock import patch

from personal_finance.main import main


def test_main():
    """Test the whole application workflow."""

    with patch("personal_finance.main.CLI") as mock_cli:
        main()

        mock_cli.return_value.run.assert_called_once_with()


def test_main_handles_loading_error():
    """Test that the application handles loading errors."""

    with patch(
        "personal_finance.main.FinanceManager.load_from_storage",
        side_effect=ValueError("Invalid JSON data"),
    ):
        with patch("personal_finance.main.CLI") as mock_cli:
            with patch("builtins.print") as mock_print:
                main()

    mock_cli.assert_not_called()

    mock_print.assert_called_once_with(
        "Could not load saved transactions: Invalid JSON data"
    )


def test_main_handles_storage_error():
    """Test that the application handles storage errors during startup."""

    with patch(
        "personal_finance.main.FinanceManager.load_from_storage",
        side_effect=OSError("Permission denied"),
    ):
        with patch("personal_finance.main.CLI") as mock_cli:
            with patch("builtins.print") as mock_print:
                main()

    mock_cli.assert_not_called()

    mock_print.assert_called_once_with(
        "Could not load saved transactions: Permission denied"
    )