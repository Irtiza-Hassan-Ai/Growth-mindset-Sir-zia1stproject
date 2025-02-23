import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("DataSweeper Sterling Integrator By Irtiza Hassan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[1].lower()  # Corrected: [1] not [-1]

        if file_ext == ".csv":
            try:
                df = pd.read_csv(file)
            except pd.errors.ParserError as e:
                st.error(f"Error reading CSV file {file.name}: {e}")
                continue  # Skip to the next file
        elif file_ext == ".xlsx":
            try:
                df = pd.read_excel(file)
            except Exception as e: # Catching a broader exception for Excel
                st.error(f"Error reading Excel file {file.name}: {e}")
                continue  # Skip to the next file
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue  # Skip to the next file

        # File details
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing numeric values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns  # Corrected: .columns
                    if not numeric_cols.empty: # Check if there are any numeric columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing values have been filled!")
                    else:
                        st.warning("No numeric columns found in the data.")


                st.subheader("Select Columns to Keep")
                all_columns = list(df.columns) # Convert to list to avoid issues with multiselect
                selected_columns = st.multiselect(f"Choose columns for {file.name}", all_columns, default=all_columns)
                df = df[selected_columns]

                # Data visualization
                st.subheader("Data Visualization")
                if st.checkbox(f"Show visualization for {file.name}"):
                    numeric_df = df.select_dtypes(include='number')
                    if not numeric_df.empty: # check if there are numeric columns
                        st.bar_chart(numeric_df.iloc[:, :min(2, len(numeric_df.columns))]) # Limit to max 2 columns or less
                    else:
                        st.warning("No numeric columns for visualization")

                # Conversion Option
                st.subheader("Conversion Option")
                conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

                if st.button(f"Convert {file.name}"):
                    buffer = BytesIO() # Define buffer here, inside the if block

                    if conversion_type == "CSV": # Corrected: == not =
                        df.to_csv(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".csv")
                        mime_type = "text/csv"

                    elif conversion_type == "Excel": # Corrected: elif, not if and spelling
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".xlsx") # Corrected extension
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                    buffer.seek(0)

                    st.download_button(
                        label=f"Download {file.name} as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )

    st.success("All files processed successfully!")  # Moved outside the file loop
