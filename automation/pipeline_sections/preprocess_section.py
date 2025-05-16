from pipeline_sections.notebook_section import NotebookSection
class PreprocessSection(NotebookSection):
    def generate(self):
        self.add_markdown_cell("## DataPreprocessor Class")
        code_cell = ""
        
        # Initialize class
        code_cell += 'from synthguard.data_preprocessor import DataPreprocessor' + "\n"
        code_cell += 'input_data = sd.load_data_csv(input_csv)' + "\n"
        code_cell += 'dataPreprocessor = DataPreprocessor(data=input_data)' + "\n"
        # Preprocess
        code_cell += 'metadata = dataPreprocessor.extract_metadata()' + "\n"
        code_cell += 'processed_data = dataPreprocessor.data' + "\n"
        
        # Add all code to a single cell
        self.add_code_cell(code_cell)
        
        # Add KFP section
        if self.kfp == True:
            self.add_kfp(code_cell, 'preprocess_component')
