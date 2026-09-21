''' 

FinanceManager will generate the ID and pass it to Transaction.

Transaction
│
├── transaction_id
│   └── positive integer, unique
│
├── amount
│   └── number > 0
│
├── transaction_type
│   └── "income" or "expense"
│
├── category
│   └── predefined category:
            Food
            Transport
            Entertainment
            Shopping
            Bills
            Health
            Education
            Gym
            Other
│
├── description
│   └── optional string
│
└── date
    └── valid Python date object

'''

from datetime import date 

class Transaction:

    # allowed transaction_types
    ALLOWED_TYPES = ("income", "expense")

    # predefined categories
    CATEGORIES = [
        "Food",
        "Transport",
        "Entertainment",
        "Shopping",
        "Bills",
        "Health",
        "Education",
        "Gym",
        "Other"
    ]

    ### constructor 
    def __init__(self, transaction_id, amount, transaction_type, category, description, date):
        self.transaction_id = transaction_id    # FinanceManager will handle generating the ID later 
        self.amount = amount 
        self.transaction_type = transaction_type 
        self.category = category 
        self.description = description 
        self.date = date 
        self.validate()

    ### validate method 
    def validate(self):

        ## Transaction ID must be a positive integer
        if not isinstance(self.transaction_id, int) or self.transaction_id <= 0:
            raise ValueError("Transaction ID should be a positive integer.")


        ## amount must be greater than 0.
        if not isinstance(self.amount, (int, float)) or self.amount <= 0:
            raise ValueError("Amount should be a positive number.")


        ## transaction_type must be either income or expense 
        if not isinstance(self.transaction_type, str):
            raise TypeError("Transaction type must be in string format.")
    
        self.transaction_type = self.transaction_type.lower()

        if self.transaction_type not in self.ALLOWED_TYPES:
            raise ValueError("Transaction type must be either 'income' or 'expense'.")


        ## handle case-insensitive category input.
        if not isinstance(self.category, str):
            raise TypeError("Category must be in string format.")

        for each_category in self.CATEGORIES:
            if self.category.lower() == each_category.lower():
                self.category = each_category 
                break 
        # The else executes only if the loop finishes without hitting break.
        else:
            raise ValueError("This category doesn't exist.")    


        ## description is optional, but if provided, it should be a string of reasonable length.
        # No description --> accept ✅
        if self.description is not None:

            # Must be a string
            if not isinstance(self.description, str):
                raise TypeError("Description only allows text.")
            
            # Empty string is allowed
            if self.description != "":
                self.description = self.description.strip()

                # Whitespace-only is not allowed
                if self.description == "":
                    raise ValueError("Description cannot contain only whitespace.")

        ## Date validation 
        if not isinstance(self.date, date):
            raise TypeError("Date must be a valid Python date object.")

