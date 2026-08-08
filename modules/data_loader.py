import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """
    Loads data from an uploaded CSV or Excel file.
    Returns a Pandas DataFrame or None if an error occurs.
    """
    if uploaded_file is None:
        return None
        
    try:
        file_name = uploaded_file.name
        file_ext = file_name.split('.')[-1].lower()
        
        if file_ext == 'csv':
            # Attempt to read CSV robustly
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
            except UnicodeDecodeError:
                # Fallback to a common alternative encoding if UTF-8 fails
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='latin1', on_bad_lines='skip')
        elif file_ext in ['xls', 'xlsx']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file extension: {file_ext}. Please upload a .csv, .xls, or .xlsx file.")
            return None
            
        if df.empty:
            st.warning("The uploaded file is empty.")
            return None
            
        return df
        
    except Exception as e:
        st.error(f"An error occurred while loading the file: {str(e)}")
        return None

def get_file_info(df, file_name):
    """
    Returns basic file information.
    """
    info = {
        "File Name": file_name,
        "Rows": df.shape[0],
        "Columns": df.shape[1]
    }
    return info
