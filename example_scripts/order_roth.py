# Developers Note: All example scripts must be moved up one directory to be used.
# I repeat. This script will not run. Move the file up one folder to sit with "m1lib.py"
import m1lib
import config

#This script intends to show the m1lib.py file in use.
#This script may use deprecated functions or not work as described.

accountType = "Roth"

if (m1lib.login(config.username, config.password) == True):
    m1lib.DebugCommand("I successfully ran the login function.")

    #Order with a base multiplier
    baseOrder = 50
    baseOrder = m1lib.orderWeight(baseOrder, m1lib.checkReturnsPV("Roth", "week"))
    m1lib.orderPV(baseOrder, "Roth") #Buys $50 from "Roth" portfolio based on strength of earnings over past week

    #Order without a multiplier
    #baseOrder = 50
    #m1lib.orderPV(baseOrder, "Roth") #Buys $50 from "Roth" portfolio

#End your file with...
m1lib.closeSession()
