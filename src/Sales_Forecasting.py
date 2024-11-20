import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from statsmodels.tsa.statespace.sarimax import SARIMAX  # Use SARIMA for seasonality
st.markdown(
    """
    <style>
        .stApp {
             background-color: #1E1E2F;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.title("Sales Forecasting")

    # File upload
    file = st.file_uploader("Upload Sales Data (CSV)", type='csv')

    # Input for number of months to forecast
    num_months = st.number_input("Number of months to forecast:", min_value=1, value=1)

    if file:
        df = pd.read_csv(file, encoding='latin1')  # Adjust encoding as needed

        # Ensure the dataset has the required columns
        if 'Date' not in df.columns or 'Sales' not in df.columns:
            st.error('Dataset must contain "Date" and "Sales" columns')
            return

        # Preprocessing
        # Try parsing dates with different formats
        try:
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce').fillna(
                pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce'))
        except Exception as e:
            st.error(f'Error parsing dates: {e}')
            return

        # Drop rows where Date parsing failed
        df.dropna(subset=['Date'], inplace=True)
        df.set_index('Date', inplace=True)
        df = df.sort_index()

        # Remove duplicates and resample to monthly totals if spanning years
        df = df.groupby(df.index).sum()
        if (df.index[-1] - df.index[0]).days > 365:
            df = df.resample('M').sum()  # Resample to monthly frequency for clarity

        # Preprocessing: Log transform the sales data to stabilize variance
        # Convert 'Sales' to numeric, coercing errors to NaN
        # Remove commas, dollar signs, and other non-numeric characters
        df['Sales'] = df['Sales'].replace({',': '', r'\$': '', ' ': ''}, regex=True)

        # Convert to numeric, handling errors
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

        # Drop rows with invalid or missing Sales values
        df.dropna(subset=['Sales'], inplace=True)

        # Log transform the sales data to stabilize variance
        df['Sales'] = np.log1p(df['Sales'])  # log1p to handle zero values
        if df['Sales'].isnull().any():
            st.error("Sales column contains invalid values even after cleaning. Please check your data.")
            return

        # Updated SARIMA model with adjusted parameters for better seasonal handling
        model = SARIMAX(df['Sales'], order=(2, 1, 2), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)

        # Forecast for specified months
        forecast_log = model_fit.forecast(steps=num_months)
        forecast = np.expm1(forecast_log)  # Inverse transformation to get original scale

        # Create forecast index starting from the last date in the dataset
        forecast_index = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods=num_months, freq='M')

        # Plotting the historical data and forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=np.expm1(df['Sales']), mode='lines', name='Historical Sales',
                                 line=dict(color='blue')))
        fig.add_trace(
            go.Scatter(x=forecast_index, y=forecast, mode='lines', name='Forecasted Sales', line=dict(color='red')))

        # Improve x-axis readability for long timespans
        fig.update_xaxes(
            dtick="M3",  # Show date labels every 3 months
            tickformat="%Y-%m"  # Display format
        )

        # Enable zoom and interactive tools
        fig.update_layout(
            xaxis=dict(rangeslider=dict(visible=True), type="date"),
            title="Sales Over Time",
            xaxis_title="Date",
            yaxis_title="Sales"
        )

        # Display the plot
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()
st.markdown("""
    <style>
    .stAlert {
    background-color: #FFBF00; /* Soft Amber */
    color: #4D2600;            /* Dark Brown Text */
    border: 1px solid #FF6F00; /* Bright Orange Border */
    border-radius: 5px;
}
         div.css-1kiw93k {  /* This targets the container Streamlit uses for markdown content */
            color: #002B5B; /* Dark Navy Blue */
            font-size: 18px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
            padding: 5px;
        }
        .main {
            text-align: center;
            padding: 50px;
            color: white;
            min-height: 100vh; /* Ensure full height of viewport */
        }
        h1, h2 {
            color: #002B5B;
            color: #fff;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
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