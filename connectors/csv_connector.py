import pandas as pd

from connectors.base_connector import BaseConnector


class CSVConnector(BaseConnector):
    """
    Connector for reading business data from CSV files.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None

    def connect(self) -> None:
        """
        Load the CSV into a pandas DataFrame.
        """
        self.data = pd.read_csv(self.file_path)

    def get_schema(self) -> dict:
        """
        Return column names and inferred data types.
        """
        return {
            column: str(dtype)
            for column, dtype in self.data.dtypes.items()
        }

    def get_records(self) -> pd.DataFrame:
        """
        Return the loaded DataFrame.
        """
        return self.data

    def disconnect(self) -> None:
        """
        Release the DataFrame from memory.
        """
        self.data = None