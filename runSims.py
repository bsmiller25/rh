from strategies import *
import finsymbols

# sim parameters
sim_length = 10
cash = 50
sp500 = finsymbols.get_sp500_symbols()
tickers = [ticker['symbol'] for ticker in sp500]

strategies = [(Random, dict()),
              (BTFD, dict()),
              (Momentum, dict()),
              (BTFD, dict(dip_len=5)),
              (Momentum, dict(mo_len=5)),]


sim = Simulation(sim_length, tickers, 50, strategies)
sim.sim()
print(sim.results())

