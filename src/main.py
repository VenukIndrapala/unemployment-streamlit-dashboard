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

# Area Chart Section
st.subheader("Area Chart for a Single Region")
selected_region_for_area = st.selectbox("Select a Region for Area Chart:", regions)
if selected_region_for_area:
    area_fig = visualizer.plot_area_chart(selected_region_for_area)
    st.pyplot(area_fig)
else:
    st.write("Please select a region to display the area chart.")

# Year Range Bar Chart Section
st.subheader("Bar Chart by Year Range for Single Region")
selected_region_for_bar = st.selectbox("Select a Region for Bar Chart:", regions, key='bar_region')

if selected_region_for_bar:
    filtered_data = visualizer.filter_by_ref_area_label(selected_region_for_bar)
    min_year, max_year = visualizer.get_year_range(filtered_data)
    
    if min_year == max_year:
        st.warning(f"Only data available for {selected_region_for_bar} is in year {min_year}")
        bar_fig = visualizer.plot_bar_chart_by_year_range(filtered_data, min_year, max_year)
        st.pyplot(bar_fig)
    else:
        year_range = st.slider(
            "Select Year Range",
            min_value=int(min_year),
            max_value=int(max_year),
            value=(int(min_year), int(max_year)),
            step=1,
            key='bar_year_range'
        )
        start_year, end_year = year_range
        st.write(f"Showing data from **{start_year}** to **{end_year}**")
        
        bar_fig = visualizer.plot_bar_chart_by_year_range(filtered_data, start_year, end_year)
        st.pyplot(bar_fig)