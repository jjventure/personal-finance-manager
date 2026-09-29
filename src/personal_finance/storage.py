from pathlib import Path
import json


class Storage:
    """Handles JSON-based persistence."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def save(self, data):
        """Save Python data as JSON."""

        # if: data/ doesn't exist yet, Python creates it automatically. So your first-ever save works
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        """Load JSON data from the file.

        Returns an empty list if the file does not exist.
        """

        if not self.file_path.exists():
            return []

        with open(self.file_path, "r") as file:
            return json.load(file)