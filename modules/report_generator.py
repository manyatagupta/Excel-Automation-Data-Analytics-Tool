import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_excel_report(cleaned_df, quality_summary, stats_df, pivot_df, insights, file_name="Report.xlsx"):
    """
    Generates a multi-sheet Excel report.
    Returns the raw bytes of the Excel file.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Cleaned Data
        cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        
        # Sheet 2: Data Quality
        if quality_summary is not None:
            quality_summary.to_excel(writer, sheet_name='Data Quality', index=False)
            
        # Sheet 3: Summary Statistics
        if stats_df is not None:
            # stats_df has the metric names as columns, we might want to include the index (column names)
            stats_df.to_excel(writer, sheet_name='Summary Statistics')
            
        # Sheet 4: Pivot Analysis
        if pivot_df is not None:
            pivot_df.to_excel(writer, sheet_name='Pivot Analysis', index=False)
            
        # Sheet 5: Insights
        if insights:
            insights_df = pd.DataFrame({"Insights": insights})
            insights_df.to_excel(writer, sheet_name='Insights', index=False)
            
        # Optional: Auto-adjust column widths (basic implementation)
        for sheetname in writer.sheets:
            worksheet = writer.sheets[sheetname]
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter # Get the column name
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column].width = min(adjusted_width, 50) # Cap width at 50

    return output.getvalue()


def generate_pdf_report(file_name, original_rows, original_cols, cleaned_df, actions, stats_df, insights, pivot_df):
    """
    Generates a professional PDF report.
    Returns the raw bytes of the PDF file.
    """
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Custom list style
    list_style = ParagraphStyle(
        'ListStyle',
        parent=styles['Normal'],
        leftIndent=20,
        spaceBefore=3,
        spaceAfter=3
    )

    elements = []
    
    # 1. Title
    elements.append(Paragraph("Excel Automation & Data Analytics Report", title_style))
    elements.append(Spacer(1, 12))
    
    # 2. File Overview
    elements.append(Paragraph("Dataset Overview", subtitle_style))
    elements.append(Paragraph(f"<b>File Name:</b> {file_name}", normal_style))
    elements.append(Paragraph(f"<b>Original Size:</b> {original_rows} rows, {original_cols} columns", normal_style))
    elements.append(Paragraph(f"<b>Cleaned Size:</b> {cleaned_df.shape[0]} rows, {cleaned_df.shape[1]} columns", normal_style))
    elements.append(Spacer(1, 12))
    
    # 3. Cleaning Actions
    elements.append(Paragraph("Cleaning Actions Performed", subtitle_style))
    for action in actions:
        elements.append(Paragraph(action, list_style))
    elements.append(Spacer(1, 12))
    
    # 4. Key Insights
    if insights:
        elements.append(Paragraph("Key Insights", subtitle_style))
        for insight in insights:
            elements.append(Paragraph(f"• {insight}", list_style))
        elements.append(Spacer(1, 12))
        
    # 5. Key Statistics (Table)
    if stats_df is not None:
        elements.append(Paragraph("Key Statistics (Numeric Columns)", subtitle_style))
        
        # Prepare data for table
        # Reset index to include column names in the table
        stats_reset = stats_df.reset_index().rename(columns={'index': 'Column'})
        
        # Convert to list of lists, rounding floats for readability
        table_data = [stats_reset.columns.tolist()]
        for index, row in stats_reset.iterrows():
            row_data = []
            for val in row:
                if isinstance(val, float):
                    row_data.append(f"{val:.2f}")
                else:
                    row_data.append(str(val))
            table_data.append(row_data)
            
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))
        
    # 6. Pivot Analysis Summary
    if pivot_df is not None:
        elements.append(Paragraph("Pivot Analysis Summary", subtitle_style))
        
        # Take top 20 rows if it's too large
        pivot_display = pivot_df.head(20)
        
        table_data = [pivot_display.columns.tolist()]
        for index, row in pivot_display.iterrows():
            row_data = []
            for val in row:
                if isinstance(val, float):
                    row_data.append(f"{val:.2f}")
                else:
                    row_data.append(str(val))
            table_data.append(row_data)
            
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.steelblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.aliceblue),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(t)
        if len(pivot_df) > 20:
             elements.append(Paragraph(f"<i>... showing top 20 of {len(pivot_df)} rows</i>", normal_style))
             
    # Build PDF
    doc.build(elements)
    return output.getvalue()
