import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from io import StringIO

# Load API keys from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

# Define the prompt template for generating synthetic data
prompt_template = ChatPromptTemplate.from_template(
    """
    Generate synthetic data for structural deformation in beams under various load conditions.
    The data should include the following fields for each entry:
    - Beam Length (mm)
    - Beam Width (mm)
    - Beam Height (mm)
    - Load (N)
    - Young’s Modulus (MPa)
    - Poisson’s Ratio
    - Maximum Deformation (mm)

    Use a range of values as follows:
    - Beam Length: 500 to 2000 mm
    - Beam Width: 10 to 100 mm
    - Beam Height: 10 to 100 mm
    - Load: 100 to 5000 N
    - Young's Modulus: 200 to 300 GPa
    - Poisson's Ratio: 0.2 to 0.35

    Provide 10 synthetic entries for the dataset in a table format.
    """
)

# Function to generate synthetic data
def generate_synthetic_data():
    prompt = prompt_template.format()  # Format prompt with specific data if needed
    response = llm.invoke(prompt)
    
    try:
        # Access the raw response content
        response_content = response.content
        st.write("Raw response:", response_content)  # Display on Streamlit for debugging

        # Convert raw text to DataFrame
        # Assuming the raw response is formatted as rows of tabular data in plain text
        # You might need to adjust the delimiter based on the format of `response_content`
        # Here, we assume each line represents a row and columns are separated by commas
        data = StringIO(response_content)  # Convert string to a file-like object
        df = pd.read_csv(data, sep=",")  # Adjust `sep` if the delimiter is different

        # Display DataFrame in Streamlit
        st.write("### Generated Synthetic Structural Deformation Data")
        st.dataframe(df)

        # Save DataFrame to CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="structural_deformation_data.csv",
            mime="text/csv"
        )
        
    except json.JSONDecodeError:
        st.error("The response is not in JSON format and could not be parsed as structured data.")
        st.write(response_content)  # Display raw response content

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Streamlit interface
st.title("Structural Deformation Data Generator")
st.write("Generate synthetic structural deformation data under various beam configurations and load conditions.")
if st.button("Generate Data"):
    generate_synthetic_data()
