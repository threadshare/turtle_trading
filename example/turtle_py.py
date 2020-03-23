#!/usr/bin/env python  
# -*- coding: utf-8 -*-
'''backtest
start: 2019-01-01 00:00:00
end: 2020-03-02 00:00:00
period: 1d
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","stocks":0}]
args: [["fresh_rete",24],["DC_range",20],["atrlength",14]]
'''

import numpy as np
import pandas as pd
import datetime

data = {'ordertime': [], 'id': [], 'price': []}
hisorder = pd.DataFrame(data)


def turtle():
    # 声明全局变量
    global hisorder

    acct = exchange.GetAccount()

    records = exchange.GetRecords(fresh_rete * 60 * 60)

    ticker = exchange.GetTicker()

    portfolio_value = acct.Balance + acct.FrozenBalance + (acct.Stocks + acct.FrozenStocks) * records[-1]['Close']
    atr = TA.ATR(records, atrlength)[-1]
    # 计算得到unit大小
    value = portfolio_value * trade_percent
    unit = min(round(value / atr, 4), round(acct.Balance / (ticker['Last'] + 100), 4))
    # unit =  round(value/atr,2)

    df = pd.DataFrame(records)
    current_price = records[-1]['Close']
    last_price = 0
    if len(hisorder) != 0:
        last_price = hisorder.iloc[-1]['price']
    max_price = df[-DC_range:-2]['High'].max()
    min_price = df[-int(DC_range / 2):-2]['Low'].min()

    opensign = len(hisorder) == 0 and current_price > max_price

    addsign = len(hisorder) != 0 and current_price > last_price + 0.5 * atr

    stopsign = len(hisorder) != 0 and current_price < min_price

    closesign = len(hisorder) != 0 and current_price < (last_price - 2 * atr)

    #    if _D(records[-1]['Time']/1000) == '2020-01-25 00:00:00':
    #        Log("records[-1]",records[-1])

    if opensign | addsign:
        if acct.Balance >= (ticker['Last'] + 10) * unit and unit > 0:
            id = exchange.Buy(ticker['Last'] + 10, unit)
            orderinfo = exchange.GetOrder(id)
            data = {'ordertime': _D(records[-1]['Time'] / 1000), 'id': id, 'price': records[-1]['Close']}
            hisorder = hisorder.append(data, ignore_index=True)
            Log('买入后，最新账户信息：', exchange.GetAccount())
            Log("opensign", opensign, "addsign", addsign)
    #    else:
    #        Log('余额已不足，请充值......', exchange.GetAccount())
    if stopsign | closesign:
        exchange.Sell(-1, acct.Stocks + acct.FrozenStocks)
        data = {'ordertime': [], 'id': [], 'price': []}
        hisorder = pd.DataFrame(data)
        Log('卖出后，最新账户信息：', exchange.GetAccount())
        Log("stopsign", stopsign, "closesign", closesign)


def main():
    while True:
        turtle()
        Sleep(fresh_rete * 60 * 60 * 1000)