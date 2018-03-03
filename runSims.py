from strategies import *

tickers = ['TWTR', 'GPRO']
strategies = [Random, BTFD, RTW]

sim = Simulation(10, tickers, 50, strategies, date_offset=0)
sim.sim()
sim.results()

