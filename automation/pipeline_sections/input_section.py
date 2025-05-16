from pipeline_sections.notebook_section import NotebookSection
class InputSection(NotebookSection):
    def generate(self):
        input_type = self.dictionary['type']
        code_cell = ""
        
        # Class initialization
        self.add_markdown_cell("## InputHandler Class")
        code_cell += 'from synthguard.input_handler import InputHandler' + "\n"
        code_cell += 'inputHandler = InputHandler()' + "\n"
        
        # Data loading
        if input_type == 'csv':
            source_type = list(self.dictionary.keys())[2]
            source = self.dictionary[source_type]
            self.add_markdown_cell("### Input data from URL")
            code_cell += f'input_data = inputHandler.load_data_from_url("{ source }")' + "\n"
        
        # Add all the added lines to a single cell
        self.add_code_cell(code_cell)
        
        # Add KFP section
        if self.kfp:
            self.add_kfp(code_cell, 'input_component')