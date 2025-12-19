# src/agent_tools.py
from langchain.agents import Tool
from src.detection.image_detector import ImageDetector
from src.emissions.calculator import CarbonCalculator
from src.recommendations.engine import RecommendationEngine

# Initialize modules
detector = ImageDetector()
calculator = CarbonCalculator()
recommender = RecommendationEngine()

# Define tools
tools = [
    Tool(
        name="ImageDetector",
        func=lambda file_path: detector.detect(file_path),
        description="Detect product name from an uploaded image file path."
    ),
    Tool(
        name="CarbonCalculator",
        func=lambda product: calculator.get_embodied_emissions(product),
        description="Calculate embodied carbon emissions (kg CO2) for a product name."
    ),
    Tool(
        name="RecommendationEngine",
        func=lambda product: recommender.get_recommendations(product).get("alternatives", []),
        description="Suggest eco-friendly alternatives for a product."
    )
]
