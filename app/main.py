import streamlit as st
import plotly_express as px
import pandas as pd
from api import cdr_view
import xml.etree.ElementTree as ET
import json


# Function to convert XML to JSON
def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    xml_dict = {}
    for child in root:
        xml_dict[child.tag] = child.text
    return json.dumps(xml_dict)


st.set_page_config(page_title="RITHMS CDR Visualizer", page_icon="📊")
tab1, tab2 = st.tabs(["Vizualize CDR", "Generate CDR"])

with tab1:
    st.title("RITHMS CDR Visualizer")

    st.set_option("deprecation.showfileUploaderEncoding", False)

    st.sidebar.subheader("Visualization Settings")

    uploaded_file = st.sidebar.file_uploader(
        label="Upload your CDR file. It can be in .csv, .xlsx, .xml, or .json format",
        type=["csv", "xlsx", "xml", "json"],
    )

    global df

    try:
        if uploaded_file.type is not None:
            # User uploaded a JSON file
            if uploaded_file.type == "json":
                # User uploaded a JSON file
                df = pd.read_json(uploaded_file)
            else:
                # User uploaded a non-JSON file
                if uploaded_file.type == "xml":
                    # Convert XML to JSON
                    xml_data = uploaded_file.read()
                    json_data = xml_to_json(xml_data)
                    df = pd.read_json(json_data)
                else:
                    # Handle CSV and XLSX files
                    try:
                        df = pd.read_csv(uploaded_file, sep=";")
                    except Exception:
                        df = pd.read_excel(uploaded_file)

            st.write(df)
            numeric_columns = df.select_dtypes(["float", "int"]).columns.tolist()
            categorical_columns = df.select_dtypes(["object"]).columns.tolist()

            # Display JSON data
            st.subheader("JSON Data")
            # for record in df.to_dict(orient="records"):
            #     formatted_data = ", ".join(
            #         [f"{key}: {value}" for key, value in record.items()]
            #     )
            #     st.json(formatted_data, expanded=True)
            st.json(df.to_dict(orient="records"))
    except Exception as e:
        st.write("Please upload a file in the left section of the page.")


with tab2:
    st.title("Please introduce the latitude and longitude of the interest zone.")
    st.subheader(
        "The values must be float numbers. You should give an interval for each of them. Example of a longitude value: 23.1234"
    )
    st.subheader("Longitude")
    longitude1 = st.number_input(
        "Enter left head of the interval", min_value=0.0, step=0.00001, key=1
    )
    longitude2 = st.number_input(
        "Enter right head of the interval", min_value=0.0, step=0.00001, key=2
    )
    st.write("Introduced interval is: ", longitude1, longitude2)
    st.subheader("Latitude")
    latitude1 = st.number_input(
        "Enter left head of the interval", min_value=0.0, step=0.00001, key=3
    )
    latitude2 = st.number_input(
        "Enter right head of the interval", min_value=0.0, step=0.00001, key=4
    )
    st.write("Introduced interval is: ", latitude1, latitude2)
    print(longitude1, longitude2, latitude1, latitude2)
    # cdrs = cdr_view(latitude1, latitude2, longitude1, longitude2)
    # print("Robert", cdrs)
    try:
        cdrs = cdr_view(latitude1, latitude2, longitude1, longitude2)
        print(cdrs)
    except Exception as e:
        print(e)
        st.write("Please introduce the values for the latitude and longitude!")

    if st.button("Generate CDR"):
        st.write(cdrs)
