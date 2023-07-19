import time
from os import getenv
from datetime import datetime, timedelta
import numpy as np

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame

'''
    This is a trading script that you can run in the cloud and customize with your own trading algorithms.

    The example uses the Alpaca Trading API, which is a free algorithmic trading platform that allows for paper trading.
    You can setup a free account on Alpaca here: https://alpaca.markets/

    Alternatively, edit the `get_data`, `buy`, and `sell` functions to connect your own APIs.
'''

PUB_KEY = getenv('ALPACA_KEY')
SEC_KEY = getenv('ALPACA_SECRET')

trade = TradingClient(PUB_KEY, SEC_KEY)
data = StockHistoricalDataClient(PUB_KEY, SEC_KEY)

def get_data(symb):
    # Returns a numpy array of the closing prices of the past 15 minutes
    market_data = data.get_stock_bars(StockBarsRequest(
        symbol_or_symbols = symb,
        timeframe = TimeFrame.Minute,
        start = datetime.now() - timedelta(minutes=30),
        end = datetime.now() - timedelta(minutes=15),
    ))
    
    close_list = market_data.df['close']
    return close_list

# Returns nothing, makes call to buy stock
def buy(q, s):
    trade.submit_order(order_data=MarketOrderRequest(
        symbol=s,
        qty=q,
        side='buy',
        time_in_force='gtc'
    ))

# Returns nothing, makes call to sell stock
def sell(q, s):
    trade.submit_order(order_data=MarketOrderRequest(
        symbol=s,
        qty=q,
        side='sell',
        time_in_force='gtc'
    ))

symb = "SPY" # Ticker of stock you want to trade
pos_held = False

while True:
    print("")
    print("Checking Price")

    close_list = get_data(symb)

    ma = np.mean(close_list)
    last_price = close_list[-1]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    # Make buy/sell decision
    # This algorithm buys or sells when the moving average crosses the most recent closing price

    if ma + 0.1 < last_price and not pos_held: # Buy when moving average is ten cents below the last price
        print("Buy")
        buy(1, symb)
        pos_held = True

    elif ma - 0.1 > last_price and pos_held: # Sell when moving average is ten cents above the last price
        print("Sell")
        sell(1, symb)
        pos_held = False

    time.sleep(60)
