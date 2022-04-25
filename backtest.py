import backtrader as bt
from strats import TestStrategy


class MyStrategy(bt.Strategy):
    def next(self):
        pass #Do something

#Instantiate Cerebro engine
cerebro = bt.Cerebro()
cerebro.broker.set_cash(50)
print('Starting at %.2f' % cerebro.broker.getvalue())


data = bt.feeds.YahooFinanceCSVData(
    dataname = 'ADA-USD.csv',
    reverse=False)


cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)

#Run Cerebro Engine
cerebro.run()
print('Result Value: %.2f' % cerebro.broker.getvalue())
