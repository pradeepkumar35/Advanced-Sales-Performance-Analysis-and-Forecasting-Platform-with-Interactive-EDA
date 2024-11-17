import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS to style the app consistently
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

# Title of the Streamlit app
st.title('Exploratory Data Analysis and Sales Performance')

# Create a card for file upload
st.markdown("""
    <div class="card">
        <h2>Upload Your CSV File</h2>
        <p>Please upload a CSV file for analysis.</p>
    </div>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Function to check for common alternative column names
def get_column_name(df, alternatives):
    for col in alternatives:
        if col in df.columns:
            return col
    return None

if uploaded_file is not None:
    try:
        # Read the CSV file
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
            except Exception as e:
                st.error(f"Error reading the file: {e}")

        # Identify required columns with alternative names
        amount_col = get_column_name(df, ['Amount', 'Sales', 'sale', 'cost'])
        qty_col = get_column_name(df, ['Qty', 'Quantity', 'quantity'])
        cost_col = get_column_name(df, ['Cost', 'Unit Cost', 'Price'])
        date_col = get_column_name(df, ['Date', 'date', 'Order Date'])

        # Inform user if certain columns are missing
        missing_columns = []
        if not amount_col:
            missing_columns.append("Amount")
        if not qty_col:
            missing_columns.append("Qty")
        if not cost_col:
            missing_columns.append("Cost")
        if not date_col:
            missing_columns.append("Date")

        if missing_columns:
            st.warning(f"The dataset is missing the following required columns: {', '.join(missing_columns)}")
        
        # Check if both Qty and Cost are missing
        if not qty_col and not cost_col:
            st.error("Both 'Qty' and 'Cost' columns are missing, which limits profit analysis.")
            add_data = st.file_uploader("Upload an additional CSV file containing Qty and Cost information (optional)", type=["csv"])

            if add_data:
                try:
                    extra_df = pd.read_csv(add_data)
                    # Add missing columns from supplementary data
                    if 'Qty' in extra_df.columns and qty_col is None:
                        df['Qty'] = extra_df['Qty']
                        qty_col = 'Qty'
                    if 'Cost' in extra_df.columns and cost_col is None:
                        df['Cost'] = extra_df['Cost']
                        cost_col = 'Cost'
                    st.success("Supplementary data added successfully!")
                except Exception as e:
                    st.error(f"Failed to load supplementary data: {e}")

            else:
                st.info("Proceeding with limited analysis without 'Qty' and 'Cost'.")
                # You may choose to add further code here to limit the analysis or modify your analytics code accordingly

        # Analysis continues if at least some columns are available
        if amount_col and date_col:
            st.write("### Data Preview")
            st.dataframe(df.head())

            st.title('Sales and Profit Analysis')

            if amount_col and qty_col and cost_col:
                # Calculate total sales
                total_sales = df[amount_col].sum()

                # Calculate total cost
                total_cost = (df[qty_col] * df[cost_col]).sum()

                # Calculate profit
                profit = total_sales - total_cost

                # Calculate profit percentage
                profit_percentage = (profit / total_sales) * 100 if total_sales != 0 else 0

                # Create a new column for profit per order
                df['Profit'] = df[amount_col] - (df[qty_col] * df[cost_col])

                # Convert 'Date' column to datetime format
                df[date_col] = pd.to_datetime(df[date_col])

                # Group by date and sum profits for time-series analysis
                profit_time_series = df.groupby(date_col)['Profit'].sum().reset_index()

                # Line graph for profit analysis over time
                st.subheader('Profit Analysis Over Time')
                profit_fig = px.line(profit_time_series, x=date_col, y='Profit', title='Profit Analysis Over Time', labels={date_col: 'Date', 'Profit': 'Total Profit'})
                st.plotly_chart(profit_fig)

                # Total Sales Over Time
                st.subheader('Total Sales Over Time')
                sales_time_series = df.groupby(date_col)[amount_col].sum().reset_index()
                sales_fig = px.line(sales_time_series, x=date_col, y=amount_col, title='Total Sales Over Time', labels={date_col: 'Date', amount_col: 'Total Sales'})
                st.plotly_chart(sales_fig)

                # Sales by Category
                if 'Category' in df.columns:
                    st.subheader('Sales by Category')
                    sales_by_category = df.groupby('Category')[amount_col].sum().reset_index()
                    category_fig = px.bar(sales_by_category, x='Category', y=amount_col, title='Sales by Category')
                    st.plotly_chart(category_fig)

                # Sales Quantity Distribution
                st.subheader('Distribution of Sales Quantities')
                quantity_fig = px.histogram(df, x=qty_col, title='Distribution of Sales Quantities')
                st.plotly_chart(quantity_fig)

                # Sales Performance by Region
                if 'ship_state' in df.columns:
                    st.subheader('Sales Performance by Region')
                    sales_by_region = df.groupby('ship_state')[amount_col].sum().reset_index()
                    region_fig = px.bar(sales_by_region, x='ship_state', y=amount_col, title='Sales Performance by Region')
                    st.plotly_chart(region_fig)

                # Profit by Category
                if 'Category' in df.columns:
                    st.subheader('Profit by Category')
                    profit_by_category = df.groupby('Category')['Profit'].sum().reset_index()
                    profit_category_fig = px.bar(profit_by_category, x='Category', y='Profit', title='Profit by Category')
                    st.plotly_chart(profit_category_fig)

                # Moving Average for Sales
                st.subheader('Sales Trends with Moving Average')
                sales_time_series['Moving_Avg'] = sales_time_series[amount_col].rolling(window=7).mean()
                moving_avg_fig = px.line(sales_time_series, x=date_col, y=[amount_col, 'Moving_Avg'], title='Sales Trends with Moving Average', labels={date_col: 'Date', 'value': 'Sales'})
                st.plotly_chart(moving_avg_fig)

                # Display results
                st.markdown(
                    """
                    <div class="card" style='width: 80%; margin: 0 auto;'>
                        <h2 style='font-size: 50px;'>Profit/Loss Analysis</h2>
                        <p style='font-size: 40px; font-style: italic;'>Total Sales: <strong>${:,.2f}</strong></p>
                        <p style='font-size: 40px; font-style: italic;'>Total Cost: <strong>${:,.2f}</strong></p>
                        <p style='font-size: 40px; font-style: italic;'>Profit: <strong>${:,.2f}</strong></p>
                        <p style='font-size: 40px; font-style: italic;'>Profit Percentage: <strong>{:.2f}%</strong></p>
                    </div>
                    """.format(total_sales, total_cost, profit, profit_percentage),
                    unsafe_allow_html=True
                )

            else:
                st.warning("Profit analysis is not available due to missing 'Qty' and/or 'Cost'.")

            # Custom Graph Creation Section
            st.title('Custom Graph Creation')

            # Dropdown for selecting two variables for comparison
            st.write("### Select two columns to compare")
            col1 = st.selectbox("Select first column", df.columns)
            col2 = st.selectbox("Select second column", df.columns)

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

    except Exception as e:
        st.error(f"Error reading the file: {e}")
