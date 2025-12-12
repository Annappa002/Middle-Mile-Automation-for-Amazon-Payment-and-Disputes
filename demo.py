"""
Demo script to showcase the Middle Mile Automation Application
"""
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from services.sop_parser import SopParser
from services.payment_calculator import PaymentCalculator
from services.dispute_analyzer import DisputeAnalyzer
from models.ml_model import MLModel

def demo():
    """Demonstrate the application with a sample SOP"""
    print("=== Middle Mile Automation Demo ===")
    
    # Parse the sample SOP
    print("\n1. Parsing Sample SOP...")
    parser = SopParser()
    sop_data = parser.parse("data/sample_sop.txt")
    print("Extracted factors:", sop_data)
    
    # Calculate payment
    print("\n2. Calculating Payment...")
    calculator = PaymentCalculator()
    payment_result = calculator.calculate(sop_data)
    print("Payment Decision:", payment_result)
    
    # Analyze for disputes
    print("\n3. Analyzing for Disputes...")
    analyzer = DisputeAnalyzer()
    dispute_result = analyzer.analyze(sop_data)
    print("Dispute Analysis:", dispute_result)
    
    # Apply ML model (note: this will use default values since we don't have a trained model)
    print("\n4. Applying ML Model...")
    ml_model = MLModel()
    ml_result = ml_model.predict(sop_data)
    print("ML Enhanced Result:", ml_result)
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()