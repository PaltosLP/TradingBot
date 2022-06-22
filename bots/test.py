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
                client = None
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
            qty = int(round(unrounded_qty, 0)) / selling

        print(qty)
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
        
        buyprice = float(order['fills'][0]['price'])
        self.file_log('BUY', buyprice)

        return order



    def file_log(self, side, price):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        current_time = datetime.datetime.now()
        f = open('log.txt', 'a')
        txt = str(current_time) + ' ' + str(self.strategy) + ' ' + str(side) + ' at ' + str(price) + '\n'
        f.write(txt)
        f.close()


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


macd_bot = Bot('ADAUSDT',15, 'macd', 60)

# print(macd_bot.get_min_data())
# print(macd_bot.place_order('BUY'))
macd_bot.file_log('BUY', 5)
