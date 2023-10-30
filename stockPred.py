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
    file = open('stocksList.csv', 'r')
    file.readline()
    read = file.read()
    read = read.split('\n')
    for line in read:
        #stocklst.append(line.split(',')[0])
        stocklst +=line.split(',')[0]+" "
        

def getTicker():
    global data, stocklst
    file  = open('stocks.csv','w')
    file.write("Stock, Daily Change, avg low, avg high, Weekly Change, percentage Profit, Highest, Lowest\n")
    getSymbl()
    """for symbl in stocklst:
        ticker = yf.Ticker(symbl)
        test = ticker.history(period='1mo')
        print(test)
        print(ticker.history(period='1mo'))
    """
    stocklst = stocklst.split()
    total = len(stocklst)
    onePerc = int(total*0.01)
    print(onePerc, total)
    counter = 1
    perc = 0
    with tqdm(total=len(stocklst), desc="Downloading Stocks") as pbar:
        for stock in stocklst:
            try:
                if '^' in stock:
                    stock = stock[:stock.index("^")]
                data = yf.download(stock, period='6mo', progress=False)
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
                add = True
                for date, row in data.iterrows():
                    if(add):
                        lowest = row['Low']
                        highest = row['High']
                        add = False
                    dailyavgChange += abs(row['High'] - row['Low'])
                    weekend += abs(row['High']- row['Low'])
                    avglow += row['Low']
                    avghigh += row['High']
                    if(row['High']> highest):
                        highest = row['High']
                    if(row['Low']< lowest):
                        lowest = row['Low']                   
                    if weeklyInd % 5==0:
                        weeklyCount+=1
                        weeklyavgChange+= (weekend/5)
                        weekend = 0
                    dailyCount+=1
                    dailyavgChange = dailyavgChange/dailyCount
                    if dailyavgChange / row['Low'] >= 0.15:
                        file.write(stock+", "+str(dailyavgChange)+", "+str(avglow)+", "+str(avghigh)+", "+str(weeklyavgChange)+", "+str((dailyavgChange / row['Low'])*100)+", "+str(highest)+", "+str(lowest)+"\n")                       
            except Exception as e:
                print(e)
            finally:
                pbar.update(1)
    file.close()
        

def doAnalysis():
    getTicker()
    file = open("stocks.csv", 'r')
    header = file.readline()
    rest = file.read()
    rest = rest.split('\n')
    initial = 500.0
    stockSugg = open("StockSuggestion.csv", 'w')
    stockSugg.write("Stock, buy price, sell price, percentage increase\n")
    for i in range(54):
        stock = random.randint(1, len(rest)-1)
        stock = rest[stock].split(",")
        initial+= (initial // float(stock[2])) * float(stock[3])
        if i%2==0:
            initial+=500
        stockSugg.write(stock[0]+", "+stock[2]+", "+stock[3]+", "+stock[5]+'\n')
    stockSugg.write("Total = "+str(initial/1000000)+"million\n")




doAnalysis()
