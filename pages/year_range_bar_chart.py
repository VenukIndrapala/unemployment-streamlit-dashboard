import streamlit as st
import pandas as pd
from src.visualize_data import DataVisualizer

# Page configuration
st.set_page_config(page_title="Year Range Bar Chart", page_icon="📊")

st.title("📊 Total Unemployment by Year Range")

# Initialize the visualizer
csv_path = "data/processed/processed_unemployment.csv"
visualizer = DataVisualizer(csv_path)

# Get available years
min_year, max_year = visualizer.get_year_range()

# Get unique countries/regions for selection
all_data = visualizer.data
countries = sorted(all_data['REF_AREA_LABEL'].unique())

# Sidebar for country selection
st.sidebar.header("Filter Options")
selected_countries = st.sidebar.multiselect(
    "Select Countries/Regions",
    options=countries,
    default=countries[:5] if len(countries) >= 5 else countries
)

# Year range slider
st.subheader("Select Year Range")
year_range = st.slider(
    "Choose a range of years",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    step=1
)

start_year, end_year = year_range
st.write(f"Showing data from **{start_year}** to **{end_year}**")

# Filter data by selected countries
if selected_countries:
    filtered_data = visualizer.filter_by_ref_area_label(selected_countries)
    
    # Display the bar chart
    try:
        fig = visualizer.plot_bar_chart_by_year_range(filtered_data, start_year, end_year)
        st.pyplot(fig)
    except ValueError as e:
        st.warning(str(e))
else:
    st.info("Please select at least one country/region from the sidebar.")

# Show data table
st.subheader("📋 Data Table")
if selected_countries:
    year_filtered = filtered_data[
        (filtered_data['TIME_PERIOD'] >= start_year) & 
        (filtered_data['TIME_PERIOD'] <= end_year)
    ]
    aggregated = year_filtered.groupby('REF_AREA_LABEL')['OBS_VALUE'].sum().reset_index()
    aggregated = aggregated.sort_values('OBS_VALUE', ascending=False)
    st.dataframe(aggregated, use_container_width=True)