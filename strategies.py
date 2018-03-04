'''Investment Strategies'''
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
            history = self.full_market[self.date_offset + self.sim_length - day:, :, :]
            market = self.full_market[self.date_offset + (self.sim_length - day - 1), :, :]
            for strategy in self.strategies:
                strategy.choose(history=history, market=market)

    def results(self):
        res = {strategy: strategy.cash for strategy in self.strategies}
        return(res)


class Strategy:
    
    def __init__(self, cash, tickers):
        self.tickers = tickers
        self.cash = cash
        self.portfolio = {}
        self.value = cash
        self.gl = 0

    def purchase(self, ticker, price, shares):
        assert price * shares <= self.cash, "purchase order too expensive"
        
        if ticker in self.portfolio.keys():
            self.portfolio[ticker] += shares
        else:
            self.portfolio[ticker] = shares

        self.cash -= round(price * shares, 2)

    def sell(self, ticker, price, shares):
        assert shares <= self.portfolio[ticker], "not enough shares to sell"
        
        self.portfolio[ticker] -= shares
        if self.portfolio[ticker] == 0:
            self.portfolio.pop(ticker, None)
            
        self.cash += round(price * shares, 2)

    def invest(self, choice, market):
        p_open = market[self.tickers.index(choice), 0]
        num_shares = int(self.cash / p_open)
        self.purchase(choice, p_open, num_shares)
        
        # sell at end of day
        p_close = market[self.tickers.index(choice), 1]
        self.sell(choice, p_close, num_shares)


class Random(Strategy):
    '''Choose a stock randomly'''
    def __init__(self, *args, **kwargs):
        self.name = 'Random'
        super(Random, self).__init__(*args, **kwargs)

    def choose(self, history, market):
        # Randomly choose a ticker
        choice = self.tickers[np.random.randint(len(self.tickers))]

        # invest
        self.invest(choice, market)
        

    def __str__(self):
        return(self.name)
    __repr__ = __str__


class BTFD(Strategy):
    '''Buy choose the stock that performed worst yesterday'''
    
    def __init__(self, dip_len=None, *args, **kwargs):
        if not dip_len:
            self.dip_len = 0
        else:
            self.dip_len = dip_len
        self.name = 'BTFD' + '-{}'.format(self.dip_len)
        super(BTFD, self).__init__(*args, **kwargs)
    
    def choose(self, history, market):
        # get yesterday's performance
        perf = (history[0,:,1] - history[self.dip_len,:,0]) / history[self.dip_len,:,0]
        choice = self.tickers[perf.argmin()]
        
        # invest
        self.invest(choice, market)

    def __str__(self):
        return(self.name)
    __repr__ = __str__


class Momentum(Strategy):
    '''Buy choose the stock that performed best yesterday'''
    
    def __init__(self, mo_len=None, *args, **kwargs):
        if not mo_len:
            self.mo_len = 0
        else:
            self.mo_len = mo_len
        self.name = 'Momentum' + '-{}'.format(self.mo_len)
        super(Momentum, self).__init__(*args, **kwargs)
    
    def choose(self, history, market):
        # get yesterday's performance
        perf = (history[0,:,1] - history[self.mo_len,:,0]) / history[self.mo_len,:,0]
        choice = self.tickers[perf.argmax()]
        
        # invest
        self.invest(choice, market)

    def __str__(self):
        return(self.name)
    __repr__ = __str__

