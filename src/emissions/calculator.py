import json

class CarbonCalculator:
    def __init__(self, data_file='src/knowledge_base/data.json'):
        self.data = self._load_data(data_file)
        
    def _load_data(self, data_file):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: The data file '{data_file}' was not found.")
            return None

    def get_embodied_emissions(self, product_name):
        """
        Fetches the embodied emissions for a given product.
        
        Args:
            product_name (str): The name of the product.
            
        Returns:
            float: The embodied emissions in kg CO2, or None if not found.
        """
        for product in self.data['products']:
            if product['name'] == product_name:
                return product.get('embodied_emissions_kg_co2')
        return None
    
    def get_operational_emissions(self, product_name, usage_hours, power_rating_watts, region_carbon_intensity=0.4):
        """
        Calculates operational emissions for an appliance.
        
        Args:
            product_name (str): The name of the appliance.
            usage_hours (float): The duration of usage in hours.
            power_rating_watts (float): The power rating of the appliance.
            region_carbon_intensity (float): Grams CO2 per kWh (default is a general estimate).
            
        Returns:
            float: The operational emissions in kg CO2.
        """
        # Convert watts to kilowatts and hours to kWh
        kwh = (power_rating_watts * usage_hours) / 1000
        # Calculate emissions: kWh * region_carbon_intensity (g/kWh) / 1000 (g/kg)
        emissions_kg_co2 = (kwh * region_carbon_intensity) / 1000
        return emissions_kg_co2