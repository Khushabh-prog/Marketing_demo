# Agentic Campaign Optimization Engine

A Streamlit workshop app that demonstrates how AI agents can autonomously analyze marketing campaign performance, identify underperforming segments, rewrite ad copy, and reallocate budgets.

## Project structure
- `app.py` - Main Streamlit application shell with page routing
- `data/generate_data.py` - Dummy marketing dataset generator with intentional underperformers
- `data/marketing_campaigns.xlsx` - Exported dataset produced when `app.py` runs
- `requirements.txt` - Python dependencies

## Getting started
1. Create and activate a Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Features
- Campaign Dashboard with interactive charts
- Anomaly Detection to flag low CTR/high CPA segments
- Simulated Agentic Creative Optimization
- Budget Reallocation recommendations

## Notes
- The dummy data generator intentionally skews the performance of several segments so the agent has clear optimization opportunities.
- The dataset is exported to `data/marketing_campaigns.xlsx` when the app loads.
