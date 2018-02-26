'''Investment Strategies'''
from Robinhood import Robinhood
import numpy as np


class Simulation:
    
    def __init__(self, sim_length, tickers, strategies):
        self.sim_length = sim_length
        self.tickers = tickers
        self.strategies = strategies
        self.load_prices()
        
    def load_prices(self, interval='day'):
        
        trader = Robinhood()
        self.ticker_prices = trader.get_historical_quotes(self.tickers,
                                                   interval='day',
                                                   span='year')
        self.full_market = np.zeros((len(self.ticker_prices['results'][0]['historicals']), # day dim
                                     len(self.tickers), # ticker dim
                                     2)) # var dim (open, close)
        self.len_hist = self.full_market.shape[0]
        # for each day
        for day in list(range(self.len_hist)):
            for ticker in list(range(len(self.tickers))):
                day_ticker_p = self.ticker_prices['results'][ticker]['historicals']\
                               [self.len_hist - day - 1]
                p_open = day_ticker_p['open_price']
                p_close = day_ticker_p['close_price']
                self.full_market[day][ticker] = [p_open, p_close]
        
    def sim(self):
        for day in list(range(self.sim_length)):
            history = self.full_market[self.sim_length - day:, :, :]
            market = self.full_market[(self.sim_length - day - 1), :, 0]


class Strategy:
    
    def __init__(self, cash, tickers):
        self.tickers = tickers
        self.cash = cash
        self.portfolio = {}
        self.value = cash
        self.gl = 0
        self.load_hist()

    def purchase(self, ticker, price, shares):
        assert price * shares < self.cash, "purchase order too expensive"
        
        if ticker in self.portfolio.keys():
            self.portfolio[ticker] += shares
        else:
            self.portfolio[ticker] = shares

        self.cash -= price * shares

    def sell(self, ticker, price, shares):
        assert shares <= self.portfolio[ticker], "not enough shares to sell"
        
        self.portfolio[ticker] -= shares
        if self.portfolio[ticker] == 0:
            self.portfolio.pop(ticker, None)
            
        self.cash += price * shares
        self.gl += price * shares
        
        
        
class Random(Strategy):
    def act(self):
        

