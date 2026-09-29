# Personal Finance Manager

## Overview

The Personal Finance Manager is a Python-based application for tracking personal finances by recording income and expenses, while providing summaries and insights into spending and overall balance.

## Features

* Add income and expense transactions
* View all transactions
* Search transactions by category or description
* Filter transactions by category or type
* Calculate total income, expenses, and current balance
* View spending summaries by category
* Save and load transactions using JSON
* Automatically save transactions when exiting
* Command-line interface (CLI)

## Tech Stack

* Python 3.12.1
* pytest
* JSON
* Git & GitHub

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
├── data/
├── .gitignore
├── pyproject.toml
└── README.md
```

* `src/personal_finance/` — application source code
* `tests/` — automated tests for the application
* `data/` — local storage for transaction data
* `pyproject.toml` — project and package configuration
* `.gitignore` — files and directories excluded from Git

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

### 4. Install the project

```bash
pip install -e .
```

## Usage

Run the application with:

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

Transactions are stored locally as JSON data in:

```text
data/transactions.json
```

The `data/` directory is excluded from Git so personal financial data is not committed to the repository.

## Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```bash
python -m pytest
```

The v1.0.0 test suite contains **73 tests**, covering transactions, finance management, storage, CLI functionality, and application startup.

## Future Roadmap

Potential future versions may expand the project with:

* Pandas-based financial analysis
* Matplotlib-based visualizations
* SQL database storage
* Machine learning features
* FastAPI backend
* Docker containerization
* Cloud deployment
* Web-based financial dashboard

## Version

**v1.0.0**

The v1.0.0 release provides a functional command-line personal finance manager with transaction management, financial analytics, JSON persistence, and automated testing.
