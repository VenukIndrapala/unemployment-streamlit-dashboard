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

    def filter_by_ref_area_label(self, ref_area_labels):
        """
        Filter the data by the selected REF_AREA_LABEL(s) and sort by TIME_PERIOD in ascending order.

        Args:
            ref_area_labels (str or list): The REF_AREA_LABEL(s) to filter by.

        Returns:
            pd.DataFrame: Filtered and sorted DataFrame containing only rows for the selected REF_AREA_LABEL(s).
        """
        if self.data is None:
            raise ValueError("Data not loaded.")

        if isinstance(ref_area_labels, str):
            ref_area_labels = [ref_area_labels]

        filtered_data = self.data[self.data['REF_AREA_LABEL'].isin(ref_area_labels)]
        if filtered_data.empty:
            raise ValueError(f"No data found for REF_AREA_LABELs: {ref_area_labels}")

        # Sort by REF_AREA_LABEL and TIME_PERIOD in ascending order
        filtered_data = filtered_data.sort_values(['REF_AREA_LABEL', 'TIME_PERIOD'])

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
        unique_labels = filtered_data['REF_AREA_LABEL'].unique()
        for label in unique_labels:
            data_subset = filtered_data[filtered_data['REF_AREA_LABEL'] == label]
            ax.plot(data_subset['TIME_PERIOD'], data_subset['OBS_VALUE'], marker='o', linestyle='-', label=label)
        ax.set_title('Unemployment Trends')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Observation Value')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
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
        unique_labels = filtered_data['REF_AREA_LABEL'].unique()
        for label in unique_labels:
            data_subset = filtered_data[filtered_data['REF_AREA_LABEL'] == label]
            ax.scatter(data_subset['TIME_PERIOD'], data_subset['OBS_VALUE'], alpha=0.7, label=label)
        ax.set_title('Unemployment Scatter Plot')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Observation Value')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        ax.legend()
        plt.tight_layout()
        return fig

    def plot_area_chart(self, ref_area_label):
        """
        Plot an area chart for the selected REF_AREA_LABEL.

        Args:
            ref_area_label (str): The REF_AREA_LABEL to plot.

        Returns:
            matplotlib.figure.Figure: The figure object for the area chart.
        """
        filtered_data = self.filter_by_ref_area_label(ref_area_label)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(filtered_data['TIME_PERIOD'], filtered_data['OBS_VALUE'], alpha=0.5)
        ax.plot(filtered_data['TIME_PERIOD'], filtered_data['OBS_VALUE'], marker='o', linestyle='-')
        ax.set_title(f'Unemployment Area Chart for {ref_area_label}')
        ax.set_xlabel('Time Period')
        ax.set_ylabel('Observation Value')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        return fig

    def visualize_selected_areas(self, ref_area_labels):
        """
        Visualize the trends and scatter plot for the selected REF_AREA_LABEL(s).

        Args:
            ref_area_labels (str or list): The REF_AREA_LABEL(s) selected by the user.

        Returns:
            tuple: (trends_fig, scatter_fig) - The figure objects for trends and scatter plots.
        """
        filtered_data = self.filter_by_ref_area_label(ref_area_labels)
        trends_fig = self.plot_trends(filtered_data)
        scatter_fig = self.plot_scatter(filtered_data)
        return trends_fig, scatter_fig