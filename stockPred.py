import yfinance as yf
stocklst = ''

#msft = yf.Ticker("msft")

#print(msft.download(period="1mo"))

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
    getSymbl()
    """for symbl in stocklst:
        ticker = yf.Ticker(symbl)
        test = ticker.history(period='1mo')
        print(test)
        print(ticker.history(period='1mo'))
    """
    data = yf.download(stocklst[:len(stocklst)-2], period='1mo')
    
getTicker()
