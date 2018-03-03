from strategies import *

tickers = ['TWTR', 'GPRO']
strategies = [Random, BTFD, RTW]

sim = Simulation(10, tickers, 50, strategies)
sim.sim()
print(sim.results())
