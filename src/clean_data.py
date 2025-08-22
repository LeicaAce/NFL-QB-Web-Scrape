#
import re
from config import TEAM_NAME_MAPPING


def clean_text(value, data_type=str):
    """
    Cleans and converts a text value to the specified data type.
    Removes annotations (e.g., values in parentheses or brackets) and commas for numbers.

    Args:
        value (str): The string value to clean.
        data_type (type): The type to convert the cleaned value to (e.g., int, float, str).

    Returns:
        Converted value or None if conversion fails.
    """
    value = re.sub(r"\(.*?\)|\[.*?\]", "", value).strip()  # Remove annotations
    if value == "":
        return None
    try:
        return data_type(value.replace(",", ""))  # Remove commas for numbers
    except ValueError:
        return None


def standardize_team_names(df):
    """
    Standardizes team names using the team_name_mapping dictionary.

    Args:
        df (pd.DataFrame): DataFrame containing QB stats.

    Returns:
        pd.DataFrame: DataFrame with standardized team names.
    """
    df["Standardized Team"] = df["Team"].map(TEAM_NAME_MAPPING)

    # Handle unmapped teams explicitly
    unmapped_teams = df[df["Standardized Team"].isna()]["Team"].unique()
    if len(unmapped_teams) > 0:
        print(
            f"Teams missing from mapping (Standardized Team is NaN): {unmapped_teams}"
        )

    # Fill NaN values with "Unknown" or drop rows
    df["Standardized Team"] = df["Standardized Team"].fillna("Unknown")

    return df
