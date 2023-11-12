from datetime import datetime
from stockPred import *
import time
import yfinance as yf
bought = False
stockBought = ""
goodForBuy = []
buyPrice = 0
sellPrice = 0
shares = 0
money = 100

def run_bot():
    global bought, buyPrice, sellPrice, stockBought, money, shares
    if bought:
        try:
                ticker = yf.download(stockBought, period='1d', interval='1m', progress=False)
                high = float(ticker.iloc[-1]['Adj Close'])
                if sellPrice>= high:
                    money = shares * sellPrice
                    stockBought = ""
                    bought = False
                    buyPrice = 0
                    sellPrice = 0
        except Exception as e:
            print(e)
    else:
        current_time = datetime.now().strftime("%H:%M")
        #if current_time >= "7:00" and current_time<"7:03":
        analyze()
        for stock in goodForBuy:
            try:
                ticker = yf.download(stock[0], period='1d', interval='1m', progress=False)
                low = float(ticker.iloc[-1]['Adj Close'])
                if float(stock[2])>=low:
                    print("stock buy Price",stock[2], "Current Stock Price", low)
                    bought = True
                    buyPrice = low
                    sellPrice = low+float(stock[1])
                    stockBought = stock[0]
                    shares = money / low
                    print("sell price", sellPrice, "buy price", buyPrice, "Shares ", shares)
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
                print(stock)
    except Exception as e:
        print(e)

        

while True:
    current_time = datetime.now().strftime("%H:%M")
    #if current_time >= "8:30" and current_time < "15:30":
    run_bot()
    #if current_time == "5:00" and current_time<"6:00":
        #doAnalysis()
    time.sleep(60)
