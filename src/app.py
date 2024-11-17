import streamlit as st
import pandas as pd
import plotly.express as px
import missingno as msno

st.title("EDA & Sales/Profit Analysis")

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='latin1')

    # Raw data preview
    st.write("### Raw Data Preview")
    st.dataframe(df.head())  # Show the first few rows of the raw data
    
    # Data types display
    st.write("### Attribute Data Types")
    st.dataframe(df.dtypes)
    
    # Missing values preview
    st.write("### Preview of Missing Values")
    st.dataframe(df.isnull().sum())

    # Track the values filled for each column
    filled_values = {}

    # Handle missing values with logical filling
    df_filled = df.copy()

    # Handle numeric columns (fill with median)
    for col in df.select_dtypes(include='number').columns:
        median_value = df[col].median()
        df_filled[col].fillna(median_value, inplace=True)
        filled_values[col] = median_value

    # Handle categorical columns (fill with mode, except for special cases)
    for col in df.select_dtypes(include='object').columns:
        if col == 'Status':  # 'Status' column should be filled with 'Unknown'
            df_filled[col].fillna('Unknown', inplace=True)
            filled_values[col] = 'Unknown'
        elif col == 'Order ID':  # 'Order ID' should remain missing or filled with 'ORDER_UNKNOWN'
            df_filled[col].fillna('ORDER_UNKNOWN', inplace=True)
            filled_values[col] = 'ORDER_UNKNOWN'
        elif col == 'index':  # 'index' should be filled with unique values
            df_filled[col] = df_filled[col].fillna(pd.Series(range(len(df_filled))))
            filled_values[col] = 'Unique Values'
        elif col in ['Fulfilment', 'ship-city', 'ship-state']:  # These should be filled with 'Unknown'
            df_filled[col].fillna('Unknown', inplace=True)
            filled_values[col] = 'Unknown'
        else:  # For other categorical columns, fill with mode
            mode_value = df[col].mode()[0]  # Get the most frequent value
            df_filled[col].fillna(mode_value, inplace=True)
            filled_values[col] = mode_value

    # Display the missing values after filling
    st.write("### Missing Values After Filling")
    st.dataframe(df_filled.isnull().sum())
    
    # Show what values were filled in place of missing values
    st.write("### Values Filled In Place of Missing Values")
    for col, value in filled_values.items():
        if df.isnull().sum()[col] > 0:  # Show only columns with missing values initially
            st.write(f"For column '{col}', missing values were filled with: {value}")
    
    # Remove duplicates and show before/after
    st.write("### Duplicate Rows Status")
    st.write("Before removing duplicates:", df.duplicated().sum(), "duplicates")
    df_deduped = df.drop_duplicates()
    st.write("After removing duplicates:", df_deduped.duplicated().sum(), "duplicates")

    # Display numeric and categorical data separately
    st.write("### Numeric Data")
    st.dataframe(df.select_dtypes(include='number').head())
    
    st.write("### Categorical Data")
    st.dataframe(df.select_dtypes(include='object').head())

    # Correlation heatmap of nullity
    st.write("### Nullity Correlation Heatmap")
    fig = msno.heatmap(df)
    st.pyplot(fig.figure)  # Plotting missingno heatmap in Streamlit

    # Uniformity check (example: lowercase all strings)
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.lower().str.strip()

    st.write("### Data After Uniformity Check")
    st.dataframe(df.head())

    # Download button for cleaned dataset
    cleaned_data_csv = df_filled.to_csv(index=False)
    st.download_button(
        label="Download Cleaned Dataset",
        data=cleaned_data_csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    # Sales and Profit Analysis
    st.write("### Sales and Profit Analysis")
    
    # Convert 'Date' column to datetime
    df_filled['Date'] = pd.to_datetime(df_filled['Date'], errors='coerce')

    # Check for missing dates after conversion
    if df_filled['Date'].isnull().any():
        st.warning("There are some rows with invalid or missing date values. They will be ignored in the analysis.")
        df_filled = df_filled.dropna(subset=['Date'])  # Drop rows with invalid dates if necessary

    # Check if 'Cost' column is available
    cost_column_available = 'Cost' in df_filled.columns

    # Define columns
    date_col = 'Date'
    amount_col = 'Sales' if 'Sales' in df_filled.columns else 'Amount'  # Check if 'Sales' or 'Amount' exists
    qty_col = 'Qty' if 'Qty' in df_filled.columns else 'Quantity'  # Check if 'Qty' exists

    # Proceed only if 'Sales' or 'Amount' exists
    if amount_col:
        # Total Sales Over Time
        st.subheader('Total Sales Over Time')
        sales_time_series = df_filled.groupby(date_col)[amount_col].sum().reset_index()
        sales_fig = px.line(sales_time_series, x=date_col, y=amount_col, title='Total Sales Over Time', labels={date_col: 'Date', amount_col: 'Total Sales'})
        st.plotly_chart(sales_fig)

        # Sales by Category
        if 'Category' in df_filled.columns:
            st.subheader('Sales by Category')
            sales_by_category = df_filled.groupby('Category')[amount_col].sum().reset_index()
            category_fig = px.bar(sales_by_category, x='Category', y=amount_col, title='Sales by Category')
            st.plotly_chart(category_fig)

        # Sales Quantity Distribution (Only plot if 'Qty' column exists)
        if qty_col and qty_col in df_filled.columns:
            st.subheader('Distribution of Sales Quantities')
            quantity_fig = px.histogram(df_filled, x=qty_col, title='Distribution of Sales Quantities')
            st.plotly_chart(quantity_fig)
        else:
            st.warning("The 'Qty' column is not available in the dataset. Unable to plot the distribution of sales quantities.")

        # Sales Performance by Region (Show top 10 cities if more than 10 unique regions)
            # Sales Performance by Region (Check for both 'ship-state' and 'ship_state')
        if 'ship-state' in df_filled.columns or 'ship_state' in df_filled.columns:
            st.subheader('Sales Performance by Region')
    
        # Check which column exists and use it
            region_col = 'ship-state' if 'ship-state' in df_filled.columns else 'ship_state'
    
        # Group by region and calculate total sales
            sales_by_region = df_filled.groupby(region_col)[amount_col].sum().reset_index()
    
        # Sort and limit to top 10 regions
            sales_by_region = sales_by_region.sort_values(by=amount_col, ascending=False)
            if len(sales_by_region) > 10:
                sales_by_region = sales_by_region.head(10)  # Select top 10 regions
    
            # Plot sales by region
            region_fig = px.bar(sales_by_region, x=region_col, y=amount_col, title='Sales Performance by Region')
            st.plotly_chart(region_fig)


        if cost_column_available:
            # Profit Analysis Over Time
            st.subheader('Profit Analysis Over Time')
            profit_time_series = df_filled.groupby(date_col).apply(lambda x: (x[amount_col] - x['Cost']).sum()).reset_index(name='Profit')
            profit_fig = px.line(profit_time_series, x=date_col, y='Profit', title='Profit Analysis Over Time', labels={date_col: 'Date', 'Profit': 'Total Profit'})
            st.plotly_chart(profit_fig)

            # Profit by Category
            if 'Category' in df_filled.columns:
                st.subheader('Profit by Category')
                profit_by_category = df_filled.groupby('Category').apply(lambda x: (x[amount_col] - x['Cost']).sum()).reset_index(name='Profit')
                profit_category_fig = px.bar(profit_by_category, x='Category', y='Profit', title='Profit by Category')
                st.plotly_chart(profit_category_fig)

            # Moving Average for Sales
            st.subheader('Sales Trends with Moving Average')
            sales_time_series['Moving_Avg'] = sales_time_series[amount_col].rolling(window=7).mean()
            moving_avg_fig = px.line(sales_time_series, x=date_col, y=[amount_col, 'Moving_Avg'], title='Sales Trends with Moving Average', labels={date_col: 'Date', 'value': 'Sales'})
            st.plotly_chart(moving_avg_fig)

    # Display total sales/profit in case of profit data
    total_sales = df_filled[amount_col].sum()
    st.write(f"Total Sales: {total_sales}")
    
    if cost_column_available:
        total_profit = (df_filled[amount_col] - df_filled['Cost']).sum()
        st.write(f"Total Profit: {total_profit}")
