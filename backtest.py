import backtrader as bt

class MyStrategy(bt.Strategy):
    def next(self):
        pass #Do something

#Instantiate Cerebro engine
cerebro = bt.Cerebro()

cerebro.broker.set_cash(50)

print('Starting at %.2f' % cerebro.broker.getvalue())
#Add strategy to Cerebro
# cerebro.addstrategy(MyStrategy)

#Run Cerebro Engine
cerebro.run()

print('Result Value: %.2f' % cerebro.broker.getvalue())
