class SupportSystem:
    def handle_request(self, issue_type, severity):
        # The 'God Function' - it knows too much and does too much.
        if issue_type == "billing":
            print(f"Billing Dept: Processing payment issue with severity {severity}.")
        
        elif issue_type == "technical":
            if severity == "critical":
                print(f"Senior Engineer: Fixing critical server failure!")
            else:
                print(f"Junior Tech: Fixing minor technical glitch.")
        
        elif issue_type == "general":
            print(f"Bot: Automated response sent for general inquiry.")
        
        else:
            print("System: Issue type unknown. Request dropped.")

# Execution
support = SupportSystem()
support.handle_request("technical", "critical")
support.handle_request("billing", "low")