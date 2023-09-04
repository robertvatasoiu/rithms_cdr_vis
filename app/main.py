import streamlit as st
import plotly_express as px
import pandas as pd
from api import cdr_view

st.set_page_config(page_title="RITHMS CDR Visualizer", page_icon="📊")
tab1, tab2 = st.tabs(["Vizualize CDR", "Generate CDR"])

with tab1:
    st.title("RITHMS CDR Visualizer")

    st.set_option("deprecation.showfileUploaderEncoding", False)

    st.sidebar.subheader("Visualization Settings")

    uploaded_file = st.sidebar.file_uploader(
        label="Upload your CDR file. It can be in .csv or .xlsx format",
        type=["csv", "xlsx"],
    )

    global df
    if uploaded_file is not None:
        print("hello")
        print(uploaded_file)
        try:
            df = pd.read_csv(uploaded_file, sep=";")
        except Exception as e:
            print(e)
            df = pd.read_excel(uploaded_file)

    global numeric_columns
    try:
        st.write(df)
        numeric_columns = df.select_dtypes(["float", "int"]).columns.tolist()
        categorical_columns = df.select_dtypes(["object"]).columns.tolist()
    except Exception as e:
        print(e)
        st.write("Please upload a file in the left section of the page.")

    chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=["Scatter Plot", "Lineplots", "BoxPlot", "Histogram"],
    )

    if chart_select == "Scatter Plot":
        st.sidebar.subheader("Scatter Plot Settings")
        try:
            x_values = st.sidebar.selectbox("X axis", options=numeric_columns)
            y_values = st.sidebar.selectbox("Y axis", options=numeric_columns)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values)
            # display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)
            # st.write("Please upload a file")

with tab2:
    st.title(
        "Please introduce the latitude and longitude of the cell tower that is selected."
    )
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
    try:
        cdrs = cdr_view(latitude1, latitude2, longitude1, longitude2)
    except Exception as e:
        print(e)
        st.write("Please introduce the values for the latitude and longitude")

    if st.button("Generate CDR"):
        st.write(cdrs)
