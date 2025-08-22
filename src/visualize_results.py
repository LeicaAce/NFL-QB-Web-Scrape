import matplotlib.pyplot as plt
import seaborn as sns


def visualize_correlation_matrices(correlation_by_year):
    """
    Visualizes correlation matrices as heatmaps.

    Args:
        correlation_by_year (dict): Dictionary of correlation matrices by year.
    """
    for year, matrix in correlation_by_year.items():
        plt.figure(figsize=(10, 8))
        sns.heatmap(matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title(f"Correlation Matrix for {year}")
        plt.savefig(f"correlation_matrix_{year}.png")
        plt.close()


def visualize_playoff_comparison(data):
    """
    Creates boxplots for metrics comparing playoff vs non-playoff teams.

    Args:
        data (pd.DataFrame): Dataset containing the metrics and playoff status.
    """
    metrics = [
        "Passing Yards",
        "Passing TDs",
        "Total Yards",
        "Total TDs",
        "4QC",
        "GWD",
        "Passing TD to INT Ratio",
        "Rating",
    ]
    for metric in metrics:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x="Playoff Status", y=metric, data=data)
        plt.title(f"{metric} Comparison: Playoff vs Non-Playoff")
        plt.savefig(f"{metric.lower().replace(' ', '_')}_comparison.png")
        plt.close()
