from datetime import date, datetime
import math


class Transaction:
    """Represents a single financial transaction."""

    ALLOWED_TYPES = ("income", "expense")

    CATEGORIES = [
        "Food",
        "Transport",
        "Entertainment",
        "Shopping",
        "Bills",
        "Health",
        "Education",
        "Gym",
        "Other",
    ]

    def __init__(
        self,
        transaction_id,
        amount,
        transaction_type,
        category,
        description,
        date,
    ):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.description = description
        self.date = date

        self.validate()

    def validate(self):
        """Validate and normalize transaction data."""

        # Transaction ID must be a positive integer.
        if (
            isinstance(self.transaction_id, bool)
            or not isinstance(self.transaction_id, int)
            or self.transaction_id <= 0
        ):
            raise ValueError("Transaction ID should be a positive integer.")

        # Amount must be a finite positive number.
        if (
            isinstance(self.amount, bool)
            or not isinstance(self.amount, (int, float))
            or not math.isfinite(self.amount)
            or self.amount <= 0
        ):
            raise ValueError("Amount should be a finite positive number.")

        # Transaction type must be income or expense.
        if not isinstance(self.transaction_type, str):
            raise TypeError("Transaction type must be in string format.")

        self.transaction_type = self.transaction_type.strip().lower()

        if self.transaction_type not in self.ALLOWED_TYPES:
            raise ValueError(
                "Transaction type must be either 'income' or 'expense'."
            )

        # Category must match one of the predefined categories.
        if not isinstance(self.category, str):
            raise TypeError("Category must be in string format.")

        self.category = self.category.strip()

        for allowed_category in self.CATEGORIES:
            if self.category.lower() == allowed_category.lower():
                self.category = allowed_category
                break
        else:
            raise ValueError("This category doesn't exist.")

        # Description is optional.
        if self.description is not None:
            if not isinstance(self.description, str):
                raise TypeError("Description only allows text.")

            if self.description != "":
                self.description = self.description.strip()

                if self.description == "":
                    raise ValueError(
                        "Description cannot contain only whitespace."
                    )

        # Date must be a date object, not a datetime object.
        if not isinstance(self.date, date) or isinstance(
            self.date, datetime
        ):
            raise TypeError("Date must be a valid Python date object.")

    def to_dict(self):
        """Convert the transaction into a JSON-friendly dictionary."""

        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Transaction from a dictionary."""

        if not isinstance(data, dict):
            raise TypeError("Transaction data must be a dictionary.")

        required_fields = {
            "transaction_id",
            "amount",
            "transaction_type",
            "category",
            "description",
            "date",
        }

        missing_fields = required_fields - data.keys()

        if missing_fields:
            raise ValueError(
                f"Missing transaction fields: {', '.join(sorted(missing_fields))}"
            )

        try:
            transaction_date = date.fromisoformat(data["date"])
        except (TypeError, ValueError) as error:
            raise ValueError("Transaction date must use YYYY-MM-DD format.") from error

        return cls(
            data["transaction_id"],
            data["amount"],
            data["transaction_type"],
            data["category"],
            data["description"],
            transaction_date,
        )