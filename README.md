# Streamlit CDR Visualizer

This is a Streamlit-based web application for visualizing Call Detail Records (CDRs) and generating CDRs based on latitude and longitude intervals. The app provides two main functionalities:

1. **Visualize CDR Data**:
   - Users can upload their CDR data in either CSV, XML or Excel format.

2. **Generate CDRs**:
   - Users can input latitude and longitude intervals to specify the location of a cell tower.
   - After inputting valid latitude and longitude values, users can click the "Generate CDR" button to simulate and display CDR data for that cell tower location.

## Input files location

The files to be used in the application are placed in the "utils" folder.

## Output file location

The output CDR JSON file is saved in the "datasets" folder

## Getting Started

Follow these steps to run the Streamlit app:

1. Clone this repository to your local machine.
2. Go to the location where the docker-compose file is and build the container to install the requirements: docker-compose up --build.
3. You can access the application at http://localhost:8501/ in your browser.
