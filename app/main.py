import streamlit as st
import plotly_express as px
import pandas as pd
from api import cdr_view
import xml.etree.ElementTree as ET
import json
import xmltodict
import leafmap.foliumap as leafmap
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import time
import requests


st.set_page_config(page_title="RITHMS CDR Visualizer", page_icon="📊", layout="wide")
tab1, tab2, tab3 = st.tabs(["CSV/XSLX", "XML/JSON", "Generate CDR"])

with tab1:
    st.title("RITHMS CDR Visualizer")

    st.set_option("deprecation.showfileUploaderEncoding", False)

    st.sidebar.subheader("Visualization Settings")

    uploaded_file = st.sidebar.file_uploader(
        label="Upload your CDR file. For this tab, it can be in .csv or .xlsx,  format",
        type=["csv", "xlsx"],
    )

    global df

    try:
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, sep=",")
                st.write(df)
                st.json(df.to_dict(orient="records"))
            except Exception:
                df = pd.read_excel(uploaded_file)
                st.write(df)
                st.json(df.to_dict(orient="records"))

    except Exception as e:
        st.write("Please upload a file in the left section of the page.")


with tab3:
    st.write("Please select the interest zone by drawing a rectangle on the map.")

    if "map_key" not in st.session_state:
        st.session_state.map_key = str(time.time())

    m = folium.Map(
        location=[46.087035, 25.115833],
        zoom_start=6,
        key=st.session_state.map_key,
    )

    ghelaiesti = folium.Marker([46.565577, 26.394196], popup="Ghelaiesti").add_to(m)
    cucuteni = folium.Marker([46.94835, 26.65668], popup="Cucuteni").add_to(m)
    turcoaia = folium.Marker([45.14311, 28.19508], popup="Turcoaia").add_to(m)

    Draw(export=True, draw_options={
        'polyline': False,
        'polygon': False,
        'circle': False,
        'marker': False,
        'circlemarker': False,
        'rectangle': True,
    }).add_to(m)
    output = st_folium(m, width=900, height=600, key=st.session_state.map_key + "b")

    if st.button("Reload Map", key="reload"):
        st.session_state.map_key = str(time.time())
        st.experimental_rerun()

    print(output)
    try:
        longitude1 = output["last_active_drawing"]["geometry"]["coordinates"][0][0][0]
        longitude2 = output["last_active_drawing"]["geometry"]["coordinates"][0][2][0]
        latitude1 = output["last_active_drawing"]["geometry"]["coordinates"][0][0][1]
        latitude2 = output["last_active_drawing"]["geometry"]["coordinates"][0][2][1]
        st.write(
            "The selected coordinates are: ",
            longitude1,
            longitude2,
            latitude1,
            latitude2,
        )

    except Exception as e:
        print(e)

    try:
        cdrs = cdr_view(latitude1, latitude2, longitude1, longitude2)
        print(cdrs)

    except Exception as e:
        print(e)
        st.write("Please select the interest zone!")

    if st.button("Generate CDR"):
        st.write(cdrs)

    def download_cdrs():
        # Convert the dataframe to a JSON object
        json_cdrs = cdrs.to_json(orient="records")

        # Create a file object to write the JSON data to
        file = open("./datasets/cdrs.json", "w")
        cdrs.to_csv("./datasets/synthetic_cdr.csv", index=False)
        # Write the JSON data to the file
        file.write(json_cdrs)

        # Close the file
        file.close()

    st.button("Download CDRs as JSON", key="download_button", on_click=download_cdrs)

    def convert_to_string(data):
        """Recursively convert all values in a dictionary to strings."""
        if isinstance(data, dict):
            return {key: convert_to_string(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [convert_to_string(item) for item in data]
        elif isinstance(data, (int, float)):
             return str(data)
        else:
            return data
    #Use a callback to prevent the rerun
    def send_cdrs_to_platform_callback():
        #Access cdrs from session_state instead from the outer scope of the button
        if "cdrs" in st.session_state:
            try:
                cdrs = st.session_state.cdrs
                json_cdrs = cdrs.to_dict(orient="records")

                # Convert all values to strings
                stringified_cdrs = convert_to_string(json_cdrs)
                
                #Change the endpoint to multiple
                response = requests.post(
                    'http://platform.rithms.test:30070/ingest/json/call-data-record/multiple',
                    headers = {
                    'accept': '*/*',
                    'Content-Type': 'application/json'},
                    #Send all the cdrs
                    json=stringified_cdrs
                )
                if response.status_code == 201:
                    st.session_state.send_cdrs_message = f"CDRs successfully sent to platform! Status code: {response.status_code}"
                    
                else:
                    st.session_state.send_cdrs_message = f"Failed to send CDRs. Status code: {response.status_code}, Response: {response.text}"
            except Exception as e:
                st.session_state.send_cdrs_message = f"Error sending CDRs to platform: {str(e)}"
        else:
            st.session_state.send_cdrs_message = "No CDRs available to send. Please generate CDRs first."

    # Initialize message in session state if it does not exist
    if "send_cdrs_message" not in st.session_state:
        st.session_state.send_cdrs_message = ""
    if "cdrs" not in st.session_state:
        st.session_state.cdrs = None

    # Store the `cdrs` in session state after generation
    try:
      if cdrs is not None:
        st.session_state.cdrs = cdrs
    except:
      pass
    
    st.button("Send CDRs to Platform", key="send_cdr_button", on_click=send_cdrs_to_platform_callback)
    # Display message in the page
    st.write(st.session_state.send_cdrs_message)


with tab2:
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("XML FILE", key=11)
        try:
            xml = file1.read()
            file1_data = json.loads(json.dumps(xmltodict.parse(xml)))
            st.write(file1_data)
        except Exception as e:
            st.error("Please upload an XML file.")
    with col2:
        file2 = st.file_uploader("JSON FILE", key=22)
        try:
            json_file = file2.read()
            json_data = json.loads(json_file)
            st.write(json_data)
        except Exception as e:
            st.error("Please upload a JSON file.")
