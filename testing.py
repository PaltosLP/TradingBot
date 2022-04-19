from binance.client import Client
import pandas as pd
import ta
from time import sleep
from termcolor import colored
import config


client = Client(config.apiKey, config.apiSecurity)
print('logged in')


def place_order(self, side):
     order = client.create_order(
         symbol = self.symbol,
         side = side,
         type = 'MARKET',
         quantity = self.qty,
   )

def curr_price():
    avg_price = client.get_avg_price()
    return avg_price['price']



def acc_data(asset):
    balance = dict()
    balance = client.get_asset_balance(asset = asset)
    return balance["free"]

def qty_calc(asset):
    balance = acc_data(asset)
    price = curr_price()
    amount = (float(balance)-3) / float(price)
    amount = round(amount, 0)
    return amount


def exe(symbol):
    buying_asset = symbol[0:3]
    selling_asset = symbol[3:len(symbol)+1]
    return buying_asset, selling_asset



def place_order(side,symbol):
    buying_asset = symbol[0:3]
    stable_asset = symbol[3:len(symbol)+1]
    if side == 'BUY':
         unrounded_qty = acc_data(stable_asset)
         unrounded_qty = float(unrounded_qty)
         qty = round(unrounded_qty, 0)
         print(qty, type(qty))
 
    else:
         unrounded_qty = acc_data(buying_asset)
         unrounded_qty = float(unrounded_qty)
         qty = round(unrounded_qty, 0)

    order = client.create_order(
          symbol = symbol,
          side = side,
          type = 'MARKET',
           quantity = qty,
       )
    return order


print(place_order('BUY', 'ADAUSDT'))
