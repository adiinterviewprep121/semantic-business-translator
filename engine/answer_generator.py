import pandas as pd


class AnswerGenerator:
    """
    Executes the structured query returned by the LLM
    on the pandas DataFrame.
    """

    SUPPORTED_OPERATORS = {"="}

    DISPLAY_COLUMNS = [
        "Deal Name",
        "Name",
        "Company",
        "Opportunity Name",
    ]

    def generate_answer(self, dataframe: pd.DataFrame, query: dict) -> str:
        filtered_df = dataframe.copy()

        # Validate query
        if not isinstance(query, dict):
            return "Invalid query received."

        # Apply filters
        for filter_item in query.get("filters", []):
            column = filter_item.get("column")
            operator = filter_item.get("operator")
            value = filter_item.get("value")

            if not column:
                return "Filter column is missing."

            if column not in filtered_df.columns:
                return f"Column '{column}' does not exist."

            if operator not in self.SUPPORTED_OPERATORS:
                return f"Unsupported operator: {operator}"

            if operator == "=":
                filtered_df = filtered_df[
                    filtered_df[column]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == str(value).strip().lower()
                ]

        intent = query.get("intent")
        target_column = query.get("target_column")

        if intent == "count":
            return f"There are {len(filtered_df)} matching records."

        if intent == "list":
            if filtered_df.empty:
                return "No matching records found."

            for column in self.DISPLAY_COLUMNS:
                if column in filtered_df.columns:
                    values = filtered_df[column].astype(str).tolist()
                    return "Matching records: " + ", ".join(values)

            return filtered_df.to_string(index=False)

        if intent in {"sum", "average", "minimum", "maximum"}:

            if not target_column:
                return "No target column was provided."

            if target_column not in filtered_df.columns:
                return f"Column '{target_column}' does not exist."

            series = pd.to_numeric(
                filtered_df[target_column],
                errors="coerce"
            ).dropna()

            if series.empty:
                return f"No numeric values found in '{target_column}'."

            if intent == "sum":
                value = series.sum()
                return f"Total {target_column}: {value:,.2f}"

            if intent == "average":
                value = series.mean()
                return f"Average {target_column}: {value:,.2f}"

            if intent == "minimum":
                value = series.min()
                return f"Minimum {target_column}: {value:,.2f}"

            if intent == "maximum":
                value = series.max()
                return f"Maximum {target_column}: {value:,.2f}"

        return f"Unsupported intent: {intent}"