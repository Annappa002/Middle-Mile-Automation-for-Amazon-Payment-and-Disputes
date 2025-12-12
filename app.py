"""
Main application for Middle Mile Support for Amazon Payment and Dispute Automation
"""
import os
from flask import Flask, request, jsonify, render_template, send_file
from services.sop_parser import SopParser
from services.payment_calculator import PaymentCalculator
from services.dispute_analyzer import DisputeAnalyzer
from services.report_analyzer import ReportAnalyzer
from services.cross_checker import CrossChecker
from models.ml_model import MLModel
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main UI page"""
    return render_template('index.html')

@app.route('/upload_sop', methods=['POST'])
def upload_sop():
    """Handle SOP file upload and analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    # Save file temporarily
    filepath = os.path.join('data', file.filename)
    file.save(filepath)
    
    try:
        # Parse the SOP
        parser = SopParser()
        sop_data = parser.parse(filepath)
        
        # Calculate payment
        calculator = PaymentCalculator()
        payment_result = calculator.calculate(sop_data)
        
        # Analyze for disputes
        analyzer = DisputeAnalyzer()
        dispute_result = analyzer.analyze(sop_data)
        
        # Apply ML model for enhanced decision making
        ml_model = MLModel()
        ml_result = ml_model.predict(sop_data)
        
        return jsonify({
            'success': True,
            'payment_decision': payment_result,
            'dispute_analysis': dispute_result,
            'ml_enhanced_result': ml_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/upload_report', methods=['POST'])
def upload_report():
    """Handle report file upload and analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    report_type = request.form.get('report_type', 'rate_card')
    
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    # Save file temporarily
    filepath = os.path.join('data', file.filename)
    file.save(filepath)
    
    try:
        # Analyze the report
        analyzer = ReportAnalyzer()
        
        if report_type == 'settlement':
            analysis_result = analyzer.analyze_settlement_report(filepath)
        else:
            analysis_result = analyzer.analyze_rate_card(filepath)
        
        return jsonify({
            'success': True,
            'analysis_type': report_type,
            'analysis_result': analysis_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/cross_check', methods=['POST'])
def cross_check():
    """Handle cross-checking of SOP, rate card, and settlement report"""
    # Get uploaded files
    sop_file = request.files.get('sop_file')
    rate_card_file = request.files.get('rate_card_file')
    settlement_file = request.files.get('settlement_file')
    
    if not sop_file or not rate_card_file or not settlement_file:
        return jsonify({'error': 'All three files (SOP, rate card, settlement report) are required'}), 400
    
    # Save files temporarily
    sop_path = os.path.join('data', sop_file.filename)
    rate_card_path = os.path.join('data', rate_card_file.filename)
    settlement_path = os.path.join('data', settlement_file.filename)
    
    sop_file.save(sop_path)
    rate_card_file.save(rate_card_path)
    settlement_file.save(settlement_path)
    
    try:
        # Perform cross-checking
        cross_checker = CrossChecker()
        cross_check_result = cross_checker.cross_check_all(sop_path, rate_card_path, settlement_path)
        
        return jsonify({
            'success': True,
            'cross_check_result': cross_check_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        for path in [sop_path, rate_card_path, settlement_path]:
            if os.path.exists(path):
                os.remove(path)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate Excel report with tour analysis and remarks"""
    # Get uploaded files
    sop_file = request.files.get('sop_file')
    rate_card_file = request.files.get('rate_card_file')
    settlement_file = request.files.get('settlement_file')
    
    if not sop_file or not rate_card_file or not settlement_file:
        return jsonify({'error': 'All three files (SOP, rate card, settlement report) are required'}), 400
    
    # Save files temporarily
    sop_path = os.path.join('data', sop_file.filename)
    rate_card_path = os.path.join('data', rate_card_file.filename)
    settlement_path = os.path.join('data', settlement_file.filename)
    
    sop_file.save(sop_path)
    rate_card_file.save(rate_card_path)
    settlement_file.save(settlement_path)
    
    try:
        # Perform cross-checking
        cross_checker = CrossChecker()
        cross_check_result = cross_checker.cross_check_all(sop_path, rate_card_path, settlement_path)
        
        # Generate Excel report
        report_filename = f"tour_analysis_report_{sop_file.filename.split('.')[0]}.xlsx"
        report_path = os.path.join('data', report_filename)
        
        success = cross_checker.generate_excel_report(cross_check_result, report_path)
        
        if success:
            return send_file(report_path, as_attachment=True)
        else:
            return jsonify({'error': 'Failed to generate Excel report'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        for path in [sop_path, rate_card_path, settlement_path]:
            if os.path.exists(path):
                os.remove(path)

@app.route('/generate_payment_report', methods=['POST'])
def generate_payment_report():
    """Generate payment report Excel file"""
    # Get uploaded files
    sop_file = request.files.get('sop_file')
    rate_card_file = request.files.get('rate_card_file')
    settlement_file = request.files.get('settlement_file')
    
    if not sop_file or not rate_card_file or not settlement_file:
        return jsonify({'error': 'All three files (SOP, rate card, settlement report) are required'}), 400
    
    # Save files temporarily
    sop_path = os.path.join('data', sop_file.filename)
    rate_card_path = os.path.join('data', rate_card_file.filename)
    settlement_path = os.path.join('data', settlement_file.filename)
    
    sop_file.save(sop_path)
    rate_card_file.save(rate_card_path)
    settlement_file.save(settlement_path)
    
    try:
        # Perform cross-checking
        cross_checker = CrossChecker()
        cross_check_result = cross_checker.cross_check_all(sop_path, rate_card_path, settlement_path)
        
        # Generate payment report
        report_filename = f"payment_report_{sop_file.filename.split('.')[0]}.xlsx"
        report_path = os.path.join('data', report_filename)
        
        success = cross_checker.generate_payment_report(cross_check_result, report_path)
        
        if success:
            return send_file(report_path, as_attachment=True)
        else:
            return jsonify({'error': 'Failed to generate payment report'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        for path in [sop_path, rate_card_path, settlement_path]:
            if os.path.exists(path):
                os.remove(path)

@app.route('/generate_dispute_report', methods=['POST'])
def generate_dispute_report():
    """Generate dispute report Excel file"""
    # Get uploaded files
    sop_file = request.files.get('sop_file')
    rate_card_file = request.files.get('rate_card_file')
    settlement_file = request.files.get('settlement_file')
    
    if not sop_file or not rate_card_file or not settlement_file:
        return jsonify({'error': 'All three files (SOP, rate card, settlement report) are required'}), 400
    
    # Save files temporarily
    sop_path = os.path.join('data', sop_file.filename)
    rate_card_path = os.path.join('data', rate_card_file.filename)
    settlement_path = os.path.join('data', settlement_file.filename)
    
    sop_file.save(sop_path)
    rate_card_file.save(rate_card_path)
    settlement_file.save(settlement_path)
    
    try:
        # Perform cross-checking
        cross_checker = CrossChecker()
        cross_check_result = cross_checker.cross_check_all(sop_path, rate_card_path, settlement_path)
        
        # Generate dispute report
        report_filename = f"dispute_report_{sop_file.filename.split('.')[0]}.xlsx"
        report_path = os.path.join('data', report_filename)
        
        success = cross_checker.generate_dispute_report(cross_check_result, report_path)
        
        if success:
            return send_file(report_path, as_attachment=True)
        else:
            return jsonify({'error': 'Failed to generate dispute report'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        for path in [sop_path, rate_card_path, settlement_path]:
            if os.path.exists(path):
                os.remove(path)

@app.route('/generate_payment_and_dispute_reports', methods=['POST'])
def generate_payment_and_dispute_reports():
    """Generate separate payment and dispute reports with exact data from settlement file"""
    # Get uploaded files
    sop_file = request.files.get('sop_file')
    rate_card_file = request.files.get('rate_card_file')
    settlement_file = request.files.get('settlement_file')
    
    if not sop_file or not rate_card_file or not settlement_file:
        return jsonify({'error': 'All three files (SOP, rate card, settlement report) are required'}), 400
    
    # Save files temporarily
    sop_path = os.path.join('data', sop_file.filename)
    rate_card_path = os.path.join('data', rate_card_file.filename)
    settlement_path = os.path.join('data', settlement_file.filename)
    
    sop_file.save(sop_path)
    rate_card_file.save(rate_card_path)
    settlement_file.save(settlement_path)
    
    try:
        # Perform cross-checking
        cross_checker = CrossChecker()
        cross_check_result = cross_checker.cross_check_all(sop_path, rate_card_path, settlement_path)
        
        # Create a temporary directory for the reports
        temp_dir = tempfile.mkdtemp()
        
        # Generate payment and dispute reports
        success = cross_checker.generate_payment_and_dispute_reports(cross_check_result, temp_dir)
        
        if success:
            # Return both files as a zip
            import zipfile
            zip_filename = f"payment_dispute_reports_{sop_file.filename.split('.')[0]}.zip"
            zip_path = os.path.join('data', zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                zipf.write(os.path.join(temp_dir, 'payment_report.xlsx'), 'payment_report.xlsx')
                zipf.write(os.path.join(temp_dir, 'dispute_report.xlsx'), 'dispute_report.xlsx')
            
            # Clean up temporary directory
            import shutil
            shutil.rmtree(temp_dir)
            
            return send_file(zip_path, as_attachment=True)
        else:
            return jsonify({'error': 'Failed to generate payment and dispute reports'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        for path in [sop_path, rate_card_path, settlement_path]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == '__main__':
    app.run(debug=True)