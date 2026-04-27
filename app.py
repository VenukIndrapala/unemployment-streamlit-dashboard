from src.preprocess_data import DataPreprocessor
from src.streamlit_App import run_app

# Preprocess the data
data_processor = DataPreprocessor("data/raw/worldbank_unemployment.csv", "data/processed/processed_unemployment.csv")
data_processor.run()

# Run the Streamlit app
if __name__ == "__main__":
    run_app()