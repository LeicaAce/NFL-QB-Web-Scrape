from get_data import (
    scrape_qb_pass_stats,
    scrape_qb_rush_stats,
    combine_qb_stats,
)


def main():
    """
    Main function to scrape QB stats for each year and combine them into single csv
    """
    # Define the years to
    years_to_scrape = [2013, 2021, 2022]

    # Scrape QB Passing and Rushing Stats
    for year in years_to_scrape:
        print(f"\nProcessing QB Passing Stats for {year}...")
        pass_df = scrape_qb_pass_stats(year, f"qb_pass_stats_{year}.csv")
        if pass_df is not None:
            print(f"QB Passing Stats {year} (First 5 Rows):")
            print(pass_df.head())

            print(f"\nProcessing QB Rushing Stats for {year}...")
            rush_df = scrape_qb_rush_stats(year, pass_df, f"qb_rush_stats_{year}.csv")
            if rush_df is not None:
                print(f"QB Rushing Stats {year} (First 5 Rows):")
                print(rush_df.head())
            else:
                print(f"Failed to scrape QB Rushing Stats for {year}.")
        else:
            print(f"Failed to scrape QB Passing Stats for {year}.")

    # Combine QB Passing and Rushing Stats and append with Playoff status
    print("\nCombining QB Stats and Exporting...")
    combined_df = combine_qb_stats(
        years_to_scrape, "qb_combined_stats_with_playoff_status.csv"
    )
    if combined_df is not None:
        print("Combined QB Stats (First 5 Rows):")
        print(combined_df.head())
    else:
        print("Failed to combine QB Stats.")


if __name__ == "__main__":
    main()
