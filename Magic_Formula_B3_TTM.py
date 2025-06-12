# Save the final deployment-ready script without file-writing operations
final_script = """import pandas as pd
import streamlit as st
import requests
import plotly.express as px

st.set_page_config(page_title="Magic Formula B3 TTM", layout="wide")

# === Language Selector ===
language = st.sidebar.selectbox("🌐 Escolha o idioma / Select language", ["PT-BR", "EN-US"])

# === Configuration ===
API_KEY = st.secrets["API_KEY"]
TICKERS = [
    "LEVE3.SA", "CMIN3.SA", "AURE3.SA", "VULC3.SA", "PETR4.SA", "BRAP3.SA", "CSMG3.SA",
    "CMIG4.SA", "CMIG3.SA", "VALE3.SA", "BBDC3.SA", "GOAU4.SA", "RECV3.SA", "TAEE11.SA",
    "BBAS3.SA", "ISAE4.SA", "CPFE3.SA", "ROMI3.SA", "RANI3.SA", "BBSE3.SA", "KEPL3.SA",
    "ITUB3.SA", "VBBR3.SA", "ABCB4.SA", "CURY3.SA", "LAVV3.SA", "JHSF3.SA", "UNIP6.SA",
    "AGRO3.SA", "EGIE3.SA", "SANB4.SA", "ALOS3.SA", "CXSE3.SA", "ITSA4.SA", "GRND3.SA",
    "POMO4.SA", "ABEV3.SA", "FESA4.SA", "VAMO3.SA", "JBSS3.SA", "FLRY3.SA", "SAPR4.SA",
    "SLCE3.SA", "VIVT3.SA", "GGBR4.SA", "BRSR6.SA", "RAPT4.SA", "KLBN4.SA", "AURA33.SA",
    "ALUP11.SA", "NEOE3.SA", "USIM3.SA", "WIZC3.SA", "CYRE3.SA", "PSSA3.SA", "CSNA3.SA",
    "CSAN3.SA", "B3SA3.SA", "SMTO3.SA", "RENT3.SA", "MULT3.SA", "TASA4.SA", "DXCO3.SA",
    "MDIA3.SA", "CPLE3.SA", "BLAU3.SA", "RDOR3.SA", "SUZB3.SA", "TUPY3.SA", "WEGE3.SA",
    "ELET3.SA", "RAIL3.SA", "PRIO3.SA", "DASA3.SA", "BRKM5.SA", "CGAS3.SA", "MRFG3.SA",
    "STBP3.SA", "PETZ3.SA"
]

# === Data Fetcher ===
def get_financial_data(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm?symbol={ticker}&apikey={API_KEY}"
        response = requests.get(url).json()
        if not response:
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
    except:
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

# Save final script for download
final_path = Path("/mnt/data/Magic_Formula_B3_TTM_Final.py")
final_path.write_text(final_script)

str(final_path)
