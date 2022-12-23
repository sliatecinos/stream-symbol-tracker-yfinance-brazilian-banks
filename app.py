from datetime import date
from dateutil.relativedelta import relativedelta
import yfinance as yf
import streamlit as st
import plotly.express as px


acoes = {
    "Itau": "ITUB4", "Santander": "SANB11", "Bradesco": "BBDC4", 
    "Banco do Brasil": "BBAS3", "BTG Pactual": "BPAC11", "Banrisul": "BRSR6",
    "Banco PAN": "BRSR6", "Modal": "MODL3"
    }

st.title("Tickers das Ações")
acoes_option = st.sidebar.selectbox(
    "Que banco quer visualizar?", tuple(acoes)
)

start_date = st.sidebar.date_input("Start Date", date.today() - relativedelta(months=1))
end_date = st.sidebar.date_input("End Date", date.today())

data_interval = st.sidebar.selectbox(
    "Data Interval",
    (
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ),
)

symbol_acoes = acoes[acoes_option] + ".SA"

value_selector = st.sidebar.selectbox(
    "Value Selector", ("Open", "High", "Low", "Close", "Adj Close", "Volume")
)

if st.sidebar.button("Gerar"):
    acoes_hist = yf.download(
        symbol_acoes, start=start_date, end=end_date, interval=data_interval
    )

    fig = px.line(acoes_hist, 
        x=acoes_hist.index, y=value_selector,
        labels={"x": "Data"}
        )
    for trace in fig.data:
        for xi, yi in zip(trace.x, trace.y):
            fig.add_annotation(text=f'{yi:.2f}', x=xi, y=yi, xshift=20, yshift=10, showarrow=False)
    
    st.plotly_chart(fig)



