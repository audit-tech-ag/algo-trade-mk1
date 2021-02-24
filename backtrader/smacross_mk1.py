# %%

from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
from backtesting.test import SMA, GOOG


# %%
def _read_file(filename):
    from os.path import dirname, join

    return pd.read_csv(filename,
                       index_col=0, parse_dates=True, infer_datetime_format=True)


# %%
class SmaCross(Strategy):
    sma1series = None
    sma2series = None
    sma1 = None
    sma2 = None

    def init(self, *args, **kwargs):
        close = self.data.Close
        self.sma1series = self.I(SMA, close, self.sma1 or 1)
        self.sma2series = self.I(SMA, close, self.sma2 or 5)
        # print(self.sma1)
        # print(self.sma2)

    def next(self):
        if crossover(self.sma1series, self.sma2series):
            self.buy()
            # print('bought: ' , self.sma1, self.sma2)
        elif crossover(self.sma2series, self.sma1series):
            self.sell()


# %%

data = _read_file('../data/SPY_data.csv')
data = _read_file('../data/SPY_NASDAQ_data.csv')
data = _read_file('../data/TQQQ_Nasaq_data.csv')

# %%

bt = Backtest(data, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)

# %%
# output = bt.run()
#
output1 = bt.optimize(sma1=range(20, 30), sma2=range(30, 50), constraint=lambda p: p.sma1 < p.sma2)
print(output1)
bt.plot()

# ,return_optimization=True,method='skopt'
# bt.plot()
