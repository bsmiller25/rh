from strategies import *

# sim parameters
tickers = ['TWTR', 'GPRO']
sim_length = 10
cash = 50
strategies = [(Random, dict()),
              (BTFD, dict()),
              (Momentum, dict()),
              (BTFD, dict(dip_len=5)),
              (Momentum, dict(mo_len=5)),]


sim = Simulation(sim_length, tickers, 50, strategies)
sim.sim()
print(sim.results())

