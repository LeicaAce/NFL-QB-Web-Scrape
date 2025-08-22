import pandas as pd
from scipy.stats import ttest_ind
from export_csv import export_to_csv


def descriptive_statistics(data, csv_filename=None):
    """
    Computes and prints descriptive statistics by year, and saves them to a CSV file.

    Args:
        data (pd.DataFrame): The dataset to analyze.
        csv_filename (str): Path to save the descriptive statistics as a CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing descriptive statistics.
    """
    grouped = data.groupby("Year")
    descriptive_stats = grouped.agg(
        {
            "Passing Yards": ["mean", "std", "min", "max"],
            "Passing TDs": ["mean", "std", "min", "max"],
            "Interceptions": ["mean", "std", "min", "max"],
            "Rating": ["mean", "std", "min", "max"],
            "Rushing Yards": ["mean", "std", "min", "max"],
            "Rushing TDs": ["mean", "std", "min", "max"],
            "Total Yards": ["mean", "std", "min", "max"],
            "Total TDs": ["mean", "std", "min", "max"],
            "Passing TD to INT Ratio": ["mean", "std", "min", "max"],
        }
    ).round(2)

    # Flatten multi-level column names
    descriptive_stats.columns = [
        "_".join(col).strip() for col in descriptive_stats.columns.values
    ]

    print("\n--- Descriptive Statistics ---")
    print(descriptive_stats)

    if csv_filename:
        export_to_csv(descriptive_stats, csv_filename)
        print(f"Descriptive statistics saved to {csv_filename}")

    return descriptive_stats


def correlation_analysis(data):
    """
    Generates correlation matrices for each year in the dataset.

    Args:
        data (pd.DataFrame): The dataset to analyze.

    Returns:
        dict: Dictionary of correlation matrices by year.
    """
    correlation_by_year = {}
    for year in data["Year"].unique():
        yearly_data = data[data["Year"] == year].select_dtypes(include=["float", "int"])
        if not yearly_data.empty:
            correlation_by_year[year] = yearly_data.corr()
    return correlation_by_year


def playoff_vs_non_playoff_comparison(data):
    """
    Performs T-tests comparing playoff vs non-playoff teams for key metrics.

    Args:
        data (pd.DataFrame): The dataset to analyze.

    Returns:
        dict: Dictionary of T-test results (metric: (t_stat, p_value)).
    """
    metrics = [
        "Passing Yards",
        "Passing TDs",
        "Interceptions",
        "Rating",
        "Rushing Yards",
        "Rushing TDs",
        "Total Yards",
        "Total TDs",
        "Passing TD to INT Ratio",
        "4QC",
        "GWD",
    ]
    results = {}
    for metric in metrics:
        playoff_data = data[data["Playoff Status"] == "Playoff"][metric]
        non_playoff_data = data[data["Playoff Status"] == "Eliminated"][metric]
        if not playoff_data.empty and not non_playoff_data.empty:
            t_stat, p_value = ttest_ind(
                playoff_data, non_playoff_data, nan_policy="omit"
            )
            results[metric] = (t_stat, p_value)
    return results
