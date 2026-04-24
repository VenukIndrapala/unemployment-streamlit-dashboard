import streamlit as st
from visualize_data import DataVisualizer

def run_app():
    # Page configuration
    st.set_page_config(page_title="Unemployment Dashboard", page_icon="📊", layout="wide")
    
    # Initialize the visualizer with the processed data
    visualizer = DataVisualizer("data/processed/processed_unemployment.csv")

    # Header
    st.title("📊 Unemployment Dashboard")
    st.markdown("---")

    # Get unique regions and years
    regions = sorted(visualizer.data['REF_AREA_LABEL'].unique())
    all_years = sorted(visualizer.get_all_years())

    # Create tabs for main sections
    tab1, tab2 = st.tabs(["🌍 Region-Based Analytics", "📅 Year-Based Analytics"])

    # ==================== REGION-BASED ANALYTICS ====================
    with tab1:
        st.header("Region-Based Analysis")
        
        # Region selector
        col1, col2 = st.columns([1, 3])
        with col1:
            selected_region = st.selectbox("Select a Region:", regions, key='region_select')
        
        if selected_region:
            # Filter data for selected region
            region_data = visualizer.filter_by_ref_area_label(selected_region)
            
            # Key metrics
            avg_unemployment = region_data['OBS_VALUE'].mean()
            max_unemployment = region_data['OBS_VALUE'].max()
            min_unemployment = region_data['OBS_VALUE'].min()
            year_range = visualizer.get_year_range(region_data)
            
            st.markdown(f"**{selected_region}** | Years: {int(year_range[0])} - {int(year_range[1])}")
            
            # Metrics row
            m1, m2, m3 = st.columns(3)
            m1.metric("Average Unemployment", f"{avg_unemployment:.2f}%")
            m2.metric("Max Unemployment", f"{max_unemployment:.2f}%")
            m3.metric("Min Unemployment", f"{min_unemployment:.2f}%")
            
            st.markdown("---")
            
            # Charts in columns
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("📈 Trend Over Time")
                area_fig = visualizer.plot_area_chart(selected_region)
                st.pyplot(area_fig)
            
            with c2:
                st.subheader("📊 Bar Chart by Year")
                bar_fig = visualizer.plot_bar_chart_by_year_range(region_data, int(year_range[0]), int(year_range[1]))
                st.pyplot(bar_fig)
            
            # Multi-region comparison
            st.markdown("---")
            st.subheader("🔍 Multi-Region Comparison")
            
            multi_regions = st.multiselect(
                "Select regions to compare:",
                [r for r in regions if r != selected_region],
                default=[],
                key='multi_region'
            )
            
            if multi_regions:
                compare_regions = [selected_region] + multi_regions
                trends_fig, scatter_fig = visualizer.visualize_selected_areas(compare_regions)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.caption("Trend Comparison")
                    st.pyplot(trends_fig)
                with c4:
                    st.caption("Scatter Plot")
                    st.pyplot(scatter_fig)

    # ==================== YEAR-BASED ANALYTICS ====================
    with tab2:
        st.header("Year-Based Analysis")
        
        # Year selector
        col3, col4 = st.columns([1, 3])
        with col3:
            selected_year = st.selectbox("Select a Year:", all_years, key='year_select')
        
        if selected_year:
            st.markdown(f"### Data for Year: **{selected_year}**")
            
            # Pie chart - region share
            c5, c6 = st.columns(2)
            
            with c5:
                st.subheader("🥧 Region Share")
                pie_fig = visualizer.plot_pie_chart_by_year(selected_year)
                st.pyplot(pie_fig)
            
            with c6:
                st.subheader("📊 Top Regions by Unemployment")
                # Get data for selected year
                year_data = visualizer.data[visualizer.data['TIME_PERIOD'] == selected_year]
                year_data = year_data.sort_values('OBS_VALUE', ascending=False).head(10)
                
                # Create a horizontal bar chart
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.barh(year_data['REF_AREA_LABEL'], year_data['OBS_VALUE'], color='steelblue')
                ax.set_xlabel('Unemployment Rate (%)')
                ax.set_title(f'Top 10 Regions - {selected_year}')
                ax.invert_yaxis()
                st.pyplot(fig)
            
            # Year range slider
            st.markdown("---")
            st.subheader("📅 Year Range Analysis")
            
            min_year, max_year = min(all_years), max(all_years)
            year_range = st.slider(
                "Select Year Range:",
                min_value=int(min_year),
                max_value=int(max_year),
                value=(int(min_year), int(max_year)),
                step=1,
                key='year_range_slider'
            )
            
            start_year, end_year = year_range
            if start_year != end_year:
                # Aggregate data for year range
                range_data = visualizer.data[
                    (visualizer.data['TIME_PERIOD'] >= start_year) & 
                    (visualizer.data['TIME_PERIOD'] <= end_year)
                ]
                
                avg_by_region = range_data.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().reset_index()
                avg_by_region = avg_by_region.sort_values('OBS_VALUE', ascending=False).head(15)
                
                c7, c8 = st.columns(2)
                
                with c7:
                    st.caption(f"Average Unemployment ({start_year}-{end_year})")
                    fig2, ax2 = plt.subplots(figsize=(8, 6))
                    ax2.barh(avg_by_region['REF_AREA_LABEL'], avg_by_region['OBS_VALUE'], color='coral')
                    ax2.set_xlabel('Average Unemployment Rate (%)')
                    ax2.set_title(f'Region Rankings ({start_year}-{end_year})')
                    ax2.invert_yaxis()
                    st.pyplot(fig2)
                
                with c8:
                    st.caption("Trend Over Selected Range")
                    # Line chart for top 5 regions
                    top_5_regions = avg_by_region.head(5)['REF_AREA_LABEL'].tolist()
                    trend_data = range_data[range_data['REF_AREA_LABEL'].isin(top_5_regions)]
                    trend_pivot = trend_data.pivot_table(values='OBS_VALUE', index='TIME_PERIOD', columns='REF_AREA_LABEL', aggfunc='mean')
                    
                    fig3, ax3 = plt.subplots(figsize=(8, 6))
                    trend_pivot.plot(ax=ax3, marker='o')
                    ax3.set_xlabel('Year')
                    ax3.set_ylabel('Unemployment Rate (%)')
                    ax3.set_title(f'Top 5 Regions Trend ({start_year}-{end_year})')
                    ax3.legend(loc='best', fontsize=8)
                    st.pyplot(fig3)