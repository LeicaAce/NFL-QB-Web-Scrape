
# 🏈 NFL Quarterback Performance & Playoff Correlation

This project analyzes the relationship between NFL quarterback performance and team success, particularly playoff qualification. It scrapes, cleans, and analyzes public data from Pro Football Reference to uncover which QB metrics best correlate with playoff appearances.

---

## 🔍 Project Overview

This project was developed as part of the final assignment for **DSCI 510 (Principles of Programming for Data Science)** in the USC MS in Applied Data Science program.

Key objectives:
- Scrape NFL quarterback stats and team records from [pro-football-reference.com](https://www.pro-football-reference.com)
- Merge and clean multiple data sources
- Explore statistical correlations between individual QB metrics and team playoff status
- Produce summary outputs and visualizations

---

## 🧠 Skills & Technologies Used

- **Python 3**: Data collection, cleaning, analysis
- **BeautifulSoup4**: Web scraping
- **pandas / NumPy**: Data manipulation
- **matplotlib / seaborn**: Visualization
- **Regex**: HTML parsing
- **Git & GitHub**: Version control

---

## 📂 Project Structure

```
├── data/                   # Raw and cleaned data files
├── results/                # Output analysis CSV and images
├── src/
│   ├── get_data.py         # Web scraping functions
│   ├── run_analysis.py     # Data merging and correlation logic
│   └── visualize_results.py# Visualization generator
├── utils/                  # Helper scripts (e.g., cleaning functions)
└── README.md
```

---

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/LeicaAce/NFL-QB-Web-Scrape.git
   cd NFL-QB-Web-Scrape
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Run data collection:
   ```bash
   python src/get_data.py
   ```

4. Analyze and generate results:
   ```bash
   python src/run_analysis.py
   python src/visualize_results.py
   ```

---

## 📈 Key Insights

- **Touchdown passes** and **yards per attempt** showed the strongest correlation with team playoff status.
- QBs on playoff teams had notably **higher passer ratings** and **lower turnover ratios**.
- The correlation between QB stats and team success supports the premise that efficient quarterback play is a leading indicator of postseason qualification.

---

## 💼 Resume Integration

> *Designed and deployed a Python-based web scraping pipeline to collect and analyze NFL quarterback statistics, identifying performance metrics most correlated with playoff qualification. Demonstrated end-to-end data science workflow including ETL, data cleaning, statistical analysis, and results visualization.*