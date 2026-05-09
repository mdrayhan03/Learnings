# What your app expects
class ModernAnalytics:
    def get_json_data(self):
        return '{"source": "modern", "value": 100}'

# The "Incompatible" Legacy Class
class LegacyVendor:
    def get_xml_data(self):
        return '<data><source>legacy</source><value>50</value></data>'

class LegacyAdapter() :
    def __init__(self, legacy_vendor):
        self.vendor = legacy_vendor
    def get_json_data(self) :
        self.vendor.get_xml_data()

        # converting code

        data = '{"source": "legacy", "value": 50}' 

        return data

# --- The Messy Client ---
def process_data(provider):
    data = provider.get_json_data() 
    
    print(f"Processing: {data}")

# Execution
process_data(ModernAnalytics())
vendor_instance = LegacyVendor()
adapter = LegacyAdapter(vendor_instance)
process_data(adapter)