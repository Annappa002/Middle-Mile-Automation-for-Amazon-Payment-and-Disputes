"""
Demo script to showcase the Cross-Checking functionality
"""
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from services.cross_checker import CrossChecker

def demo_cross_check():
    """Demonstrate cross-checking functionality"""
    print("=== Cross-Checking Demo ===")
    
    # Initialize cross-checker
    cross_checker = CrossChecker()
    
    # Define file paths
    sop_file = "data/sample_sop.txt"
    rate_card_file = "data/sample_rate_card.csv"
    settlement_file = "data/sample_settlement_report.csv"
    
    # Check that all files exist
    missing_files = []
    for file_path in [sop_file, rate_card_file, settlement_file]:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"Error: Missing required files: {missing_files}")
        return
    
    print("Cross-checking SOP, Rate Card, and Settlement Report...")
    
    try:
        # Perform cross-checking
        result = cross_checker.cross_check_all(sop_file, rate_card_file, settlement_file)
        
        # Display results
        print("\n--- CROSS-CHECK RESULTS ---")
        
        # Data Summary
        print("\n1. DATA SUMMARY:")
        data_summary = result['data_summary']
        print(f"   SOP Factors Extracted: {len(data_summary['sop_factors'])}")
        print(f"   Rate Card Records: {data_summary['rate_card_records']}")
        print(f"   Settlement Records: {data_summary['settlement_records']}")
        
        # Consistency Checks
        print("\n2. CONSISTENCY CHECKS:")
        inconsistencies = result['consistency_checks']
        if inconsistencies:
            for i, issue in enumerate(inconsistencies, 1):
                print(f"   {i}. {issue['description']} (Severity: {issue['severity']})")
        else:
            print("   No consistency issues found")
        
        # Payment Accuracy
        print("\n3. PAYMENT ACCURACY ANALYSIS:")
        payment = result['payment_accuracy']
        print(f"   Expected Payment: ${payment['expected_payment']:.2f}")
        print(f"   Actual Payment: ${payment['actual_payment']:.2f}")
        print(f"   Payment Variance: ${payment['variance']:.2f}")
        print(f"   Accuracy Percentage: {payment['accuracy_percentage']:.1f}%")
        
        # Risk Assessment
        print("\n4. RISK ASSESSMENT:")
        risk = result['risk_assessment']
        print(f"   Overall Risk Score: {risk['overall_risk_score']:.2f} ({risk['severity']})")
        if risk['risk_factors']:
            print("   Risk Factors:")
            for i, factor in enumerate(risk['risk_factors'], 1):
                print(f"     {i}. {factor['description']} (Severity: {factor['severity']})")
        else:
            print("   No significant risk factors identified")
        
        # Recommendations
        print("\n5. RECOMMENDATIONS:")
        recommendations = result['recommendations']
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("   No recommendations provided")
        
        # Insights
        print("\n6. KEY INSIGHTS:")
        insights = result['insights']
        if insights:
            for i, insight in enumerate(insights, 1):
                print(f"   {i}. {insight}")
        else:
            print("   No insights generated")
            
    except Exception as e:
        print(f"Error during cross-checking: {e}")
        return

def main():
    """Run the cross-checking demo"""
    print("=== Middle Mile Cross-Checking Demo ===")
    demo_cross_check()
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    main()