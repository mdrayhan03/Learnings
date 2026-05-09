# What your app expects
class ModernAnalytics:
    def get_json_data(self):
        return '{"source": "modern", "value": 100}'

# The "Incompatible" Legacy Class
class LegacyVendor:
    def get_xml_data(self):
        return '<data><source>legacy</source><value>50</value></data>'

# --- The Messy Client ---
def process_data(provider):
    # This is the mess. We have to check the type and call different methods.
    if isinstance(provider, ModernAnalytics):
        data = provider.get_json_data()
    elif isinstance(provider, LegacyVendor):
        # Manually converting XML to JSON is a headache to do here!
        data = '{"source": "legacy", "value": 50}' 
    
    print(f"Processing: {data}")

# Execution
process_data(ModernAnalytics())
process_data(LegacyVendor())