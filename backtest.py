import backtrader as bt

class MyStrategy(bt.Strategy):
    def next(self):
        pass #Do something

#Instantiate Cerebro engine
cerebro = bt.Cerebro()

#Add strategy to Cerebro
cerebro.addstrategy(MyStrategy)

#Run Cerebro Engine
cerebro.run()
