# Smartphone Market Dashboard (Streamlit)

A Streamlit application for exploratory data analysis (EDA) and comparison of smartphones. It helps analyze pricing, ratings, and key specifications across brands, and lets you compare two phones side by side.

## Streamlit Dashboard
- link: https://shlokbagwe-smartphone-eda-dashboard-app-gcfdb4.streamlit.app/

## Features
- Overview: High-level introduction to the dataset and dashboard.
- Brand Explorer: Filter by brand, price range, RAM, and storage; view metrics and distributions.
- Feature Explorer: Pick any two numeric features to explore correlations and scatter plots.
- Compare Phones: Select two models and compare specifications and categorical features. Includes an optional normalized bar chart so features with different scales are comparable.
- 5G & Connectivity: Planned section for connectivity insights.
- EDA / Raw Data: Inspect the underlying dataset.
- About: Project notes and references.

## Dataset
- File: `smartphones.csv`
- Example columns used by the app:
  - `brand_name`, `model`, `price`, `rating`, `sim_type`, `has_5g`, `has_nfc`, `has_ir_blaster`
  - `ram_capacity`, `storage_capacity`, `processor_core`, `processor_speed`
  - `battery_capacity`, `fast_charging`, `display_size`, `refresh_rate`
  - `no_of_rear_camera`, `no_of_front_camera`, `max_rear_camera_MP`, `max_front_camera_MP`
  - `card_supported`, `os`, `resolution_type`

Ensure the CSV is present in the project root (same folder as `app.py`). Missing columns will disable some UI parts gracefully.

## Project Structure
```
Smartphone_EDA/
├─ app.py                # Streamlit app
├─ smartphones.csv       # Dataset (local file, not versioned publicly if sensitive/large)
├─ .gitignore            # Ignores venv, data outputs, notebooks caches, etc.
└─ README.md             # This file
```

## Quick Start (Windows PowerShell)
```powershell
# 1) (Optional) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install streamlit pandas numpy matplotlib seaborn

# 3) Run the app
streamlit run app.py
```

If you prefer a `requirements.txt`, you can generate one after installing packages:
```powershell
pip freeze > requirements.txt
# then in future
pip install -r requirements.txt
```

## Usage Guide
- Brand Explorer
  - Select a brand and adjust filters for price, RAM, and storage.
  - View metrics (total models, average price, median rating, 5G adoption), price and rating distributions, and a filtered table.
- Feature Explorer
  - Choose two numeric features to see their scatter plot and correlation.
- Compare Phones
  - Pick two models. See a spec table, “other features” table, and a bar chart.
  - Use the “Normalize bars (0–100)” checkbox to compare features on different scales (e.g., battery mAh vs GHz) fairly.

## Notes and Conventions
- Normalization for comparison uses min–max scaling per feature across the dataset to produce 0–100 scores.
- Discrete storage selection uses a select-slider with typical GB values.
- The app checks for required columns and shows clear messages if a column is missing.

## Troubleshooting
- Python not found / venv issues
  - Install Python 3.10+ and ensure “Add Python to PATH” is selected.
  - If `Activate.ps1` is blocked, run PowerShell as your user and set policy:
    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```
- `smartphones.csv` not found
  - Place the CSV in the same directory as `app.py`.
- Packages missing
  - Reinstall dependencies: `pip install streamlit pandas numpy matplotlib seaborn`.
- Streamlit port conflict
  - Use: `streamlit run app.py --server.port 8502`.


## License
No license specified. If you intend to open-source, add a license file (e.g., MIT, Apache-2.0) to clarify reuse.
