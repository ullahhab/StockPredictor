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

last5 = [0, 0, 0, 0, 0]
goodForBuy = []
counter = 0
sellList = []
buyList = []


def seperate(value):
    return value.split("=")[1].strip(" ")


if not (os.path.exists('./botinfo.txt')):
    file = open('botinfo.txt', 'w')
    file.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = 100\nvalue = 0 ")
    file.close()


# if not(os.path.exists('./tmpFile.txt')):
# print("file doesn't exist")
# run()

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
    setSecret(key, secret)
    print(money)
botInfoRead.close()


def run_bot():
    global sellList, goodForBuy, last5

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
    try:
        doAnalysis()
        analyze()
    except Exception as e:
            print(e)
    global goodForBuy, last5, sellList, money
    mon = 0
    buyingPower = strat(money)
    if int(buyingPower)>0:
        mon = money/buyingPower
    else:
        buyingPower = 0
    for bp in range(buyingPower):
        randomList = []
        if int(bp)>0:
            for stock in goodForBuy:
                    try:
                        num = random.randint(0, len(goodForBuy)-1)
                        while num in randomList and goodForBuy[num] in last5:
                            num = random.randint(0, len(goodForBuy)-1)
                        stock = goodForBuy[num]
                        #ticker = yf.download(stock[0], period='1d', interval='1m', progress=False)
                        #low = float(ticker.iloc[-1]['Close'])
                        low = orderPrice(stock[0])
                        print(stock[0], low)
                        if round(float(stock[2]), 2) >=low:
                            print("stock",stock[0],"stock buy Price",stock[2], "Current Stock Price", low, "Value", mon)
                            buyPrice = low
                            sellPrice = round((low+(float(stock[1])/2)),2)
                            stockBought = stock[0]
                            shares = mon // low
                            sellNegative = round((buyPrice - (buyPrice * 0.07)), 2)
                            print("Sanity check", sellPrice, stockBought, shares, sellNegative, buyPrice)
                            status, orderId = putOrder(stockBought, shares, round(low, 2), sellNegative, sellPrice)
                            if status == 200:
                                #botInfoWrite = open("botinfo.txt", 'w')
                                print("sell price", sellPrice, "buy price", buyPrice, "Shares ", shares)
                                #botInfoWrite.write("bought = True\nstockBought = "+str(stockBought)+"\nbuyPrice = " +str(low)+"\nsellPrice = "+str(sellPrice)+"\nshares = "+str(shares)+"\nmoney = "+str(mon)+"\nvalue ="+str(value)+"\norderId ="+str(orderId)+'\n')
                                #botInfoWrite.close()
                                bought = True
                                sellList.append([stockBought, shares])
                                updateLastOrder(stockBought)
                                money = money - mon
                                print("money left", money)
                                break
                        time.sleep(1)
                    except Exception as e:
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


tradingHourStart = datetime.now().replace(hour=7, minute=30).strftime("%H:%M")
tradingHourEnd = datetime.now().replace(hour=19, minute=50).strftime("%H:%M")
analysisTimeStart = datetime.now().replace(hour=6, minute=10).strftime("%H:%M")
analysisTimeEnd = datetime.now().replace(hour=6, minute=30).strftime("%H:%M")
analyzeTimeStart = datetime.now().replace(hour=7, minute=15).strftime("%H:%M")
analyzeTimeEnd = datetime.now().replace(hour=7, minute=17).strftime("%H:%M")
hasPrinted = False
print("stop loss price", sellNegative, "Sell positive", sellPrice)


while float(accountValue())>0.0:
    current_time = datetime.now().strftime("%H:%M")
    is_saturday = datetime.now().weekday() == 5
    is_sunday = datetime.now().weekday() == 6
    if current_time >= tradingHourStart and current_time < tradingHourEnd and not (is_saturday or is_sunday):
        hasPrinted = False
        run_bot()
    else:
        if not (hasPrinted):
            print("non trading hours/day")
            hasPrinted = True
    time.sleep(60)
