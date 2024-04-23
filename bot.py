from datetime import datetime
from stockPred import *
import time
import yfinance as yf
import matplotlib.pyplot as plt
import os
# from stockListCleaner import *
from alapacaAPI import limitTakeProfitStopLoss as putOrder
from alapacaAPI import ChangeOrderStatus as orderStatus, accountValue, getBuyOrder
from UI import inputUI
import tkinter as tk
from tkinter import ttk
import random
import threading
import random
import yfinance as yf
from alapacaAPI import ChangeOrderStatus as orderStatus, getOrderId, orderDetails, orderPrice, setSecret
from tradingStrat import strat
from stockPred import doAnalysis
from stockListCleaner import cleaner


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
    print(last5)
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
    key, secret = inputui.getSecret()
    if inputui.Cont.get():
        sellList = inputui.cont(key, secret)
    setSecret(key, secret)
botInfoRead.close()


def run_bot():
    global sellList, goodForBuy, last5, money, buySuspended
    if money>0 and (not buySuspended):
        try:
            cleaner()
            doAnalysis()
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
        print(e)


def buy():
    retry = 0
    global goodForBuy, last5, sellList, money, timeoutForBuy, buySuspended, suspensionReason
    mon = 0
    if int(money)<=0:
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
                        print("Sanity check", sellPrice, stockBought, shares, sellNegative, buyPrice)
                        status, orderId = putOrder(stockBought, shares, round(low, 2), sellNegative, sellPrice)
                        if status == 200:
                            print("sell price", sellPrice, "buy price", buyPrice, "Shares ", shares)
                            bought = True
                            sellList.append([stockBought, shares])
                            updateLastOrder(stockBought)
                            money -= mon
                            retry = 0
                            break
                        elif(status == 500 and orderId=="timeout"):
                            timeoutForBuy = 24*3600 + time.time()
                            retry +=1
                    time.sleep(1)
                except Exception as e:
                    suspensionReason = e
                    print(e)


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
                    orderPrice = getBuyOrder(stock[2]['buy'])
                    #Just to give enough time to ping
                    stockBought = stock[0]
                    shares = stock[1]
                    high, sellPrice = orderDetails(stockBought,limit_orderId)
                    value = shares*high
                    print("stock Bought", stockBought, "current price", high, "sell price", sellPrice, "value ", value, "P/L",high-orderPrice, "net value:", accountValue())
                else:
                    print("unbought", stock[0])
                limit_status = orderStatus(limit_orderId)
                stop_status = orderStatus(stop_orderId)
                if limit_status == 'filled':
                    # remove the order from the list, update the money, and update file
                    sellList.pop(sellList.index(stock))
                    money += high * shares
                    botInfoWrite = open("botinfo.txt", 'w')
                    botInfoWrite.write(
                        "bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = " + str(
                            money) + "\nvalue = 0 " + "\norderId = 0")
                    botInfoWrite.close()
                elif stop_status == "filled":
                    sellList.pop(sellList.index(stock))
                    money += high * shares
            else:
                getOrderId(stock[0], stock)
        except Exception as e:
            print("error occured", e)



while float(accountValue())>0.0:
    run_bot()
    time.sleep(60)