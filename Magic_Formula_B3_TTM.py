# Final deployment-ready script with debug logging and only "AAPL" as the ticker
final_script_debug = """import pandas as pd
import streamlit as st
import requests
import plotly.express as px

st.set_page_config(page_title="Magic Formula B3 TTM", layout="wide")

# === Language Selector ===
language = st.sidebar.selectbox("🌐 Escolha o idioma / Select language", ["PT-BR", "EN-US"])

# === Configuration ===
API_KEY = st.secrets["API_KEY"]
TICKERS = ["AAPL"]  # Using only AAPL for debug

# === Data Fetcher ===
def get_financial_data(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm?symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url).json()
        if not response:
            st.warning(f"No data for {ticker} — check symbol or API response.")
            return {"Ticker": ticker, "EarningsYield": None, "ROIC": None, "WeightedScore": None}
        metrics = response[0]
        ey = metrics.get("earningsYieldTTM")
        roic = metrics.get("returnOnInvestedCapitalTTM")
        ey_pct = ey * 100 if ey is not None else None
        roic_pct = roic * 100 if roic is not None else None
        score = ey_pct * 1.0 + roic_pct * 0.2 if ey_pct is not None and roic_pct is not None else None
        return {
            "Ticker": ticker,
            "EarningsYield": ey_pct,
            "ROIC": roic_pct,
            "WeightedScore": score
        }
    except Exception as e:
        st.error(f"Error for {ticker}: {e}")
        return {"Ticker": ticker, "EarningsYield": None, "ROIC": None, "WeightedScore": None}

# === UI Content ===
st.title("📈 Magic Formula - B3 Stocks (TTM)")
st.caption("Data provided by Financial Modeling Prep API")
st.markdown(\"\"\"
### 🧠 Magic Formula Logic
Created by Joel Greenblatt, this strategy aims to find companies that are both **cheap and profitable**.

- **Earnings Yield (EY)**: shows how cheap a stock is based on operating earnings.
- **ROIC** (Return on Invested Capital): measures how efficiently a company generates profits from its capital.

📐 **Score = (Earnings Yield × 1.0) + (ROIC × 0.2)**
\"\"\")

# === Data Load and Ranking ===
data = pd.DataFrame([get_financial_data(ticker) for ticker in TICKERS])
data = data.dropna(subset=["WeightedScore"])
data = data.sort_values(by="WeightedScore", ascending=False).reset_index(drop=True)
data["MagicFormulaRank"] = data.index + 1

# === Table Display ===
display = data[["Ticker", "EarningsYield", "ROIC", "WeightedScore", "MagicFormulaRank"]].copy()
display["EarningsYield"] = display["EarningsYield"].apply(lambda x: f"{x:.1f}%" if x is not None else "N/A")
display["ROIC"] = display["ROIC"].apply(lambda x: f"{x:.1f}%" if x is not None else "N/A")
display["WeightedScore"] = display["WeightedScore"].apply(lambda x: f"{x:.1f}" if x is not None else "N/A")
st.dataframe(display, use_container_width=True)

# === Charts ===
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📊 EY vs ROIC Scatterplot")
    fig1 = px.scatter(data, x="EarningsYield", y="ROIC", text="Ticker", title="EY vs ROIC",
                      labels={"EarningsYield": "EY (%)", "ROIC": "ROIC (%)"}, template="plotly_dark")
    fig1.update_traces(textposition="top center")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 🔥 Heatmap by Score (Top 20)")
    heatmap_data = data.head(20).set_index("Ticker")[["EarningsYield", "ROIC", "WeightedScore"]].T
    fig2 = px.imshow(heatmap_data, text_auto=".1f", color_continuous_scale="Blues", aspect="auto")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 🏅 Top 20 Companies - Weighted Score")
fig3 = px.bar(data.head(20), x="Ticker", y="WeightedScore", title="Top 20 by Score",
              labels={"WeightedScore": "Score"}, template="plotly_white")
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)
"""

# Save the updated debug script with only AAPL
file_path = Path("/mnt/data/Magic_Formula_B3_TTM.py")
file_path.write_text(final_script_debug)

str(file_path)
