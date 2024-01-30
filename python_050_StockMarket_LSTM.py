import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
import seaborn as sns
from numpy.random import seed
seed(0)


def load_stock_prices(ticker, start_date, end_date):
    """
    Load stock prices for a given ticker symbol and date range.

    Parameters:
    - ticker: Stock symbol (e.g., 'AAPL' for Apple Inc.)
    - start_date: Start date in the format 'YYYY-MM-DD'
    - end_date: End date in the format 'YYYY-MM-DD'

    Returns:
    - DataFrame containing stock prices for the specified date range.
    """
    # Define the date range
    start = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end = dt.datetime.strptime(end_date, "%Y-%m-%d")

    # Download historical stock data from Yahoo Finance
    stock_data = pdr.get_data_yahoo(ticker, start, end)

    return stock_data

# Example usage for Amazon (NASDAQ: AMZN)
nasdaq_ticker = 'AMZN'
start_date = '2023-01-01'
end_date = '2024-01-01'

stock_prices = load_stock_prices(nasdaq_ticker, start_date, end_date)
print(stock_prices)