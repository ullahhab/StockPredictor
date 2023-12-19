import yfinance as yf
from tqdm import tqdm
stocklst = open("stocks.csv", 'r')
stocklst.readline()
stocklstP = stocklst.read().split("\n")
manualAnalyzer = open("manualAnalysis.csv", 'w')
manualAnalyzer.write("Stock, Daily Change, avg low, avg high, Weekly Change, percentage Profit, Highest, Lowest, Daily Average Price, RSI, Rating, Current Price\n")
with tqdm(total=len(stocklstP), desc="Analysing Stocks") as pbar:
        try:
            for line in stocklstP:
                stock = line.split(",")
                if float(stock[11]) > 5.0:
                      manualAnalyzer.write(line+'\n')
                pbar.update(1)
        except Exception as e:
              print(e)
              pbar.update(1)

manualAnalyzer.close()
stocklst.close()
              
            
                 
