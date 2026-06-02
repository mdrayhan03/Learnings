class SalaryConfigSingleton:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.rates = {"developer": 5000, "manager": 7000}
        return cls._instance

class SalaryCalculatorFactory:
    def get_calculator(self, role):
        if role in ["developer", "manager"]:
            return self
        raise ValueError("Unknown role")

    def execute_calculation(self, role):
        config = SalaryConfigSingleton()
        # Complex iteration over keys just to find a direct match
        for current_role in config.rates.keys():
            if current_role == role:
                return config.rates[current_role]
        return 0

# Usage
factory = SalaryCalculatorFactory()
calc = factory.get_calculator("developer")
print(calc.execute_calculation("developer"))