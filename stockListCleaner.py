
import yfinance as yf
def run():
    stocklst = open("stocksList.csv", 'r')
    firtsLine = stocklst.readline()
    newFile = open("tmpFile.txt", 'w')
    stocklst = stocklst.read().split("\n")
    newFile.write(firtsLine)
    for line in stocklst:
        stock = line.split(",")[0]
        try:
            if '^' in stock:
                stock = stock[:stock.index("^")]
            data = yf.download(stock, period='6mo', progress=False)
            if len(data) == 0:
                print("no data")
            else:
                newFile.write(line+"\n")
        except:
            continue
run()