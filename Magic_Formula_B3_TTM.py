import pandas as pd
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
    "STBP3.SA", "PETZ3.SA", "MSFT", "AMZN",
]

# === Data Fetcher ===
def get_financial_data(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={API_KEY}"
        response = requests.get(url).json()
        if not response:
            raise ValueError("Empty response")

        metrics = response[0]
        ey = metrics.get("earningYield", None)
        roic = metrics.get("returnOnCapitalEmployed", None)

        ey_pct = ey * 100 if ey is not None else None
        roic_pct = roic * 100 if roic is not None else None
        weighted_score = (ey_pct * 1.0 + roic_pct * 0.2) if ey_pct is not None and roic_pct is not None else None

        return {
            "Ticker": ticker,
            "ReportDate": metrics.get("date"),
            "EarningsYield": ey_pct,
            "ROIC": roic_pct,
            "WeightedScore": weighted_score
        }
    except Exception:
        return {
            "Ticker": ticker,
            "ReportDate": None,
            "EarningsYield": None,
            "ROIC": None,
            "WeightedScore": None
        }

# === UI Content ===
if language == "PT-BR":
    st.title("📈 Fórmula Mágica - Ações B3 (TTM)")
    st.caption("Dados por Financial Modeling Prep API")
    st.markdown("""
    ### 🧠 Lógica da Fórmula Mágica
    Criada por Joel Greenblatt, essa estratégia busca identificar empresas **baratas e lucrativas**.

    - **Earnings Yield (EY)**: mostra o quão barata está uma ação com base no lucro operacional.
    - **ROIC** (Retorno sobre Capital Investido): mede a eficiência da empresa ao usar seu capital para gerar lucros.

    A pontuação final dá **peso maior para ações baratas**, sem ignorar qualidade.

    📐 **Fórmula usada para ranqueamento:**
    ```
    Pontuação = (Earnings Yield × 1.0) + (ROIC × 0.2)
    ```
    """)
else:
    st.title("📈 Magic Formula - B3 Stocks (TTM)")
    st.caption("Data provided by Financial Modeling Prep API")
    st.markdown("""
    ### 🧠 Magic Formula Logic
    Created by Joel Greenblatt, this strategy aims to find companies that are both **cheap and profitable**.

    - **Earnings Yield (EY)**: shows how cheap a stock is based on operating earnings.
    - **ROIC** (Return on Invested Capital): measures how efficiently a company generates profits from its capital.

    The final score **gives more weight to cheapness**, while still rewarding quality.

    📐 **Scoring formula used for ranking:**
    ```
    Score = (Earnings Yield × 1.0) + (ROIC × 0.2)
    ```
    """)

# === Data Load and Ranking ===
data = pd.DataFrame([get_financial_data(ticker) for ticker in TICKERS])
data = data.dropna(subset=["WeightedScore"])
data = data.sort_values(by="WeightedScore", ascending=False).reset_index(drop=True)
data["MagicFormulaRank"] = data.index + 1

# === Full Width Table ===
display = data[[
    "Ticker", "ReportDate", "EarningsYield", "ROIC", "WeightedScore", "MagicFormulaRank"
]].copy()
display["EarningsYield"] = display["EarningsYield"].apply(lambda x: f"{x:.1f}%" if x is not None else "N/A")
display["ROIC"] = display["ROIC"].apply(lambda x: f"{x:.1f}%" if x is not None else "N/A")
display["WeightedScore"] = display["WeightedScore"].apply(lambda x: f"{x:.1f}" if x is not None else "N/A")

st.dataframe(display, use_container_width=True)

# === Interactive Charts ===
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Dispersão EY vs ROIC" if language == "PT-BR" else "### 📊 EY vs ROIC Scatterplot")
    fig_scatter = px.scatter(
        data, x="EarningsYield", y="ROIC", text="Ticker",
        title="Dispersão EY vs ROIC" if language == "PT-BR" else "EY vs ROIC Scatterplot",
        labels={"EarningsYield": "EY (%)", "ROIC": "ROIC (%)"},
        template="plotly_dark"
    )
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.markdown("### 🔥 Mapa de Calor por Pontuação (Top 20)" if language == "PT-BR" else "### 🔥 Heatmap by Score (Top 20)")
    heat_data = data.head(20).set_index("Ticker")[["EarningsYield", "ROIC", "WeightedScore"]].T
    fig_heatmap = px.imshow(
        heat_data,
        text_auto=".1f",
        color_continuous_scale="Blues",
        aspect="auto",
        title="Mapa de Calor por Métrica" if language == "PT-BR" else "Metric Heatmap"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# === Full Width Bar Chart ===
st.markdown("### 🏅 Top 20 Empresas - Pontuação Total" if language == "PT-BR" else "### 🏅 Top 20 Companies - Weighted Score")
top20 = data.head(20)
fig_bar = px.bar(
    top20, x="Ticker", y="WeightedScore",
    title="Top 20 por Pontuação Final" if language == "PT-BR" else "Top 20 by Weighted Score",
    labels={"WeightedScore": "Pontuação" if language == "PT-BR" else "Score"},
    template="plotly_white"
)
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)
