import yfinance as yf
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
    for stock in stocklst:
        try:
            if counter % onePerc ==0:
                perc+=1
                print(perc)
            if '^' in stock:
                stock = stock[:stock.index("^")]
            data = yf.download(stock, period='1mo', progress=False)
            counter+=1
        except Exception as e:
            #print(e)
            continue

def doAnalysis():
    getTicker()
    for stock in data:
        print(stock)
        print('\n\n ***************New Stock****************** \n')

doAnalysis()
