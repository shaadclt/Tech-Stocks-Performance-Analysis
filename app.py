import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.express as px
import streamlit as st

@st.cache
def load_data(start_date, end_date, selected_tickers):
    df_list = []

    for ticker in selected_tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        df_list.append(data)

    df = pd.concat(df_list, keys=selected_tickers, names=['Ticker', 'Date'])
    df = df.reset_index()

    df['MA10'] = df.groupby('Ticker')['Close'].rolling(window=10).mean().reset_index(0, drop=True)
    df['MA20'] = df.groupby('Ticker')['Close'].rolling(window=20).mean().reset_index(0, drop=True)
    df['Volatility'] = df.groupby('Ticker')['Close'].pct_change().rolling(window=10).std().reset_index(0, drop=True)

    return df

def main():
    st.title("Tech Stocks Performance Analysis")

    # Date selection
    start_date = st.date_input("Start Date", datetime.now() - pd.DateOffset(months=3))
    end_date = st.date_input("End Date", datetime.now())

    if start_date >= end_date:
        st.error("End Date must be greater than Start Date.")
        return

    # Stock selection
    selected_tickers = st.multiselect("Select Stocks", ['AAPL', 'MSFT', 'NFLX', 'GOOG','AMZN','NVDA','TSLA','META','ADBE'])

    if not selected_tickers:
        st.warning("Please select at least one stock.")
        return

    df = load_data(start_date, end_date, selected_tickers)

    # Plot stock market performance
    fig1 = px.line(df, x='Date', y='Close', color='Ticker', title="Stock Market Performance for the Selected Dates")
    st.plotly_chart(fig1)

    # Plot stock prices
    fig2 = px.area(df, x='Date', y='Close', color='Ticker',
                   facet_col='Ticker',
                   labels={'Date': 'Date', 'Close': 'Closing Price', 'Ticker': 'Company'},
                   title='Stock Prices for Selected Stocks')
    st.plotly_chart(fig2)

    # Volatility
    fig3 = px.line(df, x='Date', y='Volatility',
                   color='Ticker',
                   title='Volatility of Selected Stocks')
    st.plotly_chart(fig3)

if __name__ == '__main__':
    main()

footer = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <footer>
        <div style='visibility: visible;margin-top:7rem;justify-content:center;display:flex;'>
            <p style="font-size:1.1rem;">
                <a href="https://imshaad.in/" style="text-decoration: none; color: white;">Made by Mohamed Shaad</a>
                &nbsp;
                <a href="https://www.linkedin.com/in/mohamedshaad">
                    <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="white" class="bi bi-linkedin" viewBox="0 0 16 16">
    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
</svg>        
                </a>
                &nbsp;
                <a href="https://github.com/shaadclt">
                    <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="white" class="bi bi-github" viewBox="0 0 16 16">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                </a>
            </p>
        </div>
    </footer>
"""
st.markdown(footer, unsafe_allow_html=True)
