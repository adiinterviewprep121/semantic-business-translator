import pandas as pd


class SchemaDiscovery:
    """
    Analyses a pandas DataFrame and generates metadata
    describing its schema.
    """

    SAMPLE_SIZE = 5

    CATEGORICAL_KEYWORDS = {
        "stage",
        "status",
        "owner",
        "assigned",
        "region",
        "country",
        "department",
        "category",
        "type",
        "priority",
    }

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def analyze(self) -> dict:
        """
        Analyse every column and return schema metadata.
        """
        schema = {}

        for column in self.dataframe.columns:
            schema[column] = self._analyze_column(column)

        return schema

    def _analyze_column(self, column: str) -> dict:
        """
        Analyse a single column and return its metadata.
        """
        series = self.dataframe[column]

        metadata = {
            "data_type": self._detect_data_type(series),
            "nullable": bool(series.isnull().any()),
            "null_count": int(series.isnull().sum()),
            "unique_count": int(series.nunique()),
        }

        data_type = metadata["data_type"]

        if data_type == "number":
            metadata["minimum"] = float(series.min())
            metadata["maximum"] = float(series.max())

        elif data_type == "date":
            metadata["minimum"] = str(series.min())
            metadata["maximum"] = str(series.max())

        else:
            self._add_text_metadata(column, series, metadata)

        return metadata

    def _detect_data_type(self, series: pd.Series) -> str:
        """
        Convert pandas data types into business-friendly types.
        """
        if pd.api.types.is_numeric_dtype(series):
            return "number"

        elif pd.api.types.is_datetime64_any_dtype(series):
            return "date"

        else:
            return "text"

    def _add_text_metadata(
        self,
        column: str,
        series: pd.Series,
        metadata: dict
    ) -> None:
        """
        Add metadata for text columns.
        """
        values = series.dropna().unique().tolist()

        column_name = column.lower()

        is_categorical = any(
            keyword in column_name
            for keyword in self.CATEGORICAL_KEYWORDS
        )

        if is_categorical:
            metadata["unique_values"] = values
        else:
            metadata["sample_values"] = values[: self.SAMPLE_SIZE]