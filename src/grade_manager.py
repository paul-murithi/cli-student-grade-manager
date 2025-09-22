import json
from pathlib import Path

current_path = Path(__file__).resolve().parent
project_root = current_path.parent
data_file = project_root/"data"/"students.json"

with open(data_file, "r") as file:
    data = json.load(file)

print(data)