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
                if sellPrice<= high:
                    money = shares * high
                    stockBought = ""
                    bought = False
                    buyPrice = 0
                    sellPrice = 0
                else:
                    print("current price", high, "sell price", sellPrice)
        except Exception as e:
            print(e)
    else:
        current_time = datetime.now().strftime("%H:%M")
        if current_time >= "7:00" and current_time<"7:03":
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
    except IndexError as e:
        pass
    except Exception as e:
        print(e)

        
analyze()
while True:
    current_time = datetime.now().strftime("%H:%M")
    is_saturday = datetime.now().weekday() == 5
    is_sunday = datetime.now().weekday() == 6
    if current_time >= "20:16" and current_time < "20:30" and not(is_saturday or is_sunday):
        run_bot()
    else:
        print("non trading hours/day")
    if current_time >= "5:00" and current_time<"6:00":
        print("doing analysis")
        doAnalysis()
    time.sleep(60)
