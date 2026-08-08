import pandas as pd
import numpy as np

def get_data_quality_summary(df):
    """
    Generates a data quality summary for the dataframe.
    """
    total_rows = df.shape[0]
    total_cols = df.shape[1]
    duplicate_rows = df.duplicated().sum()
    missing_cells = df.isna().sum().sum()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    
    summary = {
        "Metric": ["Rows", "Columns", "Duplicate Rows", "Missing Cells"],
        "Value": [total_rows, total_cols, duplicate_rows, missing_cells]
    }
    
    type_counts = {
        "Numeric Columns": len(numeric_cols),
        "Categorical Columns": len(categorical_cols),
        "Date Columns": len(date_cols)
    }
    
    col_summary = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = df[col].isna().sum()
        missing_pct = (missing / total_rows) * 100 if total_rows > 0 else 0
        unique = df[col].nunique()
        col_summary.append([col, dtype, missing, f"{missing_pct:.2f}%", unique])
        
    col_summary_df = pd.DataFrame(col_summary, columns=["Column", "Data Type", "Missing Values", "Missing %", "Unique Values"])
    
    return pd.DataFrame(summary), col_summary_df, type_counts


def clean_data(df, remove_duplicates=True, num_fill_method='median', cat_fill_method='mode', trim_whitespace=True):
    """
    Cleans the dataset based on specified options.
    Returns the cleaned DataFrame and a list of actions performed.
    """
    cleaned_df = df.copy()
    actions = []
    
    # 1. Remove Duplicates
    if remove_duplicates:
        initial_rows = cleaned_df.shape[0]
        cleaned_df.drop_duplicates(inplace=True)
        final_rows = cleaned_df.shape[0]
        duplicates_removed = initial_rows - final_rows
        if duplicates_removed > 0:
            actions.append(f"✓ Removed {duplicates_removed} exact duplicate rows.")
            
    # 2. Trim Whitespace & Normalize Column Names
    cleaned_df.columns = cleaned_df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
    actions.append("✓ Normalized column names.")

    if trim_whitespace:
        str_cols = cleaned_df.select_dtypes(include=['object']).columns
        trimmed_count = 0
        for col in str_cols:
            # Check if trimming is needed (this is a rough check to save time, apply globally)
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            trimmed_count += 1
        if trimmed_count > 0:
            actions.append(f"✓ Trimmed leading/trailing whitespace from {trimmed_count} string columns.")
            
    # 3. Handle Missing Values
    numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
    cat_cols = cleaned_df.select_dtypes(include=['object', 'category']).columns
    
    # Numeric
    num_missing = cleaned_df[numeric_cols].isna().sum().sum()
    if num_missing > 0 and num_fill_method != 'None':
        for col in numeric_cols:
            if cleaned_df[col].isna().any():
                if num_fill_method == 'mean':
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
                elif num_fill_method == 'median':
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
        actions.append(f"✓ Filled {num_missing} missing numeric values with {num_fill_method}.")
        
    # Categorical
    cat_missing = cleaned_df[cat_cols].isna().sum().sum()
    if cat_missing > 0 and cat_fill_method != 'None':
        for col in cat_cols:
            if cleaned_df[col].isna().any():
                if cat_fill_method == 'mode':
                    mode_val = cleaned_df[col].mode()
                    if not mode_val.empty:
                        cleaned_df[col] = cleaned_df[col].fillna(mode_val[0])
                elif cat_fill_method == 'Unknown':
                    cleaned_df[col] = cleaned_df[col].fillna("Unknown")
        actions.append(f"✓ Filled {cat_missing} missing categorical values with {cat_fill_method}.")

    # 4. Attempt Safe Data Type Conversion
    converted_cols = 0
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            # Try to convert to datetime safely
            try:
                converted_date = pd.to_datetime(cleaned_df[col], errors='ignore')
                # Check if it actually converted
                if pd.api.types.is_datetime64_any_dtype(converted_date):
                     cleaned_df[col] = converted_date
                     converted_cols += 1
                     continue
            except Exception:
                pass
            
            # Try to convert to numeric safely
            try:
                converted_num = pd.to_numeric(cleaned_df[col], errors='ignore')
                if pd.api.types.is_numeric_dtype(converted_num):
                    cleaned_df[col] = converted_num
                    converted_cols += 1
            except Exception:
                pass
                
    if converted_cols > 0:
        actions.append(f"✓ Automatically converted data types for {converted_cols} columns.")

    if not actions:
        actions.append("No cleaning actions were necessary based on the selected options.")
        
    return cleaned_df, actions
