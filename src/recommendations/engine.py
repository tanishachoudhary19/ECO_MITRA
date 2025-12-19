# src/recommendations/engine.py
import json

class RecommendationEngine:
    def __init__(self, data_file='src/knowledge_base/data.json'):
        self.data = self._load_data(data_file)
        
    def _load_data(self, data_file):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: The data file '{data_file}' was not found.")
            return None

    def get_recommendations(self, product_name):
        """
        Provides personalized suggestions to reduce emissions for a given product.
        """
        for product in self.data['products']:
            if product['name'] == product_name:
                alternatives = product.get('alternatives')
                return {"alternatives": alternatives}
        return None