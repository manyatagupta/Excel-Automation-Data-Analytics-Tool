import base64
from io import BytesIO
import streamlit as st
import pandas as pd
from typing import Optional

def get_base64_of_bin_file(bin_file: str) -> str:
    """Returns the base64 string of a binary file."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_download_link(file_content: bytes, filename: str, text: str) -> str:
    """Generates a link to download the given content."""
    b64 = base64.b64encode(file_content).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href

def create_excel_download_link(df: pd.DataFrame, filename: str = "data.xlsx", text: str = "Download Excel") -> bytes:
    """Generates a Streamlit download button for Excel and returns the bytes."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    val = output.getvalue()
    return val

def render_error(msg: str) -> None:
    """Renders a user-friendly error message in Streamlit."""
    st.error(f"Error: {msg}")

def render_warning(msg: str) -> None:
    """Renders a user-friendly warning message in Streamlit."""
    st.warning(msg)
