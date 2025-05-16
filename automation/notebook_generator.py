#imports
import nbformat as nbf

#section classes
from pipeline_sections.input_section import InputSection
from pipeline_sections.preprocess_section import PreprocessSection
from pipeline_sections.generation_section import GenerationSection
from pipeline_sections.privacy_report_section import PrivacyReportSection
from pipeline_sections.utility_report_section import UtilityReportSection
from pipeline_sections.diagnostic_report_section import DiagnosticReportSection

class NotebookGenerator:
    def __init__(self, pipeline_dict, notebook_path, base_image):
        self.pipeline_dict = pipeline_dict
        self.notebook_path = notebook_path
        self.nb = nbf.v4.new_notebook()
        self.pipeline_name = pipeline_dict['pipeline_name']
        self.pipeline_description = pipeline_dict['pipeline_description']
        self.base_image = base_image

    def add_markdown_cell(self, text):
        self.nb['cells'].append(nbf.v4.new_markdown_cell(text))
    
    def add_code_cell(self, code):
        self.nb['cells'].append(nbf.v4.new_code_cell(code))

    def generate_notebook(self):
        """Generates a Jupyter Notebook based on the pipeline dictionary."""
        
        nb = nbf.v4.new_notebook()
        
        # Add title and markdown introduction
        self.add_markdown_cell("## Data Synthesis Pipeline")
        
        # Install KFP library
        self.add_markdown_cell("### Install Kubeflow Pipelines module")
        self.add_code_cell('#Colab\n#!pip install kfp==1.8.22\n#VSCode\n#%pip install kfp==1.8.22')
        self.add_code_cell('from kfp import dsl\nfrom kfp.compiler import Compiler\nfrom kfp import components as comp\nfrom typing import NamedTuple')
        
        components = self.pipeline_dict['components']
        # Input Data Section
        if 'input' in components:
            input_section = InputSection(components['input'], self.nb, self.base_image)
            input_section.generate()
        
        # Preprocess Section
        if 'preprocess' in components:
            preprocess_section = PreprocessSection(components['preprocess'], self.nb, self.base_image)
            preprocess_section.generate()
        
        # Generation Section
        if 'generation' in components:
            generation_section = GenerationSection(components['generation'], self.nb, self.base_image)
            generation_section.generate()
        
        # Privacy Report Section
        if 'privacy_report' in components:
            privacy_report_section = PrivacyReportSection(components['privacy_report'], self.nb, self.base_image)
            privacy_report_section.generate()
        
        # Utility Report Section
        if 'utility_report' in components:
            utility_report_section = UtilityReportSection(components['utility_report'], self.nb, self.base_image)
            utility_report_section.generate()
        
        # Diagnostic Report Section
        if 'diagnostic_report' in components:
            diagnostic_report_section = DiagnosticReportSection(components['diagnostic_report'], self.nb, self.base_image)
            diagnostic_report_section.generate()
        
        # Pipeline compiling cell
        self.add_markdown_cell('## Pipeline')
        self.add_markdown_cell('Connect all the modules and compile the pipeline')
        self.add_markdown_cell(f"""### Example
```
@dsl.pipeline(name='example_pipeline', description='example_desc')
def pipeline():
	input = input_component()
	preprocess = preprocess_component(input.output)
	generation = generation_component(input.output, preprocess.output)
	dianostic = diagnostic_report_component(input.output, generation.output, preprocess.output)
	utility = utility_report_component(input.output, generation.output, preprocess.output)
	privacy = privacy_report_component(input.output, generation.output, preprocess.output)
```
""")
        self.add_code_cell(f'@dsl.pipeline(name="{self.pipeline_name}", description="{self.pipeline_description}")\ndef pipeline():\n\t#TODO\n\tpass')
        self.add_code_cell(f'Compiler().compile(pipeline, "{self.pipeline_name}.yaml")')

        # Mandatory to run! Adds image pull secret
        self.add_markdown_cell('## Add ImagePullSecret. Mandatory to run for Kubeflow execution!')
        imagePullCode = f"""
import yaml
with open("{self.pipeline_name}.yaml", "r") as file:
    workflow_yaml = yaml.safe_load(file)
workflow_yaml["spec"]["imagePullSecrets"] = [{{"name": "regcred"}}]
with open("{self.pipeline_name}.yaml", "w") as file:
    yaml.dump(workflow_yaml, file, default_flow_style=False)
        """
        self.add_code_cell(imagePullCode)
        
        # Save the notebook
        with open(self.notebook_path, 'w') as f:
            nbf.write(self.nb, f)
        
        print(f'{self.notebook_path} was successfully generated and saved!')