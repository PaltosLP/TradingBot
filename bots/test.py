from binance.client import Client
import pandas as pd 
import ta 
from time import sleep
from termcolor import colored
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')

def place_order(side):
    if side == 'BUY':
        buying = file_get('BUY')
        unrounded_qty = acc_data('USDT')
        unrounded_qty = float(unrounded_qty) - 0.01 * float(unrounded_qty)
        qty = int(round(unrounded_qty, 0)) / buying

    else:
        selling = file_get('SELL')
        unrounded_qty = acc_data('ADA')
        unrounded_qty = float(unrounded_qty)  - 0.01 * float(unrounded_qty)
        qty = int(round(unrounded_qty, 0)) / selling

    # qty_err = True
    # while qty_err == True:
    #     try:
    #         order = client.create_order(
    #             symbol = self.symbol,
    #             side = side,
    #             type = 'MARKET',
    #             quantity = qty,
    #         )
    #         qty_err = False
    #     except:
    #         print('something wrong with qty')
    #         sleep(self.sleep_time)
    #




    if side == 'BUY':
        file_change('BUY')
    else:
        file_change('SELL')

    # return order
    return qty


def file_get(side):
    f = open("info.txt")
    lines = f.readlines()
    buying = int(list(lines[1])[0])
    selling = int(list(lines[4])[0])
    f.close()
    if side == 'BUY':
        return buying
    else:
        return selling

def file_change(side):
    buying = file_get('BUY')
    selling = file_get('SELL')

    if side == 'BUY':
        buying -= 1
        selling += 1
    else:
        buying += 1
        selling -= 1

    f = open("info.txt", 'w')
    f.write(f"Buying:\n{buying}\n\nSelling:\n{selling}")
    f.close()


def acc_data(asset):
        balance = dict()
        balance = client.get_asset_balance(asset = asset)
        return balance["free"]



print(place_order('BUY'))


