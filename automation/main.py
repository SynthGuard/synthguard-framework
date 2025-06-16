import json
from notebook_generator import NotebookGenerator

BASE_IMAGE = "kristiantamm/synthguard_public:latest"

with open('automation/configs/gun_ownership.json', 'r') as f:
    pipeline_dict = json.load(f)

print(pipeline_dict)

# Define the path for output notebook
notebook_path = 'automation/generated_content/gun_ownership.ipynb'

# Initialize the NotebookGenerator
generator = NotebookGenerator(pipeline_dict, notebook_path, BASE_IMAGE)

# Generate the notebook
generator.generate_notebook()