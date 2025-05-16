from pipeline_sections.notebook_section import NotebookSection
class DiagnosticReportSection(NotebookSection):

    def generate(self):
        self.add_markdown_cell("## Diagnostic Report Class")
        code_cell = ""
        
        # Init
        code_cell += 'from synthguard.diagnostic_report_generator import DiagnosticEvaluator' + "\n"
        code_cell += 'diagnosticEvaluator = DiagnosticEvaluator(real_data=processed_data, synthetic_data=generated_data, metadata=metadata)' + "\n"
        
        # Evaluate
        code_cell += 'diagnosticEvaluator.evaluate_diagnostic()' + "\n"
        code_cell += 'diagnosticEvaluator.visualize_diagnostic_report()' + "\n"
        
        self.add_code_cell(code_cell)
        
        # Add KFP section
        if self.kfp == True:
            self.add_kfp(code_cell, 'diagnostic_report_component')
