from binance.client import Client
import pandas as pd 
import ta 
from time import sleep
from termcolor import colored
import datetime
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')


class Bot:
    
    def __init__(self, symbol, time_interval, strategy, sleep_time):
        self.symbol = symbol 
        self.time_interval = time_interval
        self.strategy = strategy
        self.sleep_time = sleep_time
        self.buying_asset = symbol[0:3]
        self.stable_asset = symbol[3:len(symbol)+1]

    def acc_data(self, asset):
            balance = dict()
            balance = client.get_asset_balance(asset = asset)
            return balance["free"]



    def get_min_data(self): 
        utc_time = str(int(self.time_interval) * 60) + 'm UTC'
        interval = str(self.time_interval) + 'm'
        time_err = True
        client = Client(config.apiKey, config.apiSecurity)
        while time_err == True:
            try:
                df = pd.DataFrame(client.get_historical_klines(self.symbol, interval, utc_time))
                time_err = False
            except:
                print('something wrong with Timeout')
                sleep(300)
                client = Client(config.apiKey, config.apiSecurity)
                sleep(self.sleep_time)

        df = df.iloc[:,:6]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)
        return df

    def place_order(self, side):
        client = Client(config.apiKey, config.apiSecurity)
        if side == 'BUY':
            buying = self.file_get('BUY')
            unrounded_qty = self.acc_data(self.stable_asset)
            unrounded_qty = float(unrounded_qty) - 0.01 * float(unrounded_qty)
            unrounded_qty = unrounded_qty / buying
            qty = int(round(unrounded_qty, 0))

        else:
            selling = self.file_get('SELL')
            unrounded_qty = self.acc_data(self.buying_asset)
            unrounded_qty = float(unrounded_qty)  - 0.01 * float(unrounded_qty)
            unrounded_qty = unrounded_qty / selling
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
                sleep(300)
                client = Client(config.apiKey, config.apiSecurity)
                sleep(self.sleep_time)


        if side == 'BUY':
            self.file_change('BUY')
        else:
            self.file_change('SELL')

        return order


    def file_get(self, side):
        f = open("info.txt")
        lines = f.readlines()
        buying = int(list(lines[1])[0])
        selling = int(list(lines[4])[0])
        f.close()
        if side == 'BUY':
            return buying
        else:
            return selling

    def file_change(self, side):
        buying = self.file_get('BUY')
        selling = self.file_get('SELL')

        if side == 'BUY':
            buying -= 1
            selling += 1
        else:
            buying += 1
            selling -= 1

        f = open("info.txt", 'w')
        f.write(f"Buying:\n{buying}\n\nSelling:\n{selling}")
        f.close()

    def trading_strat(self, open_pos = False):
        while True:
            df = self.get_min_data()
            if not open_pos:
                if self.check_rsi_open(df):
                    order = self.place_order('BUY')
                    open_pos = True
                    buyprice = float(order['fills'][0]['price'])
                    print('bought at', buyprice)
                    self.file_log('BUY', buyprice)
                    sleep(self.sleep_time)
                    break
                sleep(self.sleep_time)
        if open_pos:
            while True:
                df = self.get_min_data()
                if self.check_rsi_close(df):
                    order = self.place_order('SELL')    #qty-(0.01*qty)
                    sellprice = float(order['fills'][0]['price'])
                    self.file_log('SELL', sellprice)
                    print('sold at', sellprice)
                    profit = sellprice - buyprice
                    print(colored(profit, 'yellow'))
                    open_pos = False
                    break
                sleep(self.sleep_time)

    #def curr_price(self):
        #avg_price = client.get_avg_price(symbol=self.symbol)
        #return avg_price['price']

    #def qty_calc(self, asset):
        #balance = self.acc_data(asset)
        #price = self.curr_price()
        #amount = (float(balance)-3) / float(price)
        #amount = round(amount, 0)
        #return amount
        
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

    def file_log(self, side, price):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        current_time = datetime.datetime.now()
        f = open('log.txt', 'a')
        txt = str(current_time) + ' ' + str(self.strategy) + ' ' + str(side) + ' at ' + str(price) + '\n'
        f.write(txt)
        f.close()

    def start(self):
        while True:
            print(colored(self.acc_data(self.stable_asset), 'green'))
            self.trading_strat()


rsi_bot = Bot('ADAUSDT',15, 'rsi', 60)

rsi_bot.start()


