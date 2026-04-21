import pandas as pd
import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, csv_path):
        """
        Initialize the DataVisualizer with the path to the CSV file.

        Args:
            csv_path (str): Path to the CSV file containing the data.
        """
        self.csv_path = csv_path
        self.data = None
        self.load_data()

    def load_data(self):
        """
        Load the CSV data into a pandas DataFrame.
        """
        try:
            self.data = pd.read_csv(self.csv_path)
            print(f"Data loaded successfully from {self.csv_path}. Shape: {self.data.shape}")
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def filter_by_ref_area_label(self, ref_area_label):
        """
        Filter the data by the selected REF_AREA_LABEL and sort by TIME_PERIOD in ascending order.

        Args:
            ref_area_label (str): The REF_AREA_LABEL to filter by.

        Returns:
            pd.DataFrame: Filtered and sorted DataFrame containing only rows for the selected REF_AREA_LABEL.
        """
        if self.data is None:
            raise ValueError("Data not loaded.")

        filtered_data = self.data[self.data['REF_AREA_LABEL'] == ref_area_label]
        if filtered_data.empty:
            raise ValueError(f"No data found for REF_AREA_LABEL: {ref_area_label}")

        # Sort by TIME_PERIOD in ascending order
        filtered_data = filtered_data.sort_values('TIME_PERIOD')

        return filtered_data

    def plot_trends(self, filtered_data):
        """
        Plot the trends of OBS_VALUE over TIME_PERIOD for the filtered data.

        Args:
            filtered_data (pd.DataFrame): The filtered DataFrame to plot.

        Returns:
            matplotlib.figure.Figure: The figure object for the plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(filtered_data['TIME_PERIOD'], filtered_data['OBS_VALUE'], marker='o', linestyle='-')
        ax.set_title(f'Unemployment Trends for {filtered_data["REF_AREA_LABEL"].iloc[0]}')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Observation Value')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        return fig

    def plot_scatter(self, filtered_data):
        """
        Plot a scatter plot of OBS_VALUE vs TIME_PERIOD for the filtered data.

        Args:
            filtered_data (pd.DataFrame): The filtered DataFrame to plot.

        Returns:
            matplotlib.figure.Figure: The figure object for the plot.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(filtered_data['TIME_PERIOD'], filtered_data['OBS_VALUE'], alpha=0.7)
        ax.set_title(f'Unemployment Scatter Plot for {filtered_data["REF_AREA_LABEL"].iloc[0]}')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Observation Value')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        return fig

    def visualize_selected_area(self, ref_area_label):
        """
        Visualize the trends and scatter plot for the selected REF_AREA_LABEL.

        Args:
            ref_area_label (str): The REF_AREA_LABEL selected by the user.

        Returns:
            tuple: (trends_fig, scatter_fig) - The figure objects for trends and scatter plots.
        """
        filtered_data = self.filter_by_ref_area_label(ref_area_label)
        trends_fig = self.plot_trends(filtered_data)
        scatter_fig = self.plot_scatter(filtered_data)
        return trends_fig, scatter_fig