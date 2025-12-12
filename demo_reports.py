"""
Demo script to showcase the Report Analysis functionality
"""
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from services.report_analyzer import ReportAnalyzer

def demo_rate_card_analysis():
    """Demonstrate rate card analysis"""
    print("=== Rate Card Analysis Demo ===")
    
    # Analyze the sample rate card
    analyzer = ReportAnalyzer()
    result = analyzer.analyze_rate_card("data/sample_rate_card.csv")
    
    print(f"Total Records: {result['total_records']}")
    print(f"Columns: {', '.join(result['columns'])}")
    print(f"Vehicle Distribution: {result['vehicle_distribution']}")
    
    if 'rate_analysis' in result and 'by_vehicle_type' in result['rate_analysis']:
        print("Rate Analysis by Vehicle Type:")
        by_vehicle_data = result['rate_analysis']['by_vehicle_type']
        # Print the structure to understand it better
        print(f"  Data structure: {by_vehicle_data}")
    
    print(f"Recommendations: {result['recommendations']}")
    print()

def demo_settlement_report_analysis():
    """Demonstrate settlement report analysis"""
    print("=== Settlement Report Analysis Demo ===")
    
    # Analyze the sample settlement report
    analyzer = ReportAnalyzer()
    result = analyzer.analyze_settlement_report("data/sample_settlement_report.csv")
    
    print(f"Total Transactions: {result['total_transactions']}")
    print(f"Columns: {', '.join(result['columns'])}")
    
    if 'financial_summary' in result and 'amount_statistics' in result['financial_summary']:
        print("Financial Summary:")
        for column, stats in result['financial_summary']['amount_statistics'].items():
            print(f"  {column}: Total = ${stats['total']:.2f}, Mean = ${stats['mean']:.2f}")
    
    if 'vendor_performance' in result:
        print("Vendor Performance:")
        # This would show vendor performance metrics if we had the right data structure
        print(f"  Data structure: {result['vendor_performance']}")
    
    if 'discrepancies' in result and result['discrepancies']:
        print("Discrepancies Found:")
        for discrepancy in result['discrepancies']:
            print(f"  - {discrepancy['description']}")
    else:
        print("No discrepancies found")
    
    print(f"Recommendations: {result['recommendations']}")
    print()

def main():
    """Run all demos"""
    print("=== Middle Mile Report Analysis Demos ===")
    demo_rate_card_analysis()
    demo_settlement_report_analysis()
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main()