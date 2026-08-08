import pandas as pd
import numpy as np

def get_key_statistics(df):
    """
    Returns the key statistics for numeric columns.
    """
    numeric_cols = df.select_dtypes(include=[np.number])
    if numeric_cols.empty:
        return None
    
    stats_df = numeric_cols.describe().T
    # Add median
    stats_df['median'] = numeric_cols.median()
    
    # Reorder columns for readability
    cols = ['count', 'mean', 'median', 'min', 'max', 'std']
    stats_df = stats_df[[c for c in cols if c in stats_df.columns]]
    
    # Rename columns for presentation
    stats_df.rename(columns={'count': 'Count', 'mean': 'Mean', 'median': 'Median', 'min': 'Minimum', 'max': 'Maximum', 'std': 'Std Dev'}, inplace=True)
    return stats_df

def generate_pivot_table(df, index_col, values_col, agg_func):
    """
    Generates a pivot table summary.
    """
    try:
        agg_map = {
            'Sum': 'sum',
            'Mean': 'mean',
            'Count': 'count',
            'Minimum': 'min',
            'Maximum': 'max'
        }
        
        pivot_df = df.pivot_table(index=index_col, values=values_col, aggfunc=agg_map[agg_func])
        
        # Rename column to indicate aggregation
        pivot_df.rename(columns={values_col: f"{agg_func} of {values_col}"}, inplace=True)
        return pivot_df.reset_index()
    except Exception as e:
        return None

def generate_insights(df):
    """
    Generates dynamic rule-based insights based on the dataframe.
    """
    insights = []
    
    # Missing values
    total_cells = np.prod(df.shape)
    missing_cells = df.isna().sum().sum()
    if missing_cells > 0 and total_cells > 0:
        missing_pct = (missing_cells / total_cells) * 100
        insights.append(f"The dataset contains {missing_pct:.2f}% missing values overall.")
        
    # Find columns with most missing values
    missing_by_col = df.isna().sum()
    if missing_by_col.max() > 0:
        worst_col = missing_by_col.idxmax()
        worst_col_missing = missing_by_col.max()
        worst_col_pct = (worst_col_missing / df.shape[0]) * 100
        insights.append(f"'{worst_col}' contains the most missing values ({worst_col_pct:.2f}%).")
        
    # Duplicate rows
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        insights.append(f"{duplicate_count} duplicate records were detected in the original format.")
        
    # Numeric column insights
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        # Highest average
        means = df[numeric_cols].mean()
        highest_avg_col = means.idxmax()
        insights.append(f"'{highest_avg_col}' has the highest average value ({means.max():.2f}) among numeric columns.")
        
    # Categorical column insights
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        # Most frequent category in the first categorical column
        first_cat = cat_cols[0]
        if not df[first_cat].mode().empty:
            top_cat = df[first_cat].mode()[0]
            cat_count = (df[first_cat] == top_cat).sum()
            insights.append(f"In '{first_cat}', the most frequent category is '{top_cat}' (appears {cat_count} times).")
            
    # Date insights
    date_cols = df.select_dtypes(include=['datetime']).columns
    if len(date_cols) > 0:
        first_date = date_cols[0]
        min_date = df[first_date].min()
        max_date = df[first_date].max()
        if pd.notnull(min_date) and pd.notnull(max_date):
            insights.append(f"The date range in '{first_date}' spans from {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}.")

    if not insights:
        insights.append("No specific patterns or insights were detected based on the current data types.")
        
    return insights
