import threading
import random
import yfinance as yf
from bot import updateLastOrder
from alapacaAPI import putOrder, ChangeOrderStatus as orderStatus, getOrderId
from tradingStrat import strat

def buy(num, goodForBuy, last5, sellList, money):
    buyList = []
    buyingPower = strat(money)
    mon = money//buyingPower
    for bp in range(len(buyingPower)):
        if bp==len(money)-1:
            mon = money - (mon*bp)
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
                        print("stock",stock[0],"stock buy Price",stock[2], "Current Stock Price", low, "Value", mon)
                        buyPrice = low
                        sellPrice = round((low+(float(stock[1])/2)),2)
                        stockBought = stock[0]
                        shares = mon // low
                        sellNegative = round((buyPrice - (buyPrice * 0.07)), 2)
                        print("Sanity check", sellPrice, stockBought, shares, sellNegative, buyPrice)
                        status, orderId = putOrder(stockBought, shares, round(low, 2), sellNegative, sellPrice)
                        print(status)
                        if status == 200:
                            botInfoWrite = open("botinfo.txt", 'w')
                            print("sell price", sellPrice, "buy price", buyPrice, "Shares ", shares)
                            botInfoWrite.write("bought = True\nstockBought = "+str(stockBought)+"\nbuyPrice = " +str(low)+"\nsellPrice = "+str(sellPrice)+"\nshares = "+str(shares)+"\nmoney = "+str(mon)+"\nvalue ="+str(value)+"\norderId ="+str(orderId)+'\n')
                            botInfoWrite.close()
                            bought = True
                            sellList.append([stockBought, shares])
                            updateLastOrder(stockBought)
                            money = money - mon
                            break
                except Exception as e:
                    print(e)
    return money



def sell(sellList, shares):
    #two possibilities if the stock is on hold or acutually excecuted. Either way just look for order id or stockBought for sell order
    for stock in sellList:
        try:
            if len(stock)>=3:
                stockBought = stock[0]
                shares = stock[1]
                orderId = stock[2]
                ticker = yf.download(stockBought, period='5d', interval='1m', progress=False)
                high = float(ticker.iloc[-1]['Close'])
                value = shares*high
                print("stock Bought", stockBought, "current price", high, "sell price", sellPrice, "Volume", ticker.iloc[-1]['Volume'], "Stop loss price",sellNegative,"value ", value)
                if orderStatus(orderId):
                    botInfoWrite = open("botinfo.txt", 'w')
                    botInfoWrite.write("bought = False\nstockBought = \nbuyPrice = 0\nsellPrice = 0\nshares = 0\nmoney = "+ str(money) +"\nvalue = 0 "+"\norderId = 0")
                    botInfoWrite.close()
            else:
                getOrderId(stock[0], stock)
        except Exception as e:
            print(e)
