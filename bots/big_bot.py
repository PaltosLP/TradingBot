from binance.client import Client
import pandas as pd 
import ta 
from time import sleep
from termcolor import colored
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')


class Bot:
    buying = 3
    selling = 0
    def __init__(self, time_interval, strategy, sleep_time, buying_asset, stable_asset): #amount 
        self.symbol = buying_asset + stable_asset
        self.time_interval = time_interval
        self.strategy = strategy
        self.sleep_time = sleep_time
        self.buying_asset = buying_asset
        self.stable_asset = stable_asset
        self.amount = amount

    def acc_data(self, asset):
            balance = dict()
            balance = client.get_asset_balance(asset = asset)
            return balance["free"] - 10



    def get_min_data(self): 
        utc_time = str(int(self.time_interval) * 60) + 'm UTC'
        interval = str(self.time_interval) + 'm'
        time_err = True
        while time_err == True:
            try:
                df = pd.DataFrame(client.get_historical_klines(self.symbol, interval, utc_time))
                time_err = False
            except:
                print('something wrong with Timeout')
                sleep(self.sleep_time) 

        df = df.iloc[:,:6]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)
        return df

    def place_order(self, side):
        if side == 'BUY':
            unrounded_qty = self.acc_data(self.stable_asset)
            unrounded_qty = float(unrounded_qty) - 0.01 * float(unrounded_qty)
            unrounded_qty = unrounded_qty / self.buying
            qty = int(round(unrounded_qty, 0))

        else:
            unrounded_qty = self.acc_data(self.buying_asset)
            unrounded_qty = float(unrounded_qty)  - 0.01 * float(unrounded_qty)
            unrounded_qty = unrounded_qty / self.selling
            qty = int(round(unrounded_qty, 0))

        qty_err = True
        while qty_err == True:
            try:
                order = client.create_order(
                    symbol = self.symbol,
                    side = side,
                    type = 'MARKET',
                    quantity = qty,
                )
                qty_err = False
            except:
                print('something wrong with qty')
                sleep(self.sleep_time)

        if side == 'BUY':
            self.buying -= 1
            self.selling += 1
        else:
            self.selling -= 1
            self.buying += 1

        return order



    def trading_strat(self, open_pos = False):
        while True:
            df = self.get_min_data()
            if not open_pos:
                if self.check('BUY', df):
                    order = self.place_order('BUY')
                    open_pos = True
                    buyprice = float(order['fills'][0]['price'])
                    print(f'{self.strategy} bought at', buyprice)
                    sleep(self.sleep_time)
                    break
                sleep(self.sleep_time)
        if open_pos:
            while True:
                df = self.get_min_data()
                if self.check('SELL',df):
                    order = self.place_order('SELL')    #qty-(0.01*qty)
                    sellprice = float(order['fills'][0]['price'])
                    print(f'{self.strategy} sold at {sellprice}')
                    profit = sellprice - buyprice
                    print(f'{self.strategy} did {profit} amount of profit')
                    open_pos = False
                    break
                sleep(self.sleep_time)


    def check(self, side, df):
        if self.strategy == 'macd':
            if side == 'BUY':
                self.check_macd_open(df)
            elif side == 'SELL':
                self.check_macd_close(df)

        elif self.strategy == 'rsi':
            if side == 'BUY':
                self.check_rsi_open(df)
            elif side == 'SELL':
                self.check_rsi_close(df)

        elif self.strategy == 'stoch':
            if side == 'BUY':
                self.check_stoch_open(df)
            elif side == 'SELL':
                self.check_stoch_close(df)

        
    def check_macd_open(self, df):
        buy_sig = False
        # print(ta.trend.macd_diff(df.Close))
        # print(ta.trend.macd_diff(df.Close).iloc[-1])
        if ta.trend.macd_diff(df.Close).iloc[-1] > 0 \
        and ta.trend.macd_diff(df.Close).iloc[-2] < 0:
            buy_sig = True
            return buy_sig

    def check_macd_close(self, df):
        sell_sig = False
        if ta.trend.macd_diff(df.Close).iloc[-1] < ta.trend.macd_diff(df.Close).iloc[-3]:
            sell_sig = True
            return sell_sig

    def check_rsi_open(self, df):
        buy_sig = False
        # print(ta.trend.macd_diff(df.Close))
        # print(ta.trend.macd_diff(df.Close).iloc[-1])
        if ta.momentum.rsi(df.Close).iloc[-1] < 32:
            buy_sig = True
            return buy_sig

    def check_rsi_close(self, df):
        sell_sig = False
        if ta.momentum.rsi(df.Close).iloc[-1] > 60:
            sell_sig = True
            return sell_sig

    def check_stoch_open(self, df):
        buy_sig = False
        # print(ta.trend.macd_diff(df.Close))
        # print(ta.trend.macd_diff(df.Close).iloc[-1])

        stoch = ta.momentum.stoch(high = df.High ,low = df.Low, close = df.Close).iloc[-1]
        stoch_sig = ta.momentum.stoch_signal(high = df.High ,low = df.Low, close = df.Close).iloc[-1]
        if stoch < 20 and stoch_sig < 20:
            if stoch > stoch_sig:
                buy_sig = True
                return buy_sig

    def check_stoch_close(self, df):
        sell_sig = False

        stoch = ta.momentum.stoch(high = df.High ,low = df.Low, close = df.Close).iloc[-1]
        stoch_sig = ta.momentum.stoch_signal(high = df.High ,low = df.Low, close = df.Close).iloc[-1]
        if stoch > 78 and stoch_sig > 20:
            if stoch == stoch_sig:
                sell_sig = True
                return sell_sig


    def start(self):
        while True:
            print(colored(self.acc_data(self.stable_asset), 'green'))
            self.trading_strat()


macd_bot = Bot(15, 'macd', 60, 'ADA', 'USDT')
rsi_bot = Bot(15, 'rsi', 60, 'ADA', 'USDT')
stoch_bot = Bot(15, 'stoch', 60, 'ADA', 'USDT')

macd_bot.start()
sleep(60)
rsi_bot.start()
sleep(60)
stoch_bot.start()


