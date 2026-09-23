from pathlib import Path  # useful tool for filesystem paths
import json 

class Storage:

    # Constructor 
    def __init__(self, file_path):
        self.file_path = Path(file_path) 

    # save method | Converts: Python data --> json 
    def save(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    # load method | Converts: json --> python data
    def load(self):
        if self.file_path.exists():
            with open (self.file_path, 'r') as file:
                data = json.load(file)
                return data 
        else:
            return []