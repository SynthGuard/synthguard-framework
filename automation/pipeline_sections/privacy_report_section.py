from pipeline_sections.notebook_section import NotebookSection
class PrivacyReportSection(NotebookSection):

    def generate(self):
        self.add_markdown_cell("## Privacy Report Class")
        code_cell = ""
        
        # Init
        code_cell += 'from synthguard.privacy_report_generator import PrivacyRiskEvaluator' + "\n"
        code_cell += 'synthetic_data = sd.load_data_csv(input_synth_csv)' + "\n"
        code_cell += 'real_data = sd.load_data_csv(input_real_csv)' + "\n"
        code_cell += 'metadata = sd.load_metadata(input_json)' + "\n"
        code_cell += 'privacyRiskEvaluator = PrivacyRiskEvaluator(real_data = real_data, synthetic_data = synthetic_data, metadata = metadata, method="realistic")' + "\n"
        
        # Evaluate
        code_cell += 'privacyRiskEvaluator.evaluate_privacy()' + "\n"
        code_cell += 'privacyRiskEvaluator.visualize_privacy_report()' + "\n"
        
        self.add_code_cell(code_cell)
        
        # Add KFP section
        if self.kfp == True:
            self.add_kfp(code_cell, 'privacy_report_component')
