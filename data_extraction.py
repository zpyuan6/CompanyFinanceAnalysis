import yfinance as yf

if __name__ == "__main__":
    # Download data from Yahoo Finance
    data = yf.Ticker("III.L")
    hist = data.history(start="2024-05-01", end="2013-1-1")

    print(hist.loc['Total Revenue'])