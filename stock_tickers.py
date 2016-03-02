## Author == TVS
## Build == 1/5/2016

from googlefinance import getQuotes
from yahoo_finance import Share
import json
import os
import ast
import time
import sys
from tabulate import tabulate

stocklist = ['DOW', 'HOV', 'PHM', 'AMD', 'AMZN', 'AAPL', 'ALU', 'CSCO', 'HPQ', 'MSFT', \
             'T', 'INTC', 'VZ', 'YHOO', 'GM', 'F', 'TTM', 'CVS', 'RAD', 'MGI', 'VG', \
             'WMT', 'JBLU', 'LUV', 'MCD', 'REV', 'BAC', 'C', 'WM', 'ETFC', 'RY', 'PFE', \
             'JNJ', 'PG', 'CL', 'UL', 'XOM', 'CVX', 'VLO', 'LEN', 'PGH', 'FRP', 'NOK', 'BCS']

stocklist.sort()
market = True
today = time.ctime().split(" ")[0]
yahoo_dict = {}
logfile = open(r'i:\Downloads\Python\Scripts\stock_ticker_log.log', 'a')

for stock in stocklist:
    try:
        yahoo_dict[stock] = Share(stock)
    except AttributeError as a:
        print >> logfile, "{0}: {1}: AttributeError: {2}".format(time.ctime(), "get_stock", a.message)
    
while market:
    try:
        stock_table = []
        tickers = ast.literal_eval(json.dumps(getQuotes(stocklist)))

        for tick in tickers:
            instr = tick["StockSymbol"]
            try:
                yahoo_dict[instr].refresh()
            except AttributeError as a:
                print >> logfile, "{0}: {1}: AttributeError: {2}".format(time.ctime(), "refr_stock", a.message)
                
            stock_table.append([tick["StockSymbol"], tick["LastTradePrice"],\
                                yahoo_dict[instr].get_open(), yahoo_dict[instr].get_days_low(), \
                                yahoo_dict[instr].get_days_high(), \
                                tick["LastTradeDateTime"].replace("T", " ").replace("Z", "")])

        headers = ["Ticker", "Last Trade ($)", "Day Open", \
                   "Day Low", "Day High", "Last Trade Time"]    
        os.system("cls")
        print "The ticker is printed at %s" %time.ctime()
        print tabulate(stock_table, headers, tablefmt="simple")

        time.sleep(30)
        currtime = int((time.ctime().split(" ")[3]).split(":")[0])
        if currtime >= 16 or currtime < 9 or today in ['Sat', 'Sun']:
            market = False
    except KeyboardInterrupt:
        logfile.close()
        sys.exit(0)

logfile.close()
os.system("pause")

