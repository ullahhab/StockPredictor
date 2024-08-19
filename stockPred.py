import yfinance as yf
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import random

stocklst = ''


#msft = yf.Ticker("msft")

#print(msft.download(period="1mo"))
data = ""


def getSymbl():
    global stocklst
    file = open('tmpFile.txt', 'r')
    file.readline()
    read = file.read()
    read = read.split('\n')
    for line in read:
        #stocklst.append(line.split(',')[0])
        stocklst +=line.split(',')[0]+" "
    file.close()
        

def getTicker():
    global data, stocklst
    file  = open('stocks.csv','w')
    file.write("Stock, Daily Change, avg low, avg high, Weekly Change, percentage Profit, Highest, Lowest, Daily Average Price, RSI, Rating, Current Price\n")
    getSymbl()
    """for symbl in stocklst:
        ticker = yf.Ticker(symbl)
        test = ticker.history(period='1mo')
        print(test)
        print(ticker.history(period='1mo'))
    """
    stocklstP = stocklst.split()
    total = len(stocklstP)
    onePerc = int(total*0.01)
    print(onePerc, total)
    counter = 1
    perc = 0
    with tqdm(total=len(stocklstP), desc="Analysing Stocks") as pbar:
        for stock in stocklstP:
            try:
                if '^' in stock:
                    stock = stock[:stock.index("^")]
                data = yf.download(stock, period='5d', progress=False)
                if len(data) == 0:
                    print(data)
                counter+=1
                dailyavgChange = 0
                weeklyavgChange = 0
                dailyCount = 0
                weeklyCount = 0
                weekend = 0
                weeklyInd = 0
                avglow = 0
                avghigh = 0
                lowest = 0
                highest = 0
                dailyAvgPrice = 0
                add = True
                weeklyPrice = 0
                weeklyAvgPrice = 0
                prev = 1
                positive = []
                negative = []
                for date, row in data.iterrows():
                    if(add):
                        lowest = row['Low']
                        highest = row['High']
                        add = False
                    dailyavgChange += abs(row['High'] - row['Low'])
                    weekend += abs(row['High']- row['Low'])
                    avglow += row['Low']
                    avghigh += row['High']
                    dailyAvgPrice+= row['Close']
                    weeklyPrice +=row['Close']
                    if(row['High']> highest):
                        highest = row['High']
                    if(row['Low']< lowest):
                        lowest = row['Low']                   
                    if weeklyInd % 5==0:
                        weeklyCount+=1
                        weeklyavgChange+= (weekend/5)
                        weeklyAvgPrice+=(weeklyPrice/5)
                        weekend = 0
                        weeklyPrice = 0
                    dailyCount+=1
                    if (row['Close']- prev <0):
                        negative.append(abs(row['Close']-prev) /prev)
                    else:
                        positive.append((row['Close']-prev) / prev)
                    prev = row['Close']
                dailyavgChange = dailyavgChange/dailyCount
                dailyAvgPrice = dailyAvgPrice/dailyCount
                avglow = avglow/dailyCount
                avghigh = avghigh/dailyCount
                #RSI = 100 - [100 / (1 + RS)]
                if dailyCount ==0 or sum(positive) == 0:
                    RSI = 0
                elif sum(negative) == 0: 
                    RSI = 100
                else:
                    RSI = 100 - (100 / (1+ ((sum(positive) / dailyCount)/(sum(negative)/ dailyCount))))
                if RSI < 30:
                    Rating = "Oversold"
                elif RSI > 80:
                    Rating = "OverBought"
                else:
                    Rating = "Normal"
                if dailyavgChange / row['Low'] >= 0.05 and row['Close'] > 0.5:
                    file.write(stock+", "+str(dailyavgChange)+", "+str(avglow)+", "+str(avghigh)+", "+str(weeklyavgChange)+", "+str((dailyavgChange / row['Low'])*100)+", "+str(highest)+", "+str(lowest)+", "+str(dailyAvgPrice)+", "+str(RSI)+", "+str(Rating)+", "+str(row['Close'])+"\n")
            except Exception as e:
                print(e)
            finally:
                pbar.update(1)
    file.close()
        

def doAnalysis():
    global data, stocklst
    getTicker()
    file = open("stocks.csv", 'r')
    header = file.readline()
    rest = file.read()
    rest = rest.split('\n')
    initial = 500.0
    stockSugg = open("StockSuggestion.csv", 'w')
    stockSugg.write("Stock, buy price, sell price, percentage increase, Current Price, Rating\n")
    for i in range(54):
        stock = random.randint(1, len(rest)-2)
        stock = rest[stock].split(",")
        initial+= (initial // float(stock[2])) * float(stock[3])
        if i%2==0:
            initial+=500
        stockSugg.write(stock[0]+", "+stock[2]+", "+stock[3]+", "+stock[5]+", "+stock[11]+", "+stock[10]+'\n')
    stockSugg.write("Total = "+str(initial/1000000)+"million\n")
    file.close()
    stockSugg.close()
    stocklst = ''
    data = ""

def getSingleTicker(symbol):
    global data, stocklst
    file  = open('stocks.csv','w')
    file.write("Stock, Daily Change, avg low, avg high, Weekly Change, percentage Profit, Highest, Lowest, Daily Average Price, RSI, Rating, Current Price\n")
    getSymbl()
    """for symbl in stocklst:
        ticker = yf.Ticker(symbl)
        test = ticker.history(period='1mo')
        print(test)
        print(ticker.history(period='1mo'))
    """
    stock = symbol
    counter = 1
    try:
        if '^' in stock:
            stock = stock[:stock.index("^")]
        data = yf.download(stock, period='5d', progress=False)
        if len(data) == 0:
            print(data)
        counter+=1
        dailyavgChange = 0
        weeklyavgChange = 0
        dailyCount = 0
        weeklyCount = 0
        weekend = 0
        weeklyInd = 0
        avglow = 0
        avghigh = 0
        lowest = 0
        highest = 0
        dailyAvgPrice = 0
        add = True
        weeklyPrice = 0
        weeklyAvgPrice = 0
        prev = 1
        positive = []
        negative = []
        for date, row in data.iterrows():
            if(add):
                lowest = row['Low']
                highest = row['High']
                add = False
            dailyavgChange += abs(row['High'] - row['Low'])
            weekend += abs(row['High']- row['Low'])
            avglow += row['Low']
            avghigh += row['High']
            dailyAvgPrice+= row['Close']
            weeklyPrice +=row['Close']
            if(row['High']> highest):
                highest = row['High']
            if(row['Low']< lowest):
                lowest = row['Low']                   
            if weeklyInd % 5==0:
                weeklyCount+=1
                weeklyavgChange+= (weekend/5)
                weeklyAvgPrice+=(weeklyPrice/5)
                weekend = 0
                weeklyPrice = 0
            dailyCount+=1
            if (row['Close']- prev <0):
                negative.append(abs(row['Close']-prev) /prev)
            else:
                positive.append((row['Close']-prev) / prev)
            prev = row['Close']
        dailyavgChange = dailyavgChange/dailyCount
        dailyAvgPrice = dailyAvgPrice/dailyCount
        avglow = avglow/dailyCount
        avghigh = avghigh/dailyCount
        #RSI = 100 - [100 / (1 + RS)]
        if dailyCount ==0 or sum(positive) == 0:
            RSI = 0
        elif sum(negative) == 0: 
            RSI = 100
        else:
            RSI = 100 - (100 / (1+ ((sum(positive) / dailyCount)/(sum(negative)/ dailyCount))))
        if RSI < 30:
            Rating = "Oversold"
        elif RSI > 80:
            Rating = "OverBought"
        else:
            Rating = "Normal"
        #file.write(stock+", "+str(dailyavgChange)+", "+str(avglow)+", "+str(avghigh)+", "+str(weeklyavgChange)+", "+str((dailyavgChange / row['Low'])*100)+", "+str(highest)+", "+str(lowest)+", "+str(dailyAvgPrice)+", "+str(RSI)+", "+str(Rating)+", "+str(row['Close'])+"\n")
        return stock, dailyavgChange, avglow, avghigh, weeklyavgChange, (dailyavgChange / row['Low'])*100, highest, lowest, dailyavgChange, RSI, Rating, row['Close']
    except Exception as e:
        print(e)
    file.close()


#doAnalysis()