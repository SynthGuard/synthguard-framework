from pipeline_sections.notebook_section import NotebookSection
class UtilityReportSection(NotebookSection):

    def generate(self):
        self.add_markdown_cell("## Utility Report Class")
        code_cell = ""
        
        # Init
        code_cell += 'from synthguard.utility_report_generator import UtilityEvaluator' + "\n"
        code_cell += 'synthetic_data = sd.load_data_csv(input_synth_csv)' + "\n"
        code_cell += 'real_data = sd.load_data_csv(input_real_csv)' + "\n"
        code_cell += 'metadata = sd.load_metadata(input_json)' + "\n"
        code_cell += 'utilityEvaluator = utilityEvaluator(real_data = real_data, synthetic_data = synthetic_data, metadata = metadata, method="realistic")' + "\n"
        
        # Evaluate
        code_cell += 'utilityEvaluator.evaluate_utility()' + "\n"
        code_cell += 'utilityEvaluator.visualize_utility_report()' + "\n"
        
        self.add_code_cell(code_cell)
        
        # Add KFP section
        if self.kfp == True:
            self.add_kfp(code_cell, 'utility_report_component')