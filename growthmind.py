import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "Data Sweeper",layout='wide')

#custom css
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
#title and description
st.title("DataSweeper Sterling Integrator By Irtiza Hassan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization Creating the project for quarter 3!")

#file uploader
uploader_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if upload_files:
    for file in uploaded_files:
        file_ext = os.path.splittext(file.name)[-1].lower()
        
       if file_ext == ".csv":
            df = pd.read_csv(files)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue
        
        #file details
        st.write( "Preview the head of the DataFrame")
        st.dataframe(df.head())
        
        #data cleaning options
        st.subheader("Data cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the files : {file.name}"):
                    df.drop_duplicate(inplace=True)
                    st.write("Duplicate removed!") 
            
            with col2:
                if st.button(f"Remove duplicates from the files : {file.name}"):
                    numeric_cols = df.select_dtypes(includes=['number']).colums
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")     
                    
                    st.subheader("Select Columns to keep")
                    columns = st.multiselect(f"Choose columns for {file.name}",df.columns, default=df.columns)
                    df = df[columns]
                    
                    #data visualization
                    st.subheader("data visualization")
                    if st.checkbox(f"Show visualization for {file.name}"):
                        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
                        
                    #Conversion Option
                    
                    st.subheader("Conversion Option")
                    conversion_type = st.radio(f"Convert {file.name}to:", ["CSV", "Excel"], key=file.name)
                    if st.button(f"convert{file.name}"):
                        df.to.csv(buffer, index=false)
                        file_name = file.name.replace(file_ext, ".csv")
                        mime_type = "text/csv"
                        
                    elif concersion_type == "excel":
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".xlse")
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)
                    
                    st.download_button(
                        label=f"Download{file.name}as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )              
st.success("All files processed successfully!")
