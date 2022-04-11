from binance.client import Client
import pandas as pd 
import ta 
from time import sleep
from termcolor import colored
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')


class Bot:
    
    def __init__(self, symbol, qty, time_interval, strategy):
        self.symbol = symbol
        self.qty = qty
        self.time_interval = time_interval
        self.strategy = strategy


    def get_min_data(self): 
        utc_time = str(int(self.time_interval[0]) * 60) + 'm UTC'
        df = pd.DataFrame(client.get_historical_klines(self.symbol, self.time_interval, utc_time))
        df = df.iloc[:,:6]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)
        return df

    def place_order(self, side):
        order = client.create_order(
            symbol = self.symbol,
            side = side,
            type = 'MARKET',
            quantity = self.qty,
        )
        return order

    def trading_strat(self, open_pos = False):
        while True:
            df = self.get_min_data()
            if not open_pos:
                if self.check_macd_open(df):
                    order = self.place_order('BUY')
                    open_pos = True
                    buyprice = float(order['fills'][0]['price'])
                    print('bought at', buyprice)
                    sleep(60 * int(self.time_interval[0]))
                    break
                sleep(45 * int(self.time_interval[0]))
        if open_pos:
            while True:
                df = self.get_min_data()
                if self.check_macd_close(df):
                    order = self.place_order('SELL')    #qty-(0.01*qty)
                    sellprice = float(order['fills'][0]['price'])
                    print('sold at', sellprice)
                    profit = sellprice - buyprice
                    print(profit)
                    open_pos = False
                    break
                sleep(45 * int(self.time_interval[0]))

    def acc_data(self):
        info = client.get_account()
        balance = info['balances'][11]['free']
        return balance

    def curr_price(self):
        avg_price = client.get_avg_price(symbol=self.symbol)
        return avg_price['price']

    def qty_calc(self):
        balance = self.acc_data()
        price = self.curr_price()
        amount = (float(balance)-3) / float(price)
        amount = round(amount, 0)
        return amount
        
    def check_macd_open(self, df):
        buy_sig = False
        if ta.trend.macd_diff(df.Close).iloc[-1] > 0 \
        and ta.trend.macd_diff(df.Close).iloc[-2] < 0:
            buy_sig = True
            return buy_sig

    def check_macd_close(self, df):
        sell_sig = False
        if ta.trend.macd_diff(df.Close).iloc[-1] < ta.trend.macd_diff(df.Close).iloc[-3]:
            sell_sig = True
            return sell_sig



