from datetime import datetime
from stockPred import *
import time
import yfinance as yf
import matplotlib.pyplot as plt
import os
# from stockListCleaner import *
#from alapacaAPI import limitTakeProfitStopLoss as putOrder
#from alapacaAPI import ChangeOrderStatus as orderStatus, accountValue, getBuyOrderPrice, orderDet, replaceSellLimitOrder
from UI import inputUI
import tkinter as tk
from tkinter import ttk
import random
import threading
import random
import yfinance as yf
from alapacaAPI import ChangeOrderStatus as orderStatus, getOrderId, orderLimitPriceDetails, orderPrice, setSecret, cancelOrder, LookForOrderId,accountValue, getBuyOrderPrice, orderDet, replaceSellLimitOrder, limitTakeProfitStopLoss as putOrder, orderPrice, orderLimitPriceDetails, getOrderPriceDetails, calculateMoney
from tradingStrat import strat
from stockPred import doAnalysis
from stockListCleaner import cleaner
import pytz
from datetime import datetime, timedelta, timezone
import traceback


last5 = [0, 0, 0, 0, 0]
goodForBuy = []
counter = 0
sellList = []
buyList = []
timeoutForBuy = time.time()
buySuspended = False
suspensionReason = ""
def seperate(value):
    return value.split("=")[1].strip(" ")


if not (os.path.exists('./botinfo.txt')):
    file = open('botinfo.txt', 'w')
    file.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = 100\nvalue = 0 ")
    file.close()


def updateLastOrder(order):
    global last5, counter
    if counter >= 5:
        counter = 0
    last5[counter] = order
    counter += 1


botInfoRead = open('botinfo.txt', 'r')
botInfo = botInfoRead.read().split('\n')
bought = botInfo[0].split('=')[1].strip(" ") == "True"
if bought:
    stockBought = seperate(botInfo[1])
    buyPrice = float(seperate(botInfo[2]))
    sellPrice = float(seperate(botInfo[3]))
    sellNegative = buyPrice - (buyPrice * 0.1)
    shares = float(seperate(botInfo[4]))
    money = float(seperate(botInfo[5]))
    value = float(seperate(botInfo[6]))
    orderId = seperate(botInfo[7])
    updateLastOrder(stockBought)
else:
    stockBought = ""
    buyPrice = 0
    sellPrice = 0
    shares = 0
    value = 0
    sellNegative = 0
    orderId = 0
    root = tk.Tk()
    inputui = inputUI(root)
    inputui.startUI()
    root.mainloop()
    money = inputui.getValue()
    key, secret, url = inputui.getSecret()
    if inputui.Cont.get():
        sellList = inputui.cont(key, secret)
    setSecret(key, secret, url)
botInfoRead.close()


def run_bot():
    global sellList, goodForBuy, last5, money, buySuspended
    if int(money)>1 and (not buySuspended):
        try:
            #cleaner()
            #doAnalysis()
            analyze()
        except Exception as e:
            print(e)
    lock = threading.Lock()

    buyThread = threading.Thread(target=buy, name="buyThread", args=())
    sellThread = threading.Thread(target=sell, name="sellThread", args=())

    buyThread.start()
    sellThread.start()

    buyThread.join()
    sellThread.join()



def analyze():
    global buyPrice, sellPrice
    file = open("stocks.csv", 'r')
    file.readline()
    file = file.read().split('\n')
    try:
        for line in file:
            stock = line.split(",")
            if float(stock[2]) <= float(stock[11]):
                goodForBuy.append(stock)
    except IndexError as e:
        pass
    except Exception as e:
        tb = traceback.format_exc()
        print("trace", tb, "error", e)


def buy():
    retry = 0
    global goodForBuy, last5, sellList, money, timeoutForBuy, buySuspended, suspensionReason
    mon = 0
    if int(money)<=1:
        return
    buyingPower = strat(money)
    if timeoutForBuy > time.time():
        print("buy suspended for ", (timeoutForBuy-time.time())//3600, "hours and ",((timeoutForBuy-time.time())%3600)//60, "minutes", "will resume at", datetime.fromtimestamp(timeoutForBuy))
        print("reason for suspension", suspensionReason)
        buySuspended = True
        return
    buySuspended = False
    for mon in buyingPower:
        if retry > 10:
            break
        randomList = []
        for stock in goodForBuy:
                if retry >10:
                    buySuspended = True
                    timeoutForBuy = 24*3600 + time.time()
                    break
                try:
                    num = random.randint(0, len(goodForBuy)-1)
                    while num in randomList and goodForBuy[num] in last5:
                        num = random.randint(0, len(goodForBuy)-1)
                    stock = goodForBuy[num]
                    low = orderPrice(stock[0])
                    print(stock[0], low)
                    if round(float(stock[2]), 2) >=low and money>=low:
                        print("stock",stock[0],"stock buy Price",stock[2], "Current Stock Price", low, "Value", mon)
                        buyPrice = low
                        sellPrice = round((low+(float(stock[1])/2)),2)
                        stockBought = stock[0]
                        shares = mon // low
                        sellNegative = round((buyPrice - (buyPrice * 0.07)), 2)
                        status, orderId = putOrder(stockBought, shares, round(low, 2), sellNegative, sellPrice)
                        if status == 200:
                            order = orderDet(orderId['buy'])
                            if order!= None:
                                limit_price = order.limit_price
                                qty = order.qty
                            else:
                                limit_price = mon
                                qty = shares
                            sellList.append([stockBought, qty, orderId])
                            updateLastOrder(stockBought)
                            money = money - (float(limit_price) * float(order.qty))
                            retry = 0
                            break
                        elif(status == 500 and orderId=="timeout"):
                            retry +=1
                    time.sleep(1)
                except Exception as e:
                    tb = traceback.format_exc()
                    print("trace", tb, "error", e)

def getTimeDifference(time, day=0, hours=0, weeks=0, minutes=0):
    now = datetime.now(timezone.utc).replace(tzinfo=pytz.UTC)
    time_difference = now - time
    return time_difference>timedelta(days=day, hours=hours, weeks=weeks, minutes=minutes)
'''
#TODO: 1. When we buy a stock and if the stop loss is excecuted with 3 strikes switch to paper account do simulations until you get 3 strikes back
       2. Gather the info for which stocks it has been successfull and only use the stock that has prediction success rate to be more than 70%
       3. If no prediction assume prediction to be 100% and adjust accordingly
       
       Second working prototype
       Check market idicators. If bearish push for buy and if market is bullish force sell for profit.
       apply moving avgs for stocks(I think it's already implemented just need adjustments)

       Third working prototype
       A gui that will cancel allow you to cancel and do other things like start and stop
       
'''

def sell():
    global sellList, shares, money
    # two possibilities if the stock is on hold or acutually excecuted. Either way just look for order id or stockBought for sell order
    for stock in sellList:
        time.sleep(0.2)
        try:
            if len(stock)>=3:
                limit_orderId = stock[2]["limitSell"]
                stop_orderId = stock[2]["Stop_limit"]
                if orderStatus(stock[2]["buy"])=='filled':
                    if 'orderFilledTime' not in stock[2]:
                        det = orderDet(stock[2]["buy"])
                        stock[2]['orderFilledTime'] = det.filled_at
                    getOrderPriceDetails(stock[2])
                elif getTimeDifference(orderDet(stock[2]["buy"]).submitted_at.replace(tzinfo=pytz.UTC), day=3):
                    corderdet = cancelOrder(stock[2]["buy"])
                    if corderdet[0].status == 'canceled':
                        money+=corderdet[1]
                        sellList.pop(sellList.index(stock))
                limit_status = orderStatus(limit_orderId)
                stop_status = orderStatus(stop_orderId)
                #TODO: make it robust so if half n half than apply that price
                if limit_status == 'filled':
                    # remove the order from the list, update the money, and update file
                    filledmoney,remove= calculateMoney(limit_orderId)
                    if remove:
                        sellList.pop(sellList.index(stock))
                        money += filledmoney
                elif stop_status == "filled":
                    filledmoney, remove = calculateMoney(stop_orderId)
                    if remove:
                        sellList.pop(sellList.index(stock))
                        money += filledmoney
                elif orderStatus(stock[2]["buy"])=='filled':
                    if getTimeDifference(stock[2]['orderFilledTime'].replace(tzinfo=pytz.UTC), day=5):
                        replaceSellLimitOrder(stock[2])
            else:
                print("starting to look for order \n")
                LookForOrderId(stock[0], stock)
        except Exception as e:
            tb = traceback.format_exc()
            print("trace", tb, "error", e)


valueRetry = 0
while True:
    if float(accountValue())>0.0:
        run_bot()
        valueRetry = 0
    elif valueRetry>3:
        break
    else:
        valueRetry+=1
    time.sleep(60)