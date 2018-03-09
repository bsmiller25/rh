import rh
import finsymbols

# sim parameters
sim_length = 10
cash = 50
sp500 = finsymbols.get_sp500_symbols()
tickers = [ticker['symbol'] for ticker in sp500]

strategies = [(rh.strategies.Random, dict()),
              (rh.strategies.BTFD, dict()),
              (rh.strategies.Momentum, dict()),
              (rh.strategies.BTFD, dict(dip_len=5)),
              (rh.strategies.Momentum, dict(mo_len=5)),]


sim = rh.Simulation(sim_length, tickers, 50, strategies)
sim.sim()
print(sim.results())

