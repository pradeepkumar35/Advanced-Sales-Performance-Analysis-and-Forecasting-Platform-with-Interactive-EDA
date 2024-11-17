import streamlit as st
import pandas as pd

# Function to validate the dataset and provide the link to the Tableau dashboard
def visualize_tableau_dashboard(uploaded_file):
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Define required columns based on your dataset's needs
    required_columns = {'Order_ID', 'Date', 'Amount'}  # Adjust based on your needs
    if not required_columns.issubset(df.columns):
        st.error(f"Uploaded dataset does not have the required columns: {', '.join(required_columns)}")
        return

    # Display a success message and show the dataframe (optional)
    st.success("Dataset uploaded successfully!")
    st.write(df.head())  # Display the first few rows for verification

    # Provide a link to open the Tableau dashboard in a new tab
    tableau_url = "https://public.tableau.com/views/Finalproject1tableau/Dashboard2?:language=en-US&:display_count=n&:origin=viz_share_link"
    st.markdown(f"[Click here to view the Tableau dashboard](#{tableau_url})", unsafe_allow_html=True)
    st.markdown(f'<a href="{tableau_url}" target="_blank" style="font-size: 20px; color: #0073e6;">Open Tableau Dashboard in New Tab</a>', unsafe_allow_html=True)

# Streamlit App Layout
st.title("Dynamic Tableau Dashboard Visualization")
st.write("Upload your dataset in CSV format to ensure it contains the required columns:")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    visualize_tableau_dashboard(uploaded_file)
