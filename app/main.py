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


st.set_page_config(page_title="RITHMS CDR Visualizer", page_icon="📊")
tab1, tab2, tab3, tab4 = st.tabs(["CSV/XSLX", "XML/JSON", "Generate CDR", "MAP"])

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
                df = pd.read_csv(uploaded_file, sep=";")
                st.write(df)
                st.json(df.to_dict(orient="records"))
            except Exception:
                df = pd.read_excel(uploaded_file)
                st.write(df)
                st.json(df.to_dict(orient="records"))

    except Exception as e:
        st.write("Please upload a file in the left section of the page.")


with tab3:
    ## add the map functionality
    m = leafmap.Map()
    m.to_streamlit(height=400)
    Draw(export=True).add_to(m)

    st.write(
        "Please select the interest zone by drawing a rectangle on the map. After that, select the rectangle to show the coordinates"
    )

    st.write("Please introduce the latitude and longitude of the interest zone.")
    st.write(
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

    try:
        cdrs = cdr_view(latitude1, latitude2, longitude1, longitude2)
        print(cdrs)

    except Exception as e:
        print(e)
        st.write("Please introduce the values for the latitude and longitude!")

    if st.button("Generate CDR"):
        st.write(cdrs)

    def download_cdrs():
        # Convert the dataframe to a JSON object
        json_cdrs = cdrs.to_json(orient="records")

        # Create a file object to write the JSON data to
        file = open("./datasets/cdrs.json", "w")

        # Write the JSON data to the file
        file.write(json_cdrs)

        # Close the file
        file.close()

    st.button("Download CDRs as JSON", key="download_button", on_click=download_cdrs)


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

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        m = folium.Map(location=[46.087035, 25.115833], zoom_start=5, key="map")
        Draw(export=True).add_to(m)
        output = st_folium(m, width=600, height=600)

    with c2:
        st.write(output)
        print(output)
        try:
            print(output["last_active_drawing"])
            print("111111")
            print(output["last_active_drawing"]["geometry"]["coordinates"])
        except Exception as e:
            print(e)
