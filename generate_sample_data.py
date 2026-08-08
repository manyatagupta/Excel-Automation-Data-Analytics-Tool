import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_sample_data(num_rows=550):
    print("Generating sample data...")
    
    # Categories and Regions
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys']
    regions = ['North', 'South', 'East', 'West', 'Central']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor'],
        'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Hat'],
        'Home & Garden': ['Plant', 'Chair', 'Lamp', 'Desk', 'Blender'],
        'Sports': ['Basketball', 'Yoga Mat', 'Dumbbells', 'Tennis Racket', 'Football'],
        'Toys': ['Action Figure', 'Board Game', 'Doll', 'Puzzle', 'Lego Set']
    }
    
    # Base data generation
    data = []
    start_date = datetime(2023, 1, 1)
    
    for _ in range(num_rows):
        cat = random.choice(categories)
        prod = random.choice(products[cat])
        reg = random.choice(regions)
        
        # Generate random date
        random_days = random.randint(0, 365)
        date = start_date + timedelta(days=random_days)
        
        # Numeric values
        quantity = random.randint(1, 20)
        price_per_unit = round(random.uniform(10.0, 500.0), 2)
        sales = round(quantity * price_per_unit, 2)
        
        customer_age = random.randint(18, 70)
        discount = round(random.uniform(0.0, 0.3), 2)
        
        data.append([date, prod, cat, reg, sales, quantity, customer_age, discount])
        
    df = pd.DataFrame(data, columns=['Date', 'Product', 'Category', 'Region', 'Sales', 'Quantity', 'Customer_Age', 'Discount'])
    
    # Introduce messy data intentionally
    
    # 1. Missing values
    missing_indices = np.random.choice(df.index, size=int(num_rows * 0.05), replace=False)
    df.loc[missing_indices, 'Sales'] = np.nan
    
    missing_indices = np.random.choice(df.index, size=int(num_rows * 0.03), replace=False)
    df.loc[missing_indices, 'Customer_Age'] = np.nan
    
    missing_indices = np.random.choice(df.index, size=int(num_rows * 0.02), replace=False)
    df.loc[missing_indices, 'Category'] = np.nan

    # 2. Duplicate rows
    # Take 20 rows and append them again to create exact duplicates
    duplicates = df.sample(n=20, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # 3. Whitespace issues in string columns
    df['Product'] = df['Product'].apply(lambda x: f"  {x} " if random.random() < 0.1 else x)
    df['Region'] = df['Region'].apply(lambda x: f"{x}   " if random.random() < 0.1 else x)
    
    # Ensure directory exists
    os.makedirs('sample_data', exist_ok=True)
    
    # Save to Excel
    file_path = 'sample_data/sample_sales_data.xlsx'
    df.to_excel(file_path, index=False)
    print(f"Sample data generated successfully at: {file_path}")
    print(f"Total rows: {len(df)}, Total columns: {len(df.columns)}")

if __name__ == "__main__":
    generate_sample_data()
