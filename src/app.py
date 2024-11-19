import streamlit as st
import pandas as pd
import plotly.express as px
import missingno as msno

st.title("EDA & Sales/Profit Analysis")

# Function to standardize column names dynamically
def find_column(df, possible_names):
    """
    Identifies a column in the DataFrame that matches any of the possible names.
    Returns the column name if found, otherwise None.
    """
    for name in possible_names:
        if name in df.columns:
            return name
    return None

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

    # Handle missing values
    df_filled = df.copy()

    # Dictionary to track replacement values
    replacement_values = {}

    for col in df.select_dtypes(include='number').columns:
    # Fill missing numeric values with median
        median_value = df[col].median()
        if df[col].isnull().any():  # Only replace if there are missing values
            df_filled[col].fillna(median_value, inplace=True)
            replacement_values[col] = median_value

    for col in df.select_dtypes(include='object').columns:
        # Fill missing categorical values with mode
        mode_value = df[col].mode()[0]
        if df[col].isnull().any():  # Only replace if there are missing values
            df_filled[col].fillna(mode_value, inplace=True)
            replacement_values[col] = mode_value

    # Only display replacement information if something was actually replaced
    if replacement_values:
        st.write("### Missing Values Replaced With:")
        st.write(replacement_values)

    st.write("### Missing Values After Filling")
    st.dataframe(df_filled.isnull().sum())

    # Remove duplicates
    st.write("### Duplicate Rows Status")
    st.write("Before removing duplicates:", df.duplicated().sum(), "duplicates")
    df_filled = df_filled.drop_duplicates()
    st.write("After removing duplicates:", df_filled.duplicated().sum(), "duplicates")

    # Display numeric and categorical data separately
    st.write("### Numeric Data")
    st.dataframe(df_filled.select_dtypes(include='number').head())

    st.write("### Categorical Data")
    st.dataframe(df_filled.select_dtypes(include='object').head())

    # Correlation heatmap of nullity
    st.write("### Nullity Correlation Heatmap")
    fig = msno.heatmap(df)
    st.pyplot(fig.figure)

    # Uniformity check (example: lowercase all strings)
    for col in df_filled.select_dtypes(include='object').columns:
        df_filled[col] = df_filled[col].astype(str).str.lower().str.strip()

    st.write("### Data After Uniformity Check")
    st.dataframe(df_filled.head())

    # Sales and Profit Analysis
    st.write("### Sales and Profit Analysis")

    # Ensure Date column is in datetime format
    if 'Date' in df_filled.columns:
        df_filled['Date'] = pd.to_datetime(df_filled['Date'], errors='coerce')
        df_filled = df_filled.dropna(subset=['Date'])  # Drop rows with invalid/missing dates

    # Check for 'Cost' and 'Profit' attributes
    # Find columns dynamically
    sales_column = find_column(df_filled, ["Amount","Sales", "Total_Sales", "Revenue","Amt","sales","amount"])
    quantity_column = find_column(df_filled, ["Sales Quantity", "Quantity", "Qty","quantity","Holiday_Flag"])
    region_column = find_column(df_filled, ["ship_state", "ship-state", "ship-city", "shopping_mall", "City", "State", "region","Store"])
    category_column = find_column(df_filled, ["category","Category"])
    cost_column_available = 'Cost' in df_filled.columns
    profit_column_available = 'Profit' in df_filled.columns

    # Calculate profit if 'Cost' is available, or use existing 'Profit'
    if cost_column_available and not profit_column_available:
        df_filled['Profit'] = df_filled[sales_column] - df_filled['Cost']
        st.success("Profit column calculated using 'Sales - Cost'.")
    elif profit_column_available:
        st.success("Profit column already available in the dataset.")
    else:
        st.warning("Neither 'Cost' nor 'Profit' column is available. Skipping profit-related analysis.")

    # Proceed with profit-related analysis if 'Profit' is available
    if 'Profit' in df_filled.columns:
        # Profit Analysis Over Time
        st.subheader('Profit Analysis Over Time')
        profit_time_series = df_filled.groupby('Date')['Profit'].sum().reset_index()
        profit_fig = px.line(
            profit_time_series,
            x='Date',
            y='Profit',
            title='Profit Analysis Over Time',
            labels={'Date': 'Date', 'Profit': 'Total Profit'}
        )
        st.plotly_chart(profit_fig)

        # Profit by Category
        if category_column:
            st.subheader('Profit by Category')
            profit_by_category = df_filled.groupby(category_column)['Profit'].sum().reset_index()
            profit_category_fig = px.bar(
                profit_by_category,
                x=category_column,
                y='Profit',
                title='Profit by Category'
            )
            st.plotly_chart(profit_category_fig)

        # Display total profit
        total_profit = df_filled['Profit'].sum()
        # st.write(f"### Total Profit: {total_profit}")
    else:
        st.info("Profit-related graphs and analysis are not available due to missing required columns.")

    # Sales Analysis
    if sales_column:
        df_filled[sales_column] = df_filled[sales_column].replace({',': ''}, regex=True)
        df_filled[sales_column] = pd.to_numeric(df_filled[sales_column], errors='coerce')

        # Drop rows with invalid sales values (NaN after conversion)
        df_filled = df_filled.dropna(subset=[sales_column])

        # Total Sales Over Time
        st.subheader('Total Sales Over Time')
        sales_time_series = df_filled.groupby('Date')[sales_column].sum().reset_index()
        sales_fig = px.line(
            sales_time_series,
            x='Date',
            y=sales_column,
            title='Total Sales Over Time',
            labels={'Date': 'Date', 'Sales': 'Total Sales'}
        )
        st.plotly_chart(sales_fig)

        # Sales by Category
        if category_column:
            st.subheader('Sales by Category')
            sales_by_category = df_filled.groupby(category_column)[sales_column].sum().reset_index()
            category_fig = px.bar(
                sales_by_category,
                x=category_column,
                y=sales_column,
                title='Sales by Category'
            )
            st.plotly_chart(category_fig)

        # Display total sales
        total_sales = df_filled[sales_column].sum()
        # st.write(f"### Total Sales: {total_sales}")
    else:
        st.warning("The 'Sales' column is not available in the dataset.")

    # Distribution of Sales Quantities
    st.subheader("Distribution of Sales Quantities")
    if quantity_column:
        sales_quantity_fig = px.histogram(
            df_filled,
            x=quantity_column,
            title="Distribution of Sales Quantities",
            nbins=20,
            labels={quantity_column: "Sales Quantity"}
        )
        st.plotly_chart(sales_quantity_fig)
    else:
        st.warning("The 'Sales Quantity' column is not available in the dataset.")

    # Sales Performance by Region
    st.subheader("Sales Performance by Region")
    if region_column:
        sales_by_region = df_filled.groupby(region_column)[sales_column].sum().reset_index()
        sales_region_fig = px.bar(
            sales_by_region,
            x=region_column,
            y=sales_column,
            title="Sales Performance by Region",
            labels={region_column: "Region", sales_column: "Total Sales"}
        )
        st.plotly_chart(sales_region_fig)
    else:
        st.warning("No column representing 'Region' was found in the dataset.")

    # Sales Trends with Moving Average
    st.subheader("Sales Trends with Moving Average")
    if 'Date' in df_filled.columns and sales_column:
        df_filled = df_filled.sort_values(by='Date')  # Sort by date
        df_filled['Sales_MA_7'] = df_filled[sales_column].rolling(window=7).mean()  # 7-day moving average
        sales_trend_ma_fig = px.line(
            df_filled,
            x='Date',
            y=[sales_column, 'Sales_MA_7'],
            title="Sales Trends with 7-Day Moving Average",
            labels={'value': 'Sales', 'variable': 'Legend'},
        )
        st.plotly_chart(sales_trend_ma_fig)
    else:
        st.warning("The 'Date' or 'Sales' column is missing or invalid for trend analysis.")

    # Profit/Loss Analysis Card
    if sales_column:
        if cost_column_available:
            # Calculate total cost based on 'Cost' and 'Quantity'
            total_cost = (df_filled[quantity_column] * df_filled['Cost']).sum() if quantity_column else df_filled['Cost'].sum()
            profit = total_sales - total_cost
            profit_percentage = (profit / total_sales) * 100 if total_sales != 0 else 0

            st.markdown(
                f"""
                <div class="card" style='width: 80%; margin: 0 auto;'>
                    <h2 style='font-size: 50px;'>Profit/Loss Analysis</h2>
                    <p style='font-size: 40px; font-style: italic;'>Total Sales: <strong>${total_sales:,.2f}</strong></p>
                    <p style='font-size: 40px; font-style: italic;'>Total Cost: <strong>${total_cost:,.2f}</strong></p>
                    <p style='font-size: 40px; font-style: italic;'>Profit: <strong>${profit:,.2f}</strong></p>
                    <p style='font-size: 40px; font-style: italic;'>Profit Percentage: <strong>{profit_percentage:.2f}%</strong></p>
                </div>
                """, unsafe_allow_html=True
            )
        elif profit_column_available:
            # If 'Profit' column is available
            profit = total_sales - df_filled['Profit'].sum()
            profit_percentage = (profit / total_sales) * 100 if total_sales != 0 else 0

            st.markdown(
                f"""
                <div class="card" style='width: 80%; margin: 0 auto;'>
                    <h2 style='font-size: 50px;'>Profit/Loss Analysis</h2>
                    <p style='font-size: 40px; font-style: italic;'>Total Sales: <strong>${total_sales:,.2f}</strong></p>
                    <p style='font-size: 40px; font-style: italic;'>Profit: <strong>${profit:,.2f}</strong></p>
                    <p style='font-size: 40px; font-style: italic;'>Profit Percentage: <strong>{profit_percentage:.2f}%</strong></p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            # If neither 'Cost' nor 'Profit' is available, just display Total Sales
            st.markdown(
                f"""
                <div class="card" style='width: 80%; margin: 0 auto;background-color: white;'>
                    <h2 style='font-size: 50px;'>Sales Analysis</h2>
                    <p style='font-size: 40px; font-style: italic;'>Total Sales: <strong>${total_sales:,.2f}</strong></p>
                </div>
                """, unsafe_allow_html=True
            )
        # Custom Graph Creation Section
        st.title('Custom Graph Creation')

        # Dropdown for selecting two variables for comparison
        st.write("### Select two columns to compare")
        # Initially, create an empty list for columns
        columns = df.columns.tolist()  # List of columns in the dataframe
    
        col1 = st.selectbox("Select first column", [''] + columns)  # Add empty string option to the top
        col2 = st.selectbox("Select second column", [''] + columns)  # Add empty string option to the top
    
        # If both columns are selected, allow chart type selection
        if col1 and col2:
            # Dropdown for selecting the chart type
            st.write("### Select a chart type")
            chart_type = st.selectbox("Select chart type", ['Bar', 'Line', 'Scatter', 'Histogram'])

            # Generate chart based on selected type
            if chart_type == 'Bar':
                fig = px.bar(df, x=col1, y=col2, title=f'{col1} vs {col2}')
            elif chart_type == 'Line':
                fig = px.line(df, x=col1, y=col2, title=f'{col1} vs {col2}')
            elif chart_type == 'Scatter':
                fig = px.scatter(df, x=col1, y=col2, title=f'{col1} vs {col2}')
            else:
                fig = px.histogram(df, x=col1, title=f'{col1} Distribution')

            st.plotly_chart(fig)
st.markdown("""
    <style>
        .main {
            text-align: center;
            padding: 50px;
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            color: white;
            min-height: 100vh; /* Ensure full height of viewport */
        }
        h1, h2 {
            font-size: 2.5em;
            color: #fff;
        }
        .card {
            width: 45%;
            padding: 30px;
            background: #ffffff;
            color: #333;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            margin: 20px auto; /* Center the card */
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        }
        .card h2 {
            font-size: 24px;
            color: #007bff;
        }
        .card p {
            font-size: 18px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

