'''Investment Simulation'''
from Robinhood import Robinhood
import numpy as np


class Simulation:
    
    def __init__(self, sim_length, tickers, initial_investment, strategies, date_offset=0):
        self.sim_length = sim_length
        self.tickers = tickers
        self.initial_investment = initial_investment
        self.strategies = strategies
        self.date_offset = date_offset
        self.gen_strategies()
        self.load_prices()

        assert date_offset + sim_length < len(self.full_market[:,0,0]), \
            "sim_length + date_offset must be < {}".format(len(self.full_market[:,0,0]))
              
        
    def gen_strategies(self):
        self.strategies = [s[0](cash=self.initial_investment,
                                tickers=self.tickers,
                                **s[1]) for s in self.strategies]

    def load_prices(self, interval='day'):
        
        trader = Robinhood()

        # get prices
        # note: api takes 75 or fewer tickers
        self.ticker_prices = []
        segments = list(range(0, len(self.tickers), 75))
        if segments[-1] != len(self.tickers):
            segments.append(len(self.tickers))

        for i in list(range(1, len(segments))):
            tp = trader.get_historical_quotes(self.tickers[segments[i-1]:segments[i]],
                                                              interval='day',
                                                              span='year')['results']
            self.ticker_prices = self.ticker_prices + tp
            
        self.full_market = np.zeros((len(self.ticker_prices[0]['historicals']), # day dim
                                     len(self.tickers), # ticker dim
                                     2)) # var dim (open, close)
        self.len_hist = self.full_market.shape[0]
        
        # for each day
        for day in list(range((self.len_hist - 1))):
            for ticker in list(range(len(self.tickers))):
                if self.ticker_prices[ticker]['historicals']:
                    day_ticker_p = self.ticker_prices[ticker]['historicals']\
                                   [self.len_hist - 1 - day]
                    p_open = day_ticker_p['open_price']
                    p_close = day_ticker_p['close_price']
                    self.full_market[day][ticker] = [p_open, p_close]
                else:
                    self.full_market[day][ticker] = [None, None]
        
    def sim(self):
        for day in list(range(self.sim_length)):
            history = self.full_market[self.date_offset + self.sim_length - day:, :, :]
            market = self.full_market[self.date_offset + (self.sim_length - day - 1), :, :]
            for strategy in self.strategies:
                strategy.choose(history=history, market=market)

    def results(self):
        res = {strategy: round(strategy.cash, 2) for strategy in self.strategies}
        return(res)

