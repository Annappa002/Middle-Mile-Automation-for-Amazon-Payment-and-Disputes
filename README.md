# Middle Mile Support - Amazon Payment & Dispute Automation

This application automates payment decisions and dispute identification for Amazon's middle-mile logistics operations based on Standard Operating Procedures (SOPs).

## Features

1. **SOP Parsing**: Automatically extracts key factors from SOP documents (PDF, DOCX, TXT)
2. **Payment Calculation**: Determines if payment should be made to vendors and calculates amounts
3. **Dispute Analysis**: Identifies potential disputes based on risk factors
4. **AI/ML Enhancement**: Uses machine learning models to improve decision accuracy
5. **Web Interface**: User-friendly interface for uploading SOPs and viewing results

## Key Factors Considered

- Vehicle Type (bike, car, van, truck, heavy truck)
- Advance Amount
- Delivery Distance
- Delivery Time
- Vendor Rating
- Shipment Value
- Special Handling Requirements
- Hazardous Materials
- Fragile Goods

## Installation

1. Clone the repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload an SOP document (PDF, DOCX, or TXT)

4. View the analysis results including:
   - Payment decision and calculated amount
   - Potential disputes and risk assessment
   - Machine learning enhanced recommendations
   - Extracted factors from the SOP

## Architecture

```
middle_mile_automation/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── README.md           # This file
├── templates/          # HTML templates
│   └── index.html      # Main UI
├── services/           # Business logic services
│   ├── sop_parser.py        # SOP parsing service
│   ├── payment_calculator.py # Payment calculation service
│   └── dispute_analyzer.py  # Dispute analysis service
├── models/             # Machine learning models
│   └── ml_model.py          # ML model implementation
├── data/               # Data storage (uploads, etc.)
└── tests/              # Unit tests
```

## Machine Learning Models

The application uses:
1. **Random Forest Classifier** for payment decision predictions
2. **Deep Learning Model** for complex pattern recognition

Models are trained on historical data to improve accuracy over time.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is proprietary to Amazon and intended for internal use only.