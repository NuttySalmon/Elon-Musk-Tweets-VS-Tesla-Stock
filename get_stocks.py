import yfinance as yf
import pandas as pd

if __name__ == "__main__":
    data = yf.download("TSLA ^IXIC", start="2016-01-01", end="2020-05-02", interval="1d", tz='EST')
    data.to_pickle('tsla.pkl')