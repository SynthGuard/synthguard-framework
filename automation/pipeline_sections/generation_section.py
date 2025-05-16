from pipeline_sections.notebook_section import NotebookSection
class GenerationSection(NotebookSection):

    def generate(self):
        generation_type = self.dictionary['type']
        n_rows = self.dictionary['n_rows']
        code_cell = ""
        
        self.add_markdown_cell("## SyntheticDataGenerator Class")
        # Initialize class
        code_cell += 'from synthguard.synthetic_data_generator import SyntheticDataGenerator' + "\n"
        code_cell += f'syntheticDataGenerator = SyntheticDataGenerator(output_csv=None, n_rows={ n_rows }, method="{ generation_type }")' + "\n"
        
        # Add code cell for Generation method (assuming you have functions in a local library)
        code_cell += 'generated_data = syntheticDataGenerator.generate_synthetic_data(metadata=metadata, processed_data=processed_data)' + "\n"
        
        # Add all code to a single cell
        self.add_code_cell(code_cell)
        
        # Add KFP section
        if self.kfp == True:
            self.add_kfp(code_cell, 'generation_component')