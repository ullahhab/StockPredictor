import yfinance as yf
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
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
    file.write("Stock, Daily Change, avg low, avg high, Weekly Change, percentage Profit\n")
    getSymbl()
    """for symbl in stocklst:
        ticker = yf.Ticker(symbl)
        test = ticker.history(period='1mo')
        print(test)
        print(ticker.history(period='1mo'))
    """
    print(stocklst[:len(stocklst)-2])
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
                for date, row in data.iterrows():
                    #print(row)
                    dailyavgChange += abs(row['High'] - row['Low'])
                    weekend += abs(row['High']- row['Low'])
                    avglow += row['Low']
                    avghigh += row['High']
                    if weeklyInd % 5==0:
                        weeklyCount+=1
                        weeklyavgChange+= (weekend/5)
                        weekend = 0
                    dailyCount+=1
                    dailyavgChange = dailyavgChange/dailyCount
                    if dailyavgChange / row['Low'] >= 0.15:
                        file.write(stock+", "+str(dailyavgChange)+", "+str(avglow)+", "+str(avghigh)+", "+str(weeklyavgChange)+", "+str((dailyavgChange / row['Low'])*100)+"\n")                       
            except Exception as e:
                print(e)
            finally:
                pbar.update(1)
    file.close()
        

def doAnalysis():
    getTicker()

doAnalysis()
