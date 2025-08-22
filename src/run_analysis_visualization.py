import pandas as pd
from analyze_data import (
    descriptive_statistics,
    correlation_analysis,
    playoff_vs_non_playoff_comparison,
)
from visualize_results import (
    visualize_correlation_matrices,
    visualize_playoff_comparison,
)


def main():
    # Load data
    file_path = "qb_combined_stats_with_playoff_status.csv"
    data = pd.read_csv(file_path)

    # Handle missing and infinite values
    data.fillna({"Passing TD to INT Ratio": 0}, inplace=True)
    data["Passing TD to INT Ratio"] = data["Passing TD to INT Ratio"].replace(
        [float("inf"), -float("inf")], 0
    )

    # Descriptive Statistics
    stats_csv = "descriptive_stats.csv"
    stats = descriptive_statistics(data, csv_filename=stats_csv)
    print("\nDescriptive statistics successfully computed and saved.")

    # Optionally, use `stats` for further analysis if needed
    # Example: print the mean values for all metrics
    print("\nMean statistics by year:")
    print(stats.filter(like="_mean", axis=1))

    # Correlation Analysis
    correlations = correlation_analysis(data)
    visualize_correlation_matrices(correlations)

    # Playoff vs Non-Playoff Comparison
    playoff_results = playoff_vs_non_playoff_comparison(data)
    for metric, (t_stat, p_value) in playoff_results.items():
        print(f"{metric}: t_stat={t_stat:.3f}, p_value={p_value:.3f}")

    # Visualize playoff comparisons
    visualize_playoff_comparison(data)


if __name__ == "__main__":
    main()
