import pandas as pd
import os

class DataPreprocessor:
    def __init__(self, input_path, output_path):
        """
        Initialize the DataPreprocessor with input and output file paths.

        Args:
            input_path (str): Path to the input CSV file.
            output_path (str): Path to save the processed CSV file.
        """
        self.input_path = input_path    
        self.output_path = output_path
        self.data = None

    def load_data(self):
        """
        Load the CSV data into a pandas DataFrame.
        """
        try:
            self.data = pd.read_csv(self.input_path)
            print(f"Data loaded successfully from {self.input_path}. Shape: {self.data.shape}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
        
    def get_unique(self, column_name):
        """
        Get unique values from a specified column in the data.

        Args:
            column_name (str): The name of the column to extract unique values from.

        Returns:
            numpy.ndarray: An array of unique values from the specified column.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        return self.data[column_name].unique()

    def process_data(self):
        """
        Process the loaded data. This includes selecting relevant columns,
        renaming them, handling missing values, and converting data types.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Get columns
        columns = self.data.columns

        # Dropping columns with only one unique value
        for col in columns:
            unique_columns = self.get_unique(col)
            if len(unique_columns) == 1:
                print(f"Column '{col}' has only one unique value: {unique_columns[0]}. It will be dropped.")
                self.data.drop(columns=[col], inplace=True)

        # Check for missing values and remove them
        missing_values = self.data.isnull().sum().sum()
        print(f"Total missing values after column removal: {missing_values}")

        if missing_values > 0:
            print("Removing rows with missing values...")
            self.data.dropna(inplace=True)
            print(f"Rows with missing values removed. New shape: {self.data.shape}")
        else:
            print("No missing values found.")

        print(f"Data processed. Final shape: {self.data.shape}")

    def save_data(self):
        """
        Save the processed data to the output CSV file.
        """
        if self.data is None:
            raise ValueError("Data not processed. Call process_data() first.")

        # Ensure output directory exists
        output_dir = os.path.dirname(self.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.data.to_csv(self.output_path, index=False)
        print(f"Processed data saved to {self.output_path}")

    def run(self):
        """
        Run the full preprocessing pipeline: load, process, and save.
        """
        self.load_data()
        self.process_data()
        self.save_data()