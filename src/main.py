import streamlit as st
from preprocess_data import DataPreprocessor
from visualize_data import DataVisualizer

# Preprocess the data
data_processor = DataPreprocessor("data/raw/worldbank_unemployment.csv", "data/processed/processed_unemployment.csv")
data_processor.run()

# Initialize the visualizer with the processed data
visualizer = DataVisualizer("data/processed/processed_unemployment.csv")

# Streamlit UI
st.title("Unemployment Dashboard")

# Get unique regions for selection
regions = visualizer.data['REF_AREA_LABEL'].unique()

# User input for region selection
selected_region = st.selectbox("Select a Region:", regions)

# Visualize the selected region
if selected_region:
    st.subheader(f"Visualizations for {selected_region}")
    trends_fig, scatter_fig = visualizer.visualize_selected_area(selected_region)
    st.pyplot(trends_fig)
    st.pyplot(scatter_fig)