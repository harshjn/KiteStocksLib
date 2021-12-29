#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 08:37:44 2021

@author: harshjain
"""
import os
os.chdir('/Users/harshjain/Development/StockAlgo/Python')
import numpy as np
import pandas as pd
from pprint import pprint # just for neatness of display
import time
import datetime
# from nsetools import Nse
# nse = Nse()
# print('Welcome to Stock Prediction Algorithm by Harsh Jain')
# import StockHarshLib as SHL
# query = SHL.query
# print(nse)

print('welcome to Harsh Kite Library')
import logging
from kiteconnect import KiteConnect
import urllib3
# logging.basicConfig(level=logging.WARNING)
api_key = "__"
api_secret='__';

with open('acc_tkn.txt', 'r') as file:
    acc_tkn = file.read()

kite = KiteConnect(api_key=api_key,access_token=acc_tkn)
# print("Login here:", kite.login_url() )
# acc_tkn=[]
if acc_tkn==[]:
    kite = KiteConnect(api_key=api_key)

    request_token="__"
    gen_ssn = kite.generate_session(request_token, api_secret)
    acc_tkn=gen_ssn['access_token']
    print('access token is:')
    print(acc_tkn)
    with open("acc_tkn.txt", "w") as text_file:
        text_file.write(acc_tkn)
#%%
def KiteStatus():
    # OrderList = kite.orders()
    # HoldingsList = kite.holdings()
    # OrderList.to_csv('Orderlist.csv')
    # HoldingsList.to_csv('holdings.csv')
    OL = pd.DataFrame.from_dict(kite.orders())
    HL = pd.DataFrame.from_dict(kite.holdings())
    
    PnLNet = pd.DataFrame.from_dict(kite.positions()['net'])
    PnLDay = pd.DataFrame.from_dict(kite.positions()['day'])
    
    # margins=kite.margins()['equity']['net']
    
    m=kite.margins()['equity']['available']['live_balance']
    
    return [OL,HL,m,PnLNet,PnLDay]



def KiteSell(STOCK,qty,Type, price):
    if Type=='market' or Type=='MARKET':
        order_id = kite.place_order(tradingsymbol=STOCK,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_SELL,
                                quantity=qty,variety = 'regular', 
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC )
        logging.info("Order placed. ID is: {}".format(order_id))
    else:
        order_id = kite.place_order(tradingsymbol=STOCK,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_SELL,
                                quantity=qty,variety = 'regular', price = price,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                product=kite.PRODUCT_CNC )
        logging.info("Order placed. ID is: {}".format(order_id))

    return order_id


def KiteBuy(STOCK,qty,Type, price=-1):
    if Type=='market' or Type=='MARKET':
        order_id = kite.place_order(tradingsymbol=STOCK,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=qty,variety = 'regular', 
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC )
        logging.info("Order placed. ID is: {}".format(order_id))
    else:
        order_id = kite.place_order(tradingsymbol=STOCK,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=qty,variety = 'regular', price = price,
                                order_type=kite.ORDER_TYPE_LIMIT,
                                product=kite.PRODUCT_CNC )
        logging.info("Order placed. ID is: {}".format(order_id))

    return order_id


def KiteCancel(Order_ID):
    kite.cancel_order('regular',Order_ID)


def KiteQuote(STOCK):
    q=kite.quote(List_NSE_equity.instrument_token[List_NSE_equity.tradingsymbol==STOCK])
    q=pd.DataFrame.from_dict(q).transpose();

    a=q.depth;
    a=pd.DataFrame.from_dict(a[0])
    b=a.buy
    s=a.sell
    print('p b s V')
    print([q.average_price[0],q.buy_quantity[0],q.sell_quantity[0],q.volume[0]])
    # LimitPrice = KiteLimitPrice(MarketDepth=a);
    return q#LimitPrice

def KiteLimitPrice(MarketDepth):
    MD=MarketDepth;
    MD.buy
    
    
#%%

ListInstruments=pd.DataFrame.from_dict(kite.instruments()) ;
ListInstruments.to_csv('ListInstruments.csv')

List_NSE = ListInstruments[ListInstruments.exchange=='NSE']
List_NSE.to_csv('List_NSE.csv')

List_NSE_equity = List_NSE[List_NSE.segment=='NSE']



def CheckMarketKite(List_NSE_equity):
    # SellFracMat = np.ones(len(List_NSE_equity))
    # totalTradedVMat = np.zeros(len(List_NSE_equity))
    # Del2TradMat = np.zeros(len(List_NSE_equity))
    
    iterations = int(np.ceil(len(List_NSE_equity)/1000))
    
    for i in range(iterations):
        if i == iterations-1:
            q= kite.quote(List_NSE_equity.instrument_token[List_NSE_equity.index[i*1000:]]);
        else:
            q= kite.quote(List_NSE_equity.instrument_token[List_NSE_equity.index[i*1000:(i+1)*1000]]);
        
        q_df= pd.DataFrame.from_dict(q).transpose()
        
        
        qBuy=q_df.buy_quantity
        qSell=q_df.sell_quantity
        # circuitFrac = (q_df.last_price.values- q_df.lower_circuit_limit.values)/(q_df.upper_circuit_limit.values-q_df.lower_circuit_limit.values)

        
        # If buy and sell is zero, ignore.
        # SellFrac = sellFrac/(sellFrac+buyFrac)
        
        SellFrac=qSell[qBuy>0]/(qBuy[qBuy>0]+qSell[qBuy>0])
        
        SellFracLow = SellFrac[SellFrac<0.15]
        SellFracLow = SellFracLow[SellFracLow>0]
        
        for indices in SellFracLow.keys():
        # totalTradedVMat[i] = q['totalTradedVolume']
        # Del2TradMat[i] = q['deliveryToTradedQuantity']      
            st=List_NSE_equity[List_NSE_equity.instrument_token==int(indices)];
            aa=st.tradingsymbol
            bb=st.segment
            
            q1 = q_df[q_df.instrument_token == int(indices)]
            
            circuitFracVal = (q1.last_price.values[0]- q1.lower_circuit_limit.values[0])/(q1.upper_circuit_limit.values[0]-q1.lower_circuit_limit.values[0])
            if circuitFracVal>0.6:
                print('sellFrac, price, stock, exch, circuitFrac')
                print(SellFracLow[indices], q1.average_price[0], aa[aa.index[0]], bb[bb.index[0]], circuitFracVal )
        



def kiteSellFast(Holdings):
    # For all elements in holdings, monitor the sell vs buy ratio continuously
    # 
    print(kite.holdings)
    print('selling fast ')
    


