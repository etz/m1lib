from m1lib import *
import config
import datetime


#This script intends to show the m1lib.py file in use.

day = 60*60*24

def checkDay():
    x = datetime.datetime.now()
    if (x.strftime("%a") == "Sat" or x.strftime("%a") == "Sun"):
        DebugCommand("Weekend date, skipping")
        time.sleep(day)
        pass
    else:
        runBot()

def runBot():
    if (login(config.username, config.password) == True):
        DebugCommand("I successfully ran the login function.")
        ticker_results = searchTicker("SPXS")
        print (ticker_results)
        pchange = ticker_results[1]
        if pchange > 0:
            baseorder = 25 * ((-pchange/10)+1)
            baseorder = round(baseorder, 2)
        else:
            baseorder = 25 * ((pchange/10)+1)
            baseorder = round(baseorder, 2)
        DebugCommand(baseorder)
        orderPV(baseorder, "Roth")
    #End your file with...
    closeSession()
    DebugCommand("Bot run complete")
    time.sleep(day)
    checkDay()


while 1 > 0:
    checkDay()
