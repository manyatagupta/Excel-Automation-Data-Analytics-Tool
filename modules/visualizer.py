import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def plot_numeric_distribution(df, col):
    """
    Plots a histogram for a numeric column using Plotly.
    """
    fig = px.histogram(df, x=col, title=f"Distribution of {col}", 
                       marginal="box", # Adds a box plot on top
                       template="plotly_dark")
    fig.update_layout(xaxis_title=col, yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

def plot_categorical_distribution(df, col):
    """
    Plots a bar chart for the top categories in a categorical column using Plotly.
    """
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, 'Count']
    
    # Limit to top 15 categories to avoid overcrowding
    if len(counts) > 15:
        counts = counts.head(15)
        title = f"Top 15 Categories in {col}"
    else:
        title = f"Distribution of {col}"
        
    fig = px.bar(counts, x=col, y='Count', title=title, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def plot_time_series(df, date_col, numeric_col):
    """
    Plots a time series line chart using Plotly.
    """
    # Group by date (ignoring time if present) and sum
    temp_df = df.copy()
    temp_df[date_col] = temp_df[date_col].dt.date
    ts_data = temp_df.groupby(date_col)[numeric_col].sum().reset_index()
    
    fig = px.line(ts_data, x=date_col, y=numeric_col, 
                  title=f"Trend of {numeric_col} over Time ({date_col})",
                  template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

def plot_correlation_heatmap(df):
    """
    Plots a correlation heatmap for numeric columns using Plotly.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if len(numeric_df.columns) < 2:
        return
        
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", 
                    title="Correlation Heatmap of Numeric Columns",
                    color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

def plot_top_bottom(df, cat_col, num_col, top_n=10):
    """
    Plots top and bottom N values using Plotly.
    """
    grouped = df.groupby(cat_col)[num_col].sum().reset_index()
    
    # Top N
    top_df = grouped.nlargest(top_n, num_col)
    fig_top = px.bar(top_df, x=cat_col, y=num_col, 
                     title=f"Top {top_n} {cat_col} by {num_col}",
                     template="plotly_white")
    st.plotly_chart(fig_top, use_container_width=True)
    
    # Bottom N
    bottom_df = grouped.nsmallest(top_n, num_col)
    fig_bottom = px.bar(bottom_df, x=cat_col, y=num_col, 
                        title=f"Bottom {top_n} {cat_col} by {num_col}",
                        template="plotly_white")
    st.plotly_chart(fig_bottom, use_container_width=True)

def plot_scatter(df, x_col, y_col, color_col=None):
    """
    Plots a 2D scatter plot using Plotly.
    """
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                     title=f"Scatter Plot of {y_col} vs {x_col}",
                     template="plotly_dark",
                     opacity=0.7)
    st.plotly_chart(fig, use_container_width=True)

def plot_3d_scatter(df, x_col, y_col, z_col, color_col=None):
    """
    Plots a 3D scatter plot using Plotly.
    """
    fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, color=color_col,
                        title=f"3D Scatter Plot of {x_col}, {y_col}, {z_col}",
                        template="plotly_dark",
                        opacity=0.7)
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=40))
    st.plotly_chart(fig, use_container_width=True)

def plot_map(df, location_col, num_col):
    """
    Plots a geographical map (choropleth).
    Assumes location_col contains country names or standard ISO codes.
    """
    # Group by location and sum the numeric values
    grouped = df.groupby(location_col)[num_col].sum().reset_index()
    
    fig = px.choropleth(grouped, locations=location_col, locationmode='country names',
                        color=num_col,
                        title=f"Global Map of {num_col} by {location_col}",
                        template="plotly_dark",
                        color_continuous_scale="Viridis")
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'))
    st.plotly_chart(fig, use_container_width=True)
