# Unemployment Streamlit Dashboard

A data visualization dashboard built with Streamlit that displays unemployment data from the World Bank. The app provides interactive analytics including region-based and year-based analysis with various charts and visualizations.

## Features

- **Region-Based Analytics**
  - Select and analyze unemployment trends for specific regions/countries
  - View key metrics: average, maximum, and minimum unemployment rates
  - Area charts showing trends over time
  - Bar charts for year-by-year comparison
  - Multi-region comparison with trend and scatter plots

- **Year-Based Analytics**
  - Select a specific year to view regional unemployment distribution
  - Pie chart showing region share
  - Top 10 regions by unemployment rate
  - Year range slider for aggregated analysis

## Project Structure

```
unemployment-streamlit-dashboard/
├── app.py                    # Main entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/
│   ├── raw/                  # Raw data files
│   │   └── worldbank_unemployment.csv
│   └── processed/            # Processed data files
│       └── processed_unemployment.csv
├── src/
│   ├── preprocess_data.py   # Data preprocessing module
│   ├── streamlit_app.py     # Streamlit dashboard app
│   └── visualize_data.py    # Data visualization module
├── pages_old/
│   └── year_range_bar_chart.py  # Additional Streamlit page
```

## Data

The dashboard uses unemployment data from the World Bank with the following columns:
- `REF_AREA`: Region/country code
- `TIME_PERIOD`: Year of the data point
- `OBS_VALUE`: Unemployment rate (percentage)
- `REF_AREA_LABEL`: Human-readable region/country name

## Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd unemployment-streamlit-dashboard
```

### 2. Create a Virtual Environment

**Using venv (recommended):**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `streamlit` - Web application framework
- `matplotlib` - Plotting and visualization

## Running the Application

### Option 1: Using Streamlit Directly

```bash
streamlit run src/streamlit_app.py
```

### Option 2: Using Python

```bash
python -m streamlit run src/streamlit_app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

## Data Preprocessing (Optional)

If you need to reprocess the raw data:

```bash
python src/main.py
```

This will:
1. Load the raw data from `data/raw/worldbank_unemployment.csv`
2. Clean and transform the data
3. Save the processed data to `data/processed/processed_unemployment.csv`

## Usage

1. **Select a Tab**: Choose between "Region-Based Analytics" or "Year-Based Analytics"
2. **Region Tab**: Select a region from the dropdown to view its unemployment trends
3. **Year Tab**: Select a year to see regional distribution and top performers
4. **Compare**: Use multi-region comparison to analyze multiple regions together
5. **Year Range**: Use the slider to analyze data across a range of years