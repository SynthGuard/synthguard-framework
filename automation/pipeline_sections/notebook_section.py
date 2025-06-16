import nbformat as nbf

class NotebookSection:
    def __init__(self, dictionary, notebook, base_image, kfp=True):
        self.dictionary = dictionary
        self.notebook = notebook
        self.kfp = kfp
        self.base_image = base_image

    def add_markdown_cell(self, text):
        self.notebook['cells'].append(nbf.v4.new_markdown_cell(text))

    def add_code_cell(self, code):
        self.notebook['cells'].append(nbf.v4.new_code_cell(code))

    # Generates a Python function string for a Kubeflow Pipelines component.
    def generate_kfp_function_code(self, code: str, component_name: str, base_image:str) -> str:
        """Generates a Python function string for a Kubeflow Pipelines component."""
        indented_code = '\n'.join('    ' + line for line in code.splitlines())

        template = f"""
def {component_name}(parameters):
    import synthguard.helper_functions as sd
    #Component logic
{indented_code}
    # Compiling function into a KFP component
{component_name} = comp.create_component_from_func(func={component_name}, base_image='{base_image}')
"""
        parameters = "input_csv: comp.InputPath('csv'), output_csv: comp.OutputPath('csv')"
        template = template.replace('parameters', parameters)

        return template

    # Generates a Python function string for a Kubeflow Pipelines visualization component.
    def generate_kfp_visual_function_code(self, code: str, component_name: str, base_image:str) -> str:
        """Generates a Python function string for a Kubeflow Pipelines component."""
        indented_code = '\n'.join('    ' + line for line in code.splitlines())

        template = f"""
def {component_name}(parameters) -> NamedTuple('VisualizationOutput', [('mlpipeline_ui_metadata', 'UI_metadata')]):
    import synthguard.helper_functions as sd
    import json

    with open(output_html, "w") as f:
        f.write("<html><body>")  # Start the HTML document

    #Component logic
{indented_code}

    #Write visualization elements into output_html file

    # Read the HTML content for UI metadata
    with open(output_html, 'r') as file:
        html_content = file.read()
    metadata = {{
        'outputs': [{{'type': 'web-app', 'storage': 'inline', 'source': html_content}}]
    }}

    from collections import namedtuple
    visualization_output = namedtuple('VisualizationOutput', ['mlpipeline_ui_metadata'])
    return visualization_output(json.dumps(metadata))

    # Compiling function into a KFP component
{component_name} = comp.create_component_from_func(func={component_name}, base_image='{base_image}')
"""
        parameters = "input_synth_csv: comp.InputPath('csv'), input_real_csv: comp.InputPath('csv'), input_json:comp.InputPath('json'), output_html: comp.OutputPath('html')"
        template = template.replace('parameters', parameters)

        return template

    def add_kfp(self, code, name):
        if 'report' in name.lower():
            self.add_markdown_cell('Kubeflow Pipelines Visual Component - Adjust function parameters accordingly')
            self.add_code_cell(self.generate_kfp_visual_function_code(code=code, component_name=name, base_image=self.base_image))
        else:
            self.add_markdown_cell('Kubeflow Pipelines Component - Adjust function parameters accordingly')
            self.add_code_cell(self.generate_kfp_function_code(code=code, component_name=name, base_image=self.base_image))