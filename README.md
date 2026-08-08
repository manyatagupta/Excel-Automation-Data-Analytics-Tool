# Excel Automation & Data Analytics Tool

## Project Overview
This is a complete, production-quality web application built with Python and Streamlit. The tool allows users to upload an Excel (.xlsx/.xls) or CSV file, and automatically clean, analyze, visualize, and generate reports from the uploaded dataset. It is designed to be simple, clean, professional, and beginner-friendly.

## Features
- **Upload Dataset:** Supports `.csv`, `.xlsx`, and `.xls` files.
- **Data Quality Check:** Automatically analyzes data quality (missing values, duplicates, column types).
- **Automated Data Cleaning:** Handles missing values, removes duplicates, trims whitespace, and converts data types.
- **Key Statistics:** Provides summary statistics for numeric and categorical columns.
- **Visualizations:** Automatically generates Matplotlib and Plotly charts based on data types.
- **Pivot-Style Analysis:** Allows users to create pivot table summaries.
- **Automatic Insights:** Generates rule-based insights dynamically.
- **Report Generation:** Export cleaned data to Excel/CSV and generate a professional PDF report.

## Tech Stack
- Python 3.11+
- Streamlit
- Pandas & NumPy
- Matplotlib & Plotly
- OpenPyXL
- ReportLab

## Project Structure
```text
excel-automation-tool/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── generate_sample_data.py     # Script to generate sample data
├── modules/                    # Core logic modules
│   ├── __init__.py
│   ├── data_loader.py          # Handles file upload and loading
│   ├── data_cleaner.py         # Handles data cleaning operations
│   ├── analyzer.py             # Statistical and pivot analysis
│   ├── visualizer.py           # Chart generation
│   ├── report_generator.py     # PDF and Excel report creation
│   └── utils.py                # Helper functions
└── sample_data/
    └── sample_sales_data.xlsx  # Synthetic dataset for testing
```

## Installation

1. Clone or download this repository.
2. Ensure you have Python 3.11+ installed.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run Instructions

Run the application using Streamlit:
```bash
streamlit run app.py
```

## Example Workflow
1. Run the application.
2. Upload the `sample_data/sample_sales_data.xlsx` file (generate it first using `python generate_sample_data.py` if it doesn't exist).
3. Review the Data Quality Summary.
4. Go to the "Automated Cleaning" tab and click "Clean Data".
5. Explore the "Key Statistics" and "Visualizations" tabs.
6. Create a pivot summary in the "Pivot Analysis" tab.
7. Go to the "Download Reports" tab to export the cleaned data and PDF report.

## Future Improvements
- Support for larger datasets via Dask or chunking.
- More advanced data imputation methods.
- Customizable report templates.

## Author
[Your Name]
