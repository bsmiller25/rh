'''Investment Strategies'''
import numpy as np


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
        # Randomly choose a ticker and make sure we can afford at least one
        choosing = True
        while choosing:
            choice = self.tickers[np.random.randint(len(self.tickers))]
            if market[self.tickers.index(choice), 0] < self.cash:
                choosing = False
        
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

        # choose and make sure we can afford at least one
        choosing = True
        worst = 0
        while choosing:
            choice = self.tickers[perf.argsort()[worst]]
            if market[self.tickers.index(choice), 0] < self.cash:
                choosing = False
            else:
                worst += 1
                
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

        # choose and make sure we can afford at least one
        choosing = True
        best = -1
        while choosing:
            choice = self.tickers[perf.argsort()[best]]
            if market[self.tickers.index(choice), 0] < self.cash:
                choosing = False
            else:
                best -= 1
        
        # invest
        self.invest(choice, market)

    def __str__(self):
        return(self.name)
    __repr__ = __str__

