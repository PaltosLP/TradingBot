from binance.client import Client
from binance.enums import *
import pandas as pd
import ta
from time import sleep, time
from binance.exceptions import BinanceAPIException
from termcolor import colored

apiKey = "UfI35WaTUybx3M9dYzIzQqZLgMMJjgRZtHN6MtyxQ03SQQT0DAYC8h5xYSpPnuaz"
apiSecurity = "jJ3A9mVMhaC5PQdLOCBIOVouHc0PLlgxVVEaCTnDMb8xOeXKYIoiwK4CNZ6YI4U0"


client = Client(apiKey, apiSecurity)
print("logged in")

def get_min_data(symbol, time_interval):
    
    utc_time = str(int(time_interval[0]) * 60) + 'm UTC'
    df = pd.DataFrame(client.get_historical_klines(symbol, time_interval, utc_time))
    df = df.iloc[:,:6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit='ms')
    df = df.astype(float)
    return df


def place_order(symbol, side, qty):
    order = client.create_order(
        symbol = symbol,
        side = side,
        type = 'MARKET',
        quantity = qty,
    )
    return order
    

def trading_strat(symbol, qty, time_interval, open_pos = False):
    while True:
        df = get_min_data(symbol, time_interval)
        if not open_pos:
            if check_macd_open(df):
                order = place_order(symbol, 'BUY', qty)
                open_pos = True
                buyprice = float(order['fills'][0]['price'])
                print('bought at', buyprice)
                sleep(60 * int(time_interval[0]))
                break
            sleep(45 * int(time_interval[0]))
    if open_pos:
        while True:
            df = get_min_data(symbol, time_interval)
            if check_macd_close:
                order = place_order(symbol, 'SELL', qty=qty)    #qty-(0.01*qty)
                sellprice = float(order['fills'][0]['price'])
                print('sold at', sellprice)
                profit = sellprice - buyprice
                print(profit)
                open_pos = False
                break
            sleep(45 * int(time_interval[0]))


def acc_data():
    info = client.get_account()
    balance = info['balances'][11]['free']
    return balance

def curr_price(symbol):
    avg_price = client.get_avg_price(symbol=symbol)
    return avg_price['price']

def qty_calc(symbol):
    balance = acc_data()
    price = curr_price(symbol)
    amount = (float(balance)-3) / float(price)
    amount = round(amount, 0)
    return amount
    
def check_macd_open(df):
    buy_sig = False
    if ta.trend.macd_diff(df.Close).iloc[-1] > 0 \
    and ta.trend.macd_diff(df.Close).iloc[-2] < 0:
        buy_sig = True
        return buy_sig

def check_macd_close(df):
    sell_sig = False
    if ta.trend.macd_diff(df.Close).iloc[-1] < ta.trend.macd_diff(df.Close).iloc[-3]:
        sell_sig = True
        return sell_sig
        
        
def exe_func(symbol, time_interval):
    while True:
        print(colored(acc_data(), 'green'))
        trading_strat(symbol, qty = qty_calc(symbol), time_interval=time_interval)

exe_func('ADAUSDT', '3m')
#print(acc_data())
