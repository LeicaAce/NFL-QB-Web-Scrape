import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import random
from clean_data import clean_text
from clean_data import standardize_team_names
from export_csv import export_to_csv
from config import TEAM_NAME_MAPPING


# function to delay HTTP requests to avoid rate limiting
def request_with_retry(url, headers=None, retries=3, delay=5):
    """
    Handles HTTP requests with retries for rate limiting (429 errors).

    Args:
        url (str): URL to fetch.
        headers (dict): Headers for the HTTP request.
        retries (int): Number of times to retry in case of failure.
        delay (int): Delay between retries in seconds.

    Returns:
        response (requests.Response or None): Response object or None if all retries failed.
    """
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print(
                f"Received 429 Too Many Requests. Attempt {attempt + 1}/{retries}. Retrying after {delay} seconds..."
            )
            time.sleep(delay)
            delay *= 2  # Exponential delay
        else:
            print(f"Failed to retrieve data from {url}: {response.status_code}")
            return None
    return None


def scrape_qb_pass_stats(year, csv_filename=None):
    """
    Scrapes quarterback pass stats from Pro Football Reference for a given year and returns a DataFrame.

    Args:
        year (int): The year for which to scrape QB stats.
        csv_filename (str, optional): File path to export the scraped DataFrame. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing quarterback pass stats.
    """
    pass_stats_url = f"https://www.pro-football-reference.com/years/{year}/passing.htm"
    print(f"Fetching passing stats from: {pass_stats_url}")

    headers = {
        "User-Agent": random.choice(
            [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            ]
        )
    }

    response = request_with_retry(pass_stats_url, headers=headers)
    if not response:
        print(f"Failed to retrieve data from {pass_stats_url} after retries.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="stats_table")

    # Initialize a list to store all player stats
    qb_pass_stats = []

    # Extract Quarterback Pass Stats
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")

        # Check for position "QB" in column 3 and games played >= 10 in column 5
        if (
            len(columns) > 4
            and columns[3].text.strip() == "QB"
            and columns[4].text.strip().isdigit()
            and int(columns[4].text.strip()) >= 10
        ):
            try:
                # Retrieve QB stats, clean data with clean_data.py
                qb_name = clean_text(columns[0].text, str)
                qb_team = clean_text(columns[2].text, str)
                qb_gamesplayed = clean_text(columns[4].text, int)
                qb_passingyards = clean_text(columns[10].text, int)
                qb_passingtds = clean_text(columns[11].text, int)
                qb_interceptions = clean_text(columns[13].text, int)
                qb_rating = clean_text(columns[23].text, float)

                # Skip players with no valid rating
                if pd.isna(qb_rating):
                    continue

                qb_4qc = clean_text(columns[29].text, int)  # 4th Quarter Comebacks
                qb_gwd = clean_text(columns[30].text, int)  # Game-Winning Drives

                # Append qb pass stats to the list
                qb_pass_stats.append(
                    {
                        "Name": qb_name,
                        "Team": qb_team,
                        "Games Played": qb_gamesplayed,
                        "Passing Yards": qb_passingyards,
                        "Passing TDs": qb_passingtds,
                        "Interceptions": qb_interceptions,
                        "Rating": qb_rating,
                        "4QC": qb_4qc,
                        "GWD": qb_gwd,
                        "Year": year,
                    }
                )
            except (ValueError, IndexError) as e:
                print(f"Error processing row: {e}")
                continue

    # Create a DataFrame
    qb_pass_stats_df = pd.DataFrame(qb_pass_stats)

    # Export to CSV if filename is provided
    if csv_filename:
        export_to_csv(qb_pass_stats_df, csv_filename)

    return qb_pass_stats_df


def scrape_qb_rush_stats(year, passing_stats_df, csv_filename=None):
    """
    Scrapes quarterback rushing stats from Pro Football Reference and returns a DataFrame.
    Filters for players in the passing stats DataFrame.

    Args:
        year (int): The year to fetch data for.
        passing_stats_df (pd.DataFrame): DataFrame containing passing stats to filter QBs.
        csv_filename (str, optional): File path to export the DataFrame. Defaults to None.

    Returns:
        pd.DataFrame or None: DataFrame containing quarterback rushing stats or None if no data is found.
    """
    rush_stats_url = f"https://www.pro-football-reference.com/years/{year}/rushing.htm"
    print(f"Fetching rushing stats from: {rush_stats_url}")

    headers = {
        "User-Agent": random.choice(
            [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            ]
        )
    }

    response = request_with_retry(rush_stats_url, headers=headers)
    if not response:
        print(f"Failed to retrieve data from {rush_stats_url} after retries.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="stats_table")

    if not table:
        print(f"No stats table found on {rush_stats_url}.")
        return None

    # Get the list of QB names from the passing stats DataFrame
    qb_names = passing_stats_df["Name"].tolist()

    qb_rush_stats = []

    for row in table.find_all("tr")[1:]:  # Skip header row
        columns = row.find_all("td")
        if len(columns) > 4:
            try:
                qb_name = columns[0].text.strip()
                games_played = columns[4].text.strip()

                # Check if the player is in the passing stats DataFrame
                if (
                    qb_name in qb_names
                    and games_played.isdigit()
                    and int(games_played) >= 5
                ):
                    rushing_yards = int(columns[6].text.strip().replace(",", "") or 0)
                    rushing_tds = int(columns[7].text.strip().replace(",", "") or 0)
                    qb_rush_stats.append(
                        {
                            "Name": qb_name,
                            "Rushing Yards": rushing_yards,
                            "Rushing TDs": rushing_tds,
                            "Year": year,
                        }
                    )
            except IndexError as e:
                print(f"Row parsing error: {e}. Skipping row.")
                continue

    if qb_rush_stats:
        qb_rush_stats_df = pd.DataFrame(qb_rush_stats)
        if csv_filename:
            export_to_csv(qb_rush_stats_df, csv_filename)
        return qb_rush_stats_df

    print(f"No QB rushing stats found for year {year}.")
    return None


def combine_qb_stats(years, csv_filename="qb_combined_stats_with_playoff_status.csv"):
    """
    Combines QB stats for multiple years and appends playoff status.

    Args:
        years (list): List of years to process.
        csv_filename (str): File path to export the final combined DataFrame.

    Returns:
        pd.DataFrame: Combined QB stats with playoff status.
    """
    combined_stats = []

    for year in years:
        print(f"Processing data for year {year}...")
        pass_stats = scrape_qb_pass_stats(year, f"qb_pass_stats_{year}.csv")
        if pass_stats is None:
            print(f"Skipping year {year} due to missing passing stats.")
            continue

        rush_stats = scrape_qb_rush_stats(year, pass_stats, f"qb_rush_stats_{year}.csv")
        if rush_stats is None:
            print(f"Skipping year {year} due to missing rushing stats.")
            continue

        # Merge passing and rushing stats
        year_combined = pd.merge(
            pass_stats, rush_stats, on=["Name", "Year"], how="left"
        )
        year_combined["Rushing Yards"] = year_combined["Rushing Yards"].fillna(0)
        year_combined["Rushing TDs"] = year_combined["Rushing TDs"].fillna(0)

        # Calculate additional stats
        year_combined["Total Yards"] = (
            year_combined["Passing Yards"] + year_combined["Rushing Yards"]
        )
        year_combined["Total TDs"] = (
            year_combined["Passing TDs"] + year_combined["Rushing TDs"]
        )
        year_combined["Passing TD to INT Ratio"] = (
            (year_combined["Passing TDs"] / year_combined["Interceptions"])
            .fillna(0)
            .round(2)
        )

        # Standardize team names before combining data
        year_combined = standardize_team_names(year_combined)

        combined_stats.append(year_combined)

    if not combined_stats:
        print("No data to combine.")
        return None

    # Concatenate all years' stats
    final_combined_df = pd.concat(combined_stats, ignore_index=True)

    # Debugging: Check if "Standardized Team" column is present
    if "Standardized Team" not in final_combined_df.columns:
        print("Error: 'Standardized Team' column not found in combined DataFrame.")
        return None

    # Append playoff status
    final_combined_df = playoff_team_status(final_combined_df, csv_filename, years)

    return final_combined_df


def playoff_team_status(qb_combined_stats_df, csv_filename=None, years=None):
    """
    Appends playoff status to the combined QB stats DataFrame for given years.

    Args:
        qb_combined_stats_df (pd.DataFrame): DataFrame containing QB stats with standardized team names.
        csv_filename (str, optional): File path to export the final DataFrame. Defaults to None.
        years (list, optional): List of years to process. Defaults to None.

    Returns:
        pd.DataFrame: Updated DataFrame with playoff status included.
    """
    if (
        qb_combined_stats_df is None
        or "Standardized Team" not in qb_combined_stats_df.columns
    ):
        raise ValueError(
            "The input DataFrame is missing or does not contain the required 'Standardized Team' column."
        )

    # Dictionary to store playoff status by team name per year
    team_playoff_status = {}

    def process_table(table, year):
        for row in table.find_all("tr")[1:]:  # Skip header row
            header = row.find("th")
            if header:
                team_name = header.text.strip()
                clean_team_name = team_name.rstrip(
                    "*+"
                ).strip()  # Remove playoff markers
                standardized_name = TEAM_NAME_MAPPING.get(
                    clean_team_name, clean_team_name
                )  # Use mapping

                # Debugging print to confirm mapping
                print(
                    f"Processing: Raw: {team_name}, Cleaned: {clean_team_name}, Standardized: {standardized_name}"
                )

                # Map the cleaned and standardized name to playoff status
                if team_name.endswith(("*", "+")):
                    team_playoff_status[standardized_name] = "Playoff"
                else:
                    team_playoff_status[standardized_name] = "Eliminated"

    # Process playoff data for each year
    for year in years:
        print(f"\nProcessing playoff data for year {year}...")
        team_playoff_status = {}  # Reset playoff status dictionary for each year
        team_standings_url = f"https://www.pro-football-reference.com/years/{year}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        response = request_with_retry(team_standings_url, headers=headers)
        if not response:
            print(
                f"Failed to retrieve data for year {year}. Skipping playoff status update for this year."
            )
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        afc_table = soup.find("table", id="AFC")
        nfc_table = soup.find("table", id="NFC")
        if not afc_table or not nfc_table:
            print(f"Could not find standings tables for year {year}. Skipping...")
            continue

        # Process AFC and NFC tables
        process_table(afc_table, year)
        process_table(nfc_table, year)

        # Debugging: Check playoff mapping
        print(f"Year {year} Playoff Mapping: {team_playoff_status}")

        # Map playoff statuses to QB stats DataFrame for this year
        qb_combined_stats_df.loc[
            qb_combined_stats_df["Year"] == year, "Playoff Status"
        ] = qb_combined_stats_df.loc[
            qb_combined_stats_df["Year"] == year, "Standardized Team"
        ].map(
            lambda team: team_playoff_status.get(team, "Unknown")
        )

    # Debugging: Check for unmatched teams
    unmatched_teams = qb_combined_stats_df[
        qb_combined_stats_df["Playoff Status"] == "Unknown"
    ]["Standardized Team"].unique()
    if unmatched_teams.size > 0:
        print("\n--- Debug: Unmatched Teams to Playoff Status ---")
        print(unmatched_teams)

    # Handle unmatched teams (default to "Eliminated")
    qb_combined_stats_df["Playoff Status"] = qb_combined_stats_df[
        "Playoff Status"
    ].replace("Unknown", "Eliminated")

    # Export to CSV
    if csv_filename:
        qb_combined_stats_df.to_csv(csv_filename, index=False)
        print(f"Data exported to {csv_filename}")

    return qb_combined_stats_df
