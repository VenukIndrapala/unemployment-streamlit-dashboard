from preprocess_data import DataPreprocessor

_data_processor = DataPreprocessor("data/raw/worldbank_unemployment.csv", "data/processed/processed_unemployment.csv")
_data_processor.run()