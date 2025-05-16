import json
from notebook_generator import NotebookGenerator

BASE_IMAGE = 'synthguard/synthguard:latest' # Example image, replace with your own

with open('synthguard-framework/automation/configs/police_call_pipeline_pipeline.json', 'r') as f:
    pipeline_dict = json.load(f)

print(pipeline_dict)

# Define the path for output notebook
notebook_path = 'synthguard-framework/automation/generated_content/pipeline_notebook.ipynb'

# Initialize the NotebookGenerator
generator = NotebookGenerator(pipeline_dict, notebook_path, BASE_IMAGE)

# Generate the notebook
generator.generate_notebook()