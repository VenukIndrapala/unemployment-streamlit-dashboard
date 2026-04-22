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
selected_regions = st.multiselect("Select Region(s):", regions, default=regions[:1] if len(regions) > 0 else [])

# Visualize the selected regions
if selected_regions:
    st.subheader(f"Visualizations for Selected Regions: {', '.join(selected_regions)}")
    trends_fig, scatter_fig = visualizer.visualize_selected_areas(selected_regions)
    st.pyplot(trends_fig)
    st.pyplot(scatter_fig)
else:
    st.write("Please select at least one region to visualize.")