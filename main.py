import m1lib
import config

#This script intends to show the m1lib.py file in use.

if (m1lib.login(config.username, config.password) == 0):
    m1lib.DebugCommand("I successfully ran the login function.")
    PercentGain = m1lib.CheckDayGain(config.accountType)
    print("My portfolio changed " PercentGain + "% today.")

    #Your magic here... 😄

#m1lib.BuyPortfolio(config.BaseBuy, config.accountType)
m1lib.OrderPie(config.BaseOrder, "Q1BTOjVRTjQyODE1LDYwODE5MCw2MDk5MTc%3D")



#End your file with...
m1lib.closeSession()
