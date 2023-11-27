from datetime import datetime
from stockPred import *
import time
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
from stockListCleaner import *

goodForBuy = []

def seperate(value):
    return value.split("=")[1].strip(" ")

if not(os.path.exists('./botinfo.txt')):
    file = open('botinfo.txt', 'w')
    file.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = 100\nvalue = 0 ")
    file.close()
if not(os.path.exists('./tmpFile.txt')):
    run()

botInfoRead = open('botinfo.txt', 'r')
botInfo = botInfoRead.read().split('\n')
bought = botInfo[0].split('=')[1].strip(" ")=="True"
if bought:
    stockBought = seperate(botInfo[1])
    buyPrice = float(seperate(botInfo[2]))
    sellPrice = float(seperate(botInfo[3]))
    shares = float(seperate(botInfo[4]))
    money = float(seperate(botInfo[5]))
    value = float(seperate(botInfo[6]))
else:
    stockBought = ""
    buyPrice = 0
    sellPrice = 0
    shares = 0
    money = float(seperate(botInfo[5]))
    value = 0
botInfoRead.close()
def run_bot():
    global bought, buyPrice, sellPrice, stockBought, money, shares, value
    if bought:
        try:
                ticker = yf.download(stockBought, period='5d', interval='1m', progress=False)
                high = float(ticker.iloc[-1]['Close'])
                value = shares*high
                if sellPrice<= high:
                    botInfoWrite = open("botinfo.txt", 'w')
                    money = shares * high
                    stockBought = ""
                    bought = False
                    buyPrice = 0
                    sellPrice = 0
                    botInfoWrite.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = "+ str(money) +"\nvalue = 0 ")
                    botInfoWrite.close()
                else:
                    print("stock Bought", stockBought, "current price", high, "sell price", sellPrice, "Volume", ticker.iloc[-1]['Volume'], "value ", value)
        except Exception as e:
            print(e)
    else:
        print("Looking for buying options")
        for stock in goodForBuy:
            try:
                ticker = yf.download(stock[0], period='1d', interval='1m', progress=False)
                low = float(ticker.iloc[-1]['Close'])
                print(stock[0], low)
                if float(stock[2])>=low:
                    botInfoWrite = open("botinfo.txt", 'w')
                    print("stock",stock[0],"stock buy Price",stock[2], "Current Stock Price", low, "Value", money)
                    bought = True
                    buyPrice = low
                    sellPrice = low+(float(stock[1])/2)
                    stockBought = stock[0]
                    shares = money / low
                    print("sell price", sellPrice, "buy price", buyPrice, "Shares ", shares)
                    botInfoWrite.write("bought = True\nstockBought = "+str(stockBought)+"\nbuyPrice = " +str(low)+"\nsellPrice = "+str(sellPrice)+"\nshares = "+str(shares)+"\nmoney = "+str(money)+"\nvalue ="+str(value)+'\n')
                    botInfoWrite.close()
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
tradingHourEnd = datetime.now().replace(hour=15, minute=30).strftime("%H:%M")
analysisTimeStart = datetime.now().replace(hour=6, minute=10).strftime("%H:%M")
analysisTimeEnd = datetime.now().replace(hour=6, minute=30).strftime("%H:%M")
analyzeTimeStart = datetime.now().replace(hour=7, minute=15).strftime("%H:%M")
analyzeTimeEnd = datetime.now().replace(hour=7, minute=17).strftime("%H:%M")
hasPrinted = False


doAnalysis()
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
                    print(line)
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
