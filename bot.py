from datetime import datetime
from stockPred import *
import time
import yfinance as yf
import matplotlib.pyplot as plt
import os
#from stockListCleaner import *
from alapacaAPI import limitTakeProfitStopLoss as putOrder
from alapacaAPI import ChangeOrderStatus as orderStatus
from UI import inputUI
import tkinter as tk
from tkinter import ttk
import random

last5 = [0,0,0,0,0]
goodForBuy = []
counter = 0

def seperate(value):
    return value.split("=")[1].strip(" ")

if not(os.path.exists('./botinfo.txt')):
    file = open('botinfo.txt', 'w')
    file.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = 100\nvalue = 0 ")
    file.close()
#if not(os.path.exists('./tmpFile.txt')):
    #print("file doesn't exist")
    #run()

def updateLastOrder(order):
    global last5, counter
    if counter >= 5:
        counter=0
    last5[counter] = order
    counter+=1

botInfoRead = open('botinfo.txt', 'r')
botInfo = botInfoRead.read().split('\n')
bought = botInfo[0].split('=')[1].strip(" ")=="True"
if bought:
    stockBought = seperate(botInfo[1])
    buyPrice = float(seperate(botInfo[2]))
    sellPrice = float(seperate(botInfo[3]))
    sellNegative = buyPrice-(buyPrice*0.1)
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
    print(money)
botInfoRead.close()
def run_bot():
    global bought, buyPrice, sellPrice, stockBought, money, shares, value,sellNegative, orderId, last5
    if bought:
        try:
                ticker = yf.download(stockBought, period='5d', interval='1m', progress=False)
                high = float(ticker.iloc[-1]['Close'])
                value = shares*high
                '''if sellPrice<= high or sellNegative>=high:
                    botInfoWrite = open("botinfo.txt", 'w')
                    money = shares * high
                    stockBought = ""
                    bought = False
                    buyPrice = 0
                    sellPrice = 0
                    botInfoWrite.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = "+ str(money) +"\nvalue = 0 ")
                    botInfoWrite.close()
                else:'''
                print("stock Bought", stockBought, "current price", high, "sell price", sellPrice, "Volume", ticker.iloc[-1]['Volume'], "Stop loss price",sellNegative,"value ", value)
                if orderStatus(orderId):
                    botInfoWrite = open("botinfo.txt", 'w')
                    botInfoWrite.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = "+ str(money) +"\nvalue = 0 "+"\norderId = 0")
                    botInfoWrite.close()
                    bought = False
                    
        except Exception as e:
            print(e)
    else:
        print("Looking for buying options")
        randomList = []
        for stock in goodForBuy:
            try:
                num = random.randint(0, len(goodForBuy)-1)
                while num in randomList and goodForBuy[num] in last5:
                    num = random.randint(0, len(goodForBuy)-1)
                stock = goodForBuy[num]
                ticker = yf.download(stock[0], period='1d', interval='1m', progress=False)
                low = float(ticker.iloc[-1]['Close'])
                print(stock[0], low)
                if round(float(stock[2]), 2) >=low:
                    print("stock",stock[0],"stock buy Price",stock[2], "Current Stock Price", low, "Value", money)
                    buyPrice = low
                    sellPrice = round((low+(float(stock[1])/2)),2)
                    stockBought = stock[0]
                    shares = money // low
                    sellNegative = round((buyPrice - (buyPrice * 0.07)), 2)
                    print("Sanity check", sellPrice, stockBought, shares, sellNegative, buyPrice)
                    status, orderId = putOrder(stockBought, shares, round(low, 2), sellNegative, sellPrice)
                    print(status)
                    if status == 200:
                        botInfoWrite = open("botinfo.txt", 'w')
                        print("sell price", sellPrice, "buy price", buyPrice, "Shares ", shares)
                        botInfoWrite.write("bought = True\nstockBought = "+str(stockBought)+"\nbuyPrice = " +str(low)+"\nsellPrice = "+str(sellPrice)+"\nshares = "+str(shares)+"\nmoney = "+str(money)+"\nvalue ="+str(value)+"\norderId ="+str(orderId)+'\n')
                        botInfoWrite.close()
                        bought = True
                        updateLastOrder(stockBought)
                        break
            except Exception as e:
                print(e)
        
        


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



tradingHourStart = datetime.now().replace(hour=7, minute=30).strftime("%H:%M")
tradingHourEnd = datetime.now().replace(hour=19, minute=50).strftime("%H:%M")
analysisTimeStart = datetime.now().replace(hour=6, minute=10).strftime("%H:%M")
analysisTimeEnd = datetime.now().replace(hour=6, minute=30).strftime("%H:%M")
analyzeTimeStart = datetime.now().replace(hour=7, minute=15).strftime("%H:%M")
analyzeTimeEnd = datetime.now().replace(hour=7, minute=17).strftime("%H:%M")
hasPrinted = False
print("stop loss price", sellNegative, "Sell positive", sellPrice)

#doAnalysis()
analyze()

while True:
    current_time = datetime.now().strftime("%H:%M")
    is_saturday = datetime.now().weekday() == 5
    is_sunday = datetime.now().weekday() == 6
    if current_time >= tradingHourStart and current_time < tradingHourEnd and not(is_saturday or is_sunday):
        run_bot()
        hasPrinted = False
    else:
        if not(hasPrinted):

            print("non trading hours/day")
            hasPrinted = True
    if current_time >= analysisTimeStart and current_time < analysisTimeEnd:
        print("doing analysis")
        try:
            doAnalysis()
        except Exception as e:
            print(e)
        finally:
            if bought:
                file = open('stocks.csv', 'r')
                header = file.readline()
                fileR = file.read().split('\n')
                for line in fileR:
                    line = line.split(',')
                    if line[0].strip(" ") == stockBought:
                        sellPrice = (float(line[1])/2)+buyPrice
                        print(sellPrice)
    if current_time >= analyzeTimeStart and current_time < analyzeTimeEnd:
        print("Analyzing stock")
        try:
            analyze()
        except Exception as e:
            print(e)
    time.sleep(60)
