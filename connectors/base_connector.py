from abc import ABC, abstractmethod
import pandas as pd


class BaseConnector(ABC):
    """
    Abstract base class for all business data connectors.
    Every connector must implement these methods.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source."""
        pass

    @abstractmethod
    def get_schema(self) -> dict:
        """Return schema information."""
        pass

    @abstractmethod
    def get_records(self) -> pd.DataFrame:
        """Return records as a pandas DataFrame."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Release any resources."""
        pass