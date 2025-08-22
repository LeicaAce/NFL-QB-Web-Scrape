Avery Junius
USC ID: 1491496319
GITHUB: AJUNIUS

Requirements
Python Version: 3.11.9

File Structure
.
├── data                                            # Generated CSV files and figures
├── src                                             # Source code
    ├── config.py                                   # Configuration file for mappings
    ├── get_data.py                                 # Scrapes passing and rushing data
    ├── clean_data.py                               # Cleans and processes scraped data
    ├── export_csv.py                               # Combines and exports clean data
    ├── analyze_data.py                             # Runs statistical tests and generates insights
    ├── visualize_results.py                        # Creates visualizations for analysis
    ├── run_analysis_visualization.py               # Full pipeline: analysis + visuals
    ├── main.py                                     # Entry point for running the project
├── results                                         # Location of report pdf
    ├── DSCI510_FinalProjectReport_AveryJunius.pdf
└── README.md                                       # Project documentation (this file)
└── requirements.txt                                # Dependency files

Major Dependencies:
pandas: For data manipulation and analysis.
matplotlib: For creating static visualizations.
seaborn: For enhanced data visualizations.
requests: For sending HTTP requests to fetch data.
BeautifulSoup: For web scraping HTML data.
time and random: For managing request timing and avoiding rate-limiting.
scipy: For statistical analysis.

Install the dependencies using 1 of the 2 methods:
pip install pandas matplotlib seaborn requests beautifulsoup4 scipy 
OR
pip install -r requirements.txt



File Structure
main.py: Collects and cleans data from Pro Football Reference.
run_analysis_visualization.py: Performs data analysis and generates visualizations.
get_data.py: Collects passing, rushing, and playoff data from Pro Football Reference.
clean_data.py: Cleans and processes the collected data.
analyze_data.py: Performs descriptive statistics, correlation analysis, and hypothesis testing.
visualize_results.py: Generates visualizations for correlation matrices and playoff vs. non-playoff comparisons.
export_csv.py: Manages the creation and export of cleaned data to CSV files.
config.py: Configuration file containing standardized mappings for team names.

How to Run the Project
Step 1: Data Collection and Cleaning
Navigate to the project directory (final-project-AJunius)
Run the main.py program to scrape and clean the data:
python src/main.py

This will:
Collect passing, rushing, and playoff data for the 2013, 2021, and 2022 NFL seasons.
Clean and merge the collected data.
Save the following files:
qb_pass_stats_<year>.csv: Contains passing statistics for each season.
qb_rush_stats_<year>.csv: Contains rushing statistics for each season.
qb_combined_stats_with_playoff_status.csv: Combines passing and rushing statistics with playoff status for all seasons.

Step 2: Data Analysis and Visualization
After running main.py, execute the run_analysis_visualization.py script:
python src/run_analysis_visualization.py

This program will:
Perform descriptive statistics, print them to console and save the results in descriptive_stats.csv.
Conduct correlation analysis and save correlation matrices as heatmaps for each year (e.g., correlation_matrix_2013.png).
Generate boxplots comparing playoff vs. non-playoff quarterbacks for key metrics (e.g., passing_yards_comparison.png, rating_comparison.png).

Step 3: Results
Descriptive statistics are saved in descriptive_stats.csv.
Visualizations are saved as PNG files in the project directory.
Statistical analysis outputs (e.g., t-statistics and p-values) are displayed in the terminal.

Additional Notes
Data Sources: The data is scraped from Pro Football Reference, covering the 2013, 2021, and 2022 NFL seasons.
Scope: Only quarterbacks who played at least 10 games in a season are included in the analysis.
Previously scraped data and visuals are stored in final-project-AJunius\data\
