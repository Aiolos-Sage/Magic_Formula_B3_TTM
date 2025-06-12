# Magic_Formula_B3_TTM

A Streamlit app that applies Joel Greenblatt’s Magic Formula strategy to B3-listed stocks using **TTM (Trailing Twelve Months)** financial data. This tool ranks companies based on Earnings Yield and ROIC to help identify undervalued, high-quality investment opportunities.

## 🚀 Features

- Pulls TTM financials via the Financial Modeling Prep API
- Computes custom weighted scores using:
  ```
  Score = (Earnings Yield × 1.0) + (ROIC × 0.2)
  ```
- Interactive tables, scatter plots, heatmaps, and bar charts
- Bilingual interface: Portuguese 🇧🇷 and English 🇺🇸

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- Financial Modeling Prep API

## 🔐 Secrets Configuration

Create a `.streamlit/secrets.toml` file:

```toml
[secrets]
API_KEY = "your_api_key_here"
```

## 📦 Installation

```bash
git clone https://github.com/yourusername/Magic_Formula_B3_TTM.git
cd Magic_Formula_B3_TTM
pip install -r requirements.txt
streamlit run Magic_Formula_B3_TTM.py
```

## 📡 Deploy

You can deploy this app using [Streamlit Cloud](https://streamlit.io/cloud).

---

**License**: MIT
