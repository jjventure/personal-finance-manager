from unittest.mock import patch

from personal_finance.main import main 

def test_main():
    """Test the whole application workflow."""

    with patch("personal_finance.main.CLI") as mock_cli:
        main()
        mock_cli.return_value.run.assert_called_once_with()