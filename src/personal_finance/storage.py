from pathlib import Path
import json
import os
import tempfile


class Storage:
    """Handles JSON-based persistence."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def save(self, data):
        """Save Python data as JSON using an atomic file replacement."""

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.file_path.parent,
                prefix=f".{self.file_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temp_file:

                temp_path = Path(temp_file.name)

                json.dump(
                    data,
                    temp_file,
                    indent=4,
                    ensure_ascii=False,
                )

                temp_file.write("\n")

            os.replace(temp_path, self.file_path)

        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def load(self):
        """Load JSON data from the file.

        Returns an empty list if the file does not exist.
        Raises ValueError if the JSON file is corrupted.
        """

        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON data in {self.file_path}."
            ) from error