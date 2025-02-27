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

        json_cdrs = cdrs.to_json(orient="records") 
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



    test = {
            "caller_id": "+40734657481",
            "caller_imei": "123456789012345",
            "callee_id": "+40734653481",
            "callee_imei": "789012345678901",
            "call_start_time": "2023-04-24 06:50:28",
            "call_end_time": "2023-04-24 06:57:28",
            "call_duration": "420",
            "call_type": "outbound",
            "call_result": "busy",
            "cell_id": "1125239",
            "imei": "789012345678901",
            "imsi": "154451698212861",
            "direction": "outgoing",
            "longitude": "28.0556488",
            "latitude": "45.44700623",
            "service_type": "voice",
            "billing_info": "Unknown",
            "jitter": "0.691875126",
            "packet_loss": "0.983313834",
            "latency": "31.07935221"
        }
        
    def send_cdrs_to_platform():
        try:
            json_cdrs = cdrs.to_json(orient="records")
            response = requests.post(
                'http://platform.rithms.test:30070/ingest/json/call-data-record/single',
                headers = {
                'accept': '*/*',
                'Content-Type': 'application/json'},
                json=test
            )
            if response.status_code == 200:
                print(f"CDRs successfully sent to platform! Status code: {response.status_code}")
            else:
                print(f"Failed to send CDRs. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending CDRs to platform: {str(e)}")
    
    st.button("Send CDRs to Platform", key="send_cdr_button", on_click=send_cdrs_to_platform)


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
