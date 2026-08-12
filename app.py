import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration before importing modules that use st
st.set_page_config(page_title="Excel Automation & Data Analytics Tool", layout="wide", page_icon="📊")

# Import local modules
from modules.data_loader import load_data, get_file_info
from modules.data_cleaner import get_data_quality_summary, clean_data
from modules.analyzer import get_key_statistics, generate_pivot_table, generate_insights
from modules.visualizer import plot_numeric_distribution, plot_categorical_distribution, plot_time_series, plot_correlation_heatmap, plot_top_bottom, plot_scatter, plot_3d_scatter, plot_map
from modules.report_generator import generate_pdf_report, generate_excel_report
from modules.utils import create_excel_download_link

def main():
    # Inject custom CSS for a premium look
    st.markdown("""
    <style>
    /* Main background and fonts */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #020617);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header styling */
    h1 {
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0px !important;
        animation: textShine 3s linear infinite;
        background-size: 200% auto;
    }

    @keyframes textShine {
        to {
            background-position: 200% center;
        }
    }
    
    /* Metric Cards Glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 10px 40px 0 rgba(56, 189, 248, 0.2);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Dataframe rounding */
    div[data-testid="stDataFrame"] > div {
        border-radius: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border-radius: 0.5rem;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px 0 rgba(139, 92, 246, 0.4);
        color: white;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 0.5rem;
        border-radius: 1rem;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(56, 189, 248, 0.2) !important;
        transform: translateY(-2px);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📊 Excel Automation & Data Analytics")
    st.markdown("### Upload your dataset, clean it automatically, analyze key patterns, visualize insights, and generate reports.")

    # Initialize session state for storing dataframes
    if 'original_df' not in st.session_state:
        st.session_state['original_df'] = None
    if 'cleaned_df' not in st.session_state:
        st.session_state['cleaned_df'] = None
    if 'file_name' not in st.session_state:
        st.session_state['file_name'] = ""
    if 'cleaning_actions' not in st.session_state:
        st.session_state['cleaning_actions'] = []

    # Sidebar Navigation & Settings
    st.sidebar.header("⚙️ Navigation & Settings")
    st.sidebar.divider()
    
    # 1. Upload Dataset
    st.sidebar.subheader("📂 1. Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload .csv, .xls, .xlsx", type=['csv', 'xls', 'xlsx'])
    
    if uploaded_file is not None:
        # Load data only if it's a new file
        if st.session_state['file_name'] != uploaded_file.name:
            df = load_data(uploaded_file)
            if df is not None:
                st.session_state['original_df'] = df.copy()
                st.session_state['cleaned_df'] = df.copy() # Initially cleaned_df is same as original
                st.session_state['file_name'] = uploaded_file.name
                st.session_state['cleaning_actions'] = []
                st.sidebar.success(f"Loaded: {uploaded_file.name}")
                st.toast(f"Successfully loaded {uploaded_file.name}!", icon="🎉")
    else:
        st.session_state['original_df'] = None
        st.session_state['cleaned_df'] = None
        st.session_state['file_name'] = ""
        st.info("Please upload a dataset to begin.")
        return

    # Tabs for main content
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Data Preview & Quality", 
        "Automated Cleaning", 
        "Key Statistics & Insights", 
        "Visualizations", 
        "Pivot Analysis", 
        "Download Reports"
    ])

    df_orig = st.session_state['original_df']
    df_clean = st.session_state['cleaned_df']

    # --- TAB 1: Data Preview & Quality ---
    with tab1:
        st.header("Data Preview")
        st.write(f"**File Name:** {st.session_state['file_name']}")
        
        info = get_file_info(df_orig, st.session_state['file_name'])
        
        col1, col2 = st.columns(2)
        col1.metric("Total Rows", info['Rows'])
        col2.metric("Total Columns", info['Columns'])
        
        st.dataframe(df_orig.head(10), use_container_width=True)
        
        st.header("Data Quality Summary")
        summary_df, col_summary_df, type_counts = get_data_quality_summary(df_orig)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Duplicate Rows", summary_df.loc[summary_df['Metric'] == 'Duplicate Rows', 'Value'].values[0])
        c2.metric("Missing Cells", summary_df.loc[summary_df['Metric'] == 'Missing Cells', 'Value'].values[0])
        c3.metric("Numeric Columns", type_counts['Numeric Columns'])
        c4.metric("Categorical Columns", type_counts['Categorical Columns'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔍 View Detailed Column Statistics"):
            st.dataframe(col_summary_df, use_container_width=True)

    # --- TAB 2: Automated Cleaning ---
    with tab2:
        st.header("Automated Data Cleaning")
        
        st.sidebar.subheader("2. Cleaning Options")
        remove_dup = st.sidebar.checkbox("Remove exact duplicate rows", value=True, help="Removes rows where every column matches exactly.")
        trim_ws = st.sidebar.checkbox("Trim whitespace from text", value=True, help="Removes extra spaces at the beginning and end of text values.")
        num_fill = st.sidebar.selectbox("Fill missing numeric values:", ['median', 'mean', 'None'], help="Method to fill empty cells in number columns.")
        cat_fill = st.sidebar.selectbox("Fill missing categorical values:", ['mode', 'Unknown', 'None'], help="Method to fill empty cells in text/category columns.")
        
        if st.button("Run Automated Cleaning"):
            with st.spinner("Cleaning data..."):
                cleaned, actions = clean_data(df_orig, remove_dup, num_fill, cat_fill, trim_ws)
                st.session_state['cleaned_df'] = cleaned
                st.session_state['cleaning_actions'] = actions
                st.success("Data cleaned successfully!")
                st.toast("Data cleaned successfully! 🧹", icon="✅")
                st.balloons()
                
        if st.session_state['cleaning_actions']:
            st.subheader("Cleaning Summary")
            
            # Before and after comparison
            orig_sum, _, _ = get_data_quality_summary(df_orig)
            clean_sum, _, _ = get_data_quality_summary(st.session_state['cleaned_df'])
            
            st.markdown("##### 📉 Before vs After")
            m1, m2, m3, m4 = st.columns(4)
            
            orig_rows = int(orig_sum.loc[orig_sum['Metric'] == 'Rows', 'Value'].values[0])
            clean_rows = int(clean_sum.loc[clean_sum['Metric'] == 'Rows', 'Value'].values[0])
            m1.metric("Rows", clean_rows, delta=clean_rows - orig_rows, delta_color="normal")
            
            orig_cols = int(orig_sum.loc[orig_sum['Metric'] == 'Columns', 'Value'].values[0])
            clean_cols = int(clean_sum.loc[clean_sum['Metric'] == 'Columns', 'Value'].values[0])
            m2.metric("Columns", clean_cols, delta=clean_cols - orig_cols, delta_color="normal")
            
            orig_dups = int(orig_sum.loc[orig_sum['Metric'] == 'Duplicate Rows', 'Value'].values[0])
            clean_dups = int(clean_sum.loc[clean_sum['Metric'] == 'Duplicate Rows', 'Value'].values[0])
            m3.metric("Duplicate Rows", clean_dups, delta=clean_dups - orig_dups, delta_color="inverse")
            
            orig_miss = int(orig_sum.loc[orig_sum['Metric'] == 'Missing Cells', 'Value'].values[0])
            clean_miss = int(clean_sum.loc[clean_sum['Metric'] == 'Missing Cells', 'Value'].values[0])
            m4.metric("Missing Cells", clean_miss, delta=clean_miss - orig_miss, delta_color="inverse")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🛠️ View Detailed Cleaning Actions Log"):
                for act in st.session_state['cleaning_actions']:
                    st.write(act)
                
            st.subheader("Cleaned Data Preview")
            st.dataframe(st.session_state['cleaned_df'].head(10), use_container_width=True)

    # --- TAB 3: Key Statistics & Insights ---
    with tab3:
        st.header("Key Statistics")
        stats = get_key_statistics(df_clean)
        if stats is not None:
            st.dataframe(stats, use_container_width=True)
        else:
            st.info("No numeric columns found to generate statistics.")
            
        st.header("Automatic Insights")
        insights = generate_insights(df_clean)
        for ins in insights:
            st.write(f"💡 {ins}")

    # --- TAB 4: Visualizations ---
    with tab4:
        st.header("Charts & Visualizations")
        
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = df_clean.select_dtypes(include=['datetime']).columns.tolist()
        
        if not numeric_cols and not cat_cols:
            st.warning("Not enough data to generate visualizations.")
        else:
            viz_type = st.selectbox("Select Visualization Type:", [
                "Numeric Distribution", "Categorical Distribution", "Time Series Analysis",
                "Top/Bottom Analysis", "Correlation Heatmap", "Scatter Plot (2D)",
                "Scatter Plot (3D)", "Geographical Map"
            ])
            
            st.markdown("---")
            
            if viz_type == "Numeric Distribution" and numeric_cols:
                sel_num_col = st.selectbox("Select numeric column:", numeric_cols)
                plot_numeric_distribution(df_clean, sel_num_col)
                
            elif viz_type == "Categorical Distribution" and cat_cols:
                sel_cat_col = st.selectbox("Select categorical column:", cat_cols)
                plot_categorical_distribution(df_clean, sel_cat_col)
                
            elif viz_type == "Time Series Analysis" and date_cols and numeric_cols:
                sel_date_col = st.selectbox("Select date column:", date_cols)
                sel_ts_num_col = st.selectbox("Select numeric column to track:", numeric_cols, key='ts_num')
                plot_time_series(df_clean, sel_date_col, sel_ts_num_col)
                
            elif viz_type == "Top/Bottom Analysis" and cat_cols and numeric_cols:
                sel_tb_cat = st.selectbox("Select category:", cat_cols, key='tb_cat')
                sel_tb_num = st.selectbox("Select metric:", numeric_cols, key='tb_num')
                plot_top_bottom(df_clean, sel_tb_cat, sel_tb_num)
                
            elif viz_type == "Correlation Heatmap" and len(numeric_cols) >= 2:
                plot_correlation_heatmap(df_clean)
                
            elif viz_type == "Scatter Plot (2D)" and len(numeric_cols) >= 2:
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("X-Axis (Numeric):", numeric_cols, index=0)
                with col2:
                    y_col = st.selectbox("Y-Axis (Numeric):", numeric_cols, index=1)
                with col3:
                    color_col = st.selectbox("Color By (Optional Category):", ['None'] + cat_cols)
                plot_scatter(df_clean, x_col, y_col, None if color_col == 'None' else color_col)
                
            elif viz_type == "Scatter Plot (3D)" and len(numeric_cols) >= 3:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    x_col = st.selectbox("X-Axis (Numeric):", numeric_cols, index=0)
                with col2:
                    y_col = st.selectbox("Y-Axis (Numeric):", numeric_cols, index=1)
                with col3:
                    z_col = st.selectbox("Z-Axis (Numeric):", numeric_cols, index=2)
                with col4:
                    color_col = st.selectbox("Color By (Optional):", ['None'] + cat_cols)
                plot_3d_scatter(df_clean, x_col, y_col, z_col, None if color_col == 'None' else color_col)
                
            elif viz_type == "Geographical Map" and cat_cols and numeric_cols:
                st.info("💡 Ensure the location column contains valid Country Names or standard codes for the map to render correctly.")
                col1, col2 = st.columns(2)
                with col1:
                    loc_col = st.selectbox("Location Column (Category):", cat_cols)
                with col2:
                    num_col = st.selectbox("Value Column (Numeric):", numeric_cols)
                plot_map(df_clean, loc_col, num_col)
                
            else:
                st.info(f"The selected visualization '{viz_type}' requires specific column types that are not present in your dataset.")

    # --- TAB 5: Pivot Analysis ---
    with tab5:
        st.header("Pivot-Style Analysis")
        
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if numeric_cols and cat_cols:
            p_cat = st.selectbox("Rows (Category):", cat_cols)
            p_num = st.selectbox("Values (Numeric):", numeric_cols)
            p_agg = st.selectbox("Aggregation:", ["Sum", "Mean", "Count", "Minimum", "Maximum"])
            
            if st.button("Generate Pivot Table"):
                pivot_result = generate_pivot_table(df_clean, p_cat, p_num, p_agg)
                if pivot_result is not None:
                    st.dataframe(pivot_result, use_container_width=True)
                    st.session_state['last_pivot'] = pivot_result
                else:
                    st.error("Could not generate pivot table with the selected options.")
        else:
            st.info("Pivot analysis requires at least one categorical and one numeric column.")

    # --- TAB 6: Download Reports ---
    with tab6:
        st.header("Download Reports")
        
        # Prepare data for reporting
        stats = get_key_statistics(df_clean)
        insights = generate_insights(df_clean)
        pivot_df = st.session_state.get('last_pivot', None)
        quality_summary, _, _ = get_data_quality_summary(df_clean)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Cleaned Dataset (CSV)")
            csv_data = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Cleaned CSV",
                data=csv_data,
                file_name=f"cleaned_{st.session_state['file_name'].split('.')[0]}.csv",
                mime='text/csv',
            )
            
        with col2:
            st.subheader("Excel Report")
            st.write("Contains multiple sheets (Data, Stats, Pivot, Insights)")
            if st.button("Generate Excel Report"):
                with st.spinner("Generating Excel..."):
                    excel_data = generate_excel_report(
                        df_clean, quality_summary, stats, pivot_df, insights
                    )
                    st.success("Excel Report ready!")
                    st.balloons()
                    st.download_button(
                        label="Download Excel Report",
                        data=excel_data,
                        file_name=f"report_{st.session_state['file_name'].split('.')[0]}.xlsx",
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    
        with col3:
            st.subheader("PDF Summary Report")
            st.write("Contains professional summary of the dataset and insights")
            if st.button("Generate PDF Report"):
                with st.spinner("Generating PDF..."):
                    try:
                        pdf_data = generate_pdf_report(
                            st.session_state['file_name'],
                            df_orig.shape[0], df_orig.shape[1],
                            df_clean,
                            st.session_state['cleaning_actions'],
                            stats,
                            insights,
                            pivot_df
                        )
                        st.success("PDF Report ready!")
                        st.balloons()
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_data,
                            file_name=f"report_{st.session_state['file_name'].split('.')[0]}.pdf",
                            mime='application/pdf'
                        )
                    except Exception as e:
                        st.error(f"Could not generate PDF: {str(e)}")

if __name__ == "__main__":
    main()
