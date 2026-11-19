# Personal Finance Manager

## Overview

Personal Finance Manager is a Python-based command-line application for tracking personal finances. It allows users to record income and expenses, manage transactions, and monitor their overall financial position through balance calculations and spending summaries.

## Features

- Add income and expense transactions
- View all recorded transactions
- Search transactions by category or description
- Filter transactions by category or transaction type
- Calculate total income, expenses, and current balance
- View spending summaries by category
- Save and load transactions using JSON
- Automatically save transactions when exiting
- Command-line interface (CLI)

## Tech Stack

- **Python 3.12+** — Application development
- **pytest** — Automated testing
- **JSON** — Local data storage
- **Git & GitHub** — Version control and project hosting

## Project Structure

```text
personal-finance-manager/
├── src/
│   └── personal_finance/
│       ├── __init__.py
│       ├── transaction.py
│       ├── finance_manager.py
│       ├── storage.py
│       ├── cli.py
│       └── main.py
├── tests/
│   ├── test_transaction.py
│   ├── test_finance_manager.py
│   ├── test_storage.py
│   ├── test_cli.py
│   └── test_main.py
├── docs/
│   └── Design.png
├── .gitignore
├── pyproject.toml
└── README.md
```

- `src/personal_finance/` — Application source code
- `tests/` — Automated tests
- `docs/` — Project documentation and design resources
- `data/` — Local transaction storage (created at runtime and excluded from Git)
- `pyproject.toml` — Project and package configuration
- `.gitignore` — Specifies files and directories excluded from Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jjventure/personal-finance-manager.git
cd personal-finance-manager
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Git Bash:**

```bash
source .venv/Scripts/activate
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate
```

### 4. Install the project and development dependencies

```bash
python -m pip install -e ".[dev]"
```

## Usage

Start the application with:

```bash
python -m personal_finance.main
```

The application provides a command-line menu for managing transactions:

```text
===== Personal Finance Manager =====
1. Add transaction
2. View transactions
3. Search/filter transactions
4. View balance
5. Spending summary
6. Save
7. Exit
```

### Data Storage

Transactions are stored locally in JSON format at:

```text
data/transactions.json
```

The `data/` directory is excluded from Git to prevent personal financial data from being committed to the repository.

## Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```bash
python -m pytest
```

The v1.0.0 test suite contains **97 automated tests**, covering:

- Transaction validation and functionality
- Finance management and calculations
- JSON storage and data handling
- CLI functionality
- Application startup

## Future Roadmap

Potential future improvements include:

- Pandas-based financial analysis
- Matplotlib-based data visualizations
- SQL database integration
- Machine learning features
- FastAPI backend
- Docker containerization
- Cloud deployment
- Web-based financial dashboard

## Version

**v1.0.0**

The v1.0.0 release provides a functional command-line personal finance manager with transaction management, financial calculations, JSON persistence, and automated testing.