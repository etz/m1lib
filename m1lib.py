from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import re


                            ###### DEBUGGING ######
#Function: DebugCommand
#Usage: Prints debugging information in the console
#Returns: Debugging information in Python Console
def DebugCommand(string):
    global debug_variable
    debug_variable = 1 #Change me to turn on/off debugging!
    if debug_variable == 1:
        print ("DEBUG: " + string)

#Function: cashOnly()
#Usage: Will only place orders with Cash
#Returns: True/False
def cashOnly(status):
    pass
    #Check cash balance
    #Compare cash versus order amount
    #Return True or False


                            ###### AUTH ######


#Function: login(user,pass)
#Usage: Initalizes Chrome & logs into the associated M1 Finance account
#Returns: True if successful
def login(m1user, m1pass):
    DebugCommand("Beginning User Login")
    global driver
    #Initalize Chromedriver
    chromeOptions = webdriver.ChromeOptions()
    capabilities=webdriver.DesiredCapabilities.CHROME
    driver= webdriver.Chrome(options=chromeOptions,desired_capabilities=capabilities)
    #Navigate to M1
    url = "https://dashboard.m1finance.com/login"
    driver.get(url)
    #Allow time to load
    time.sleep(4)
    #Send user credentials
    usernameField = driver.find_element_by_name("username")
    usernameField.send_keys(m1user)
    pwField = driver.find_element_by_name("password")
    pwField.send_keys(m1pass)
    #Click Login
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div/div[2]/div/div/form/div[4]/div/button""").click()
    #Allow time to load
    time.sleep(8)
    status = checkLogin()
    return status

#Function: CheckLogin()
#Usage: Verifys if Credentials were used correctly from config.py
#Returns: "0" if properly authenticated
def checkLogin():
    #Check if config.py is empty
    try:
        if (driver.find_element_by_xpath("""//*[@id="root"]/div/div/div/div[2]/div/div/form/div[2]/div/div[1]/div[2]/div""").text == "Required"):
            print("Credentials not filled out. See config.py")
            return False
    except:
        pass
    #Check if Credential login was successful
    try:
        if "Incorrect" in driver.find_element_by_xpath("""//*[@id="root"]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/div""").text:
            print("Credentials incorrect. See config.py")
            return False
    except:
        pass
    return True

#Function: closeSession()
#Usage: Self-explanatory
#Returns:
def closeSession():
    driver.close()


#Function: selectAccount(accType)
#Usage: Selects the account determined in the Config file
#Returns:
def selectAccount(accType):
    DebugCommand("Beginning Account Selection")
    accountType = driver.find_element_by_xpath("""//*[@id="popup22"]/div[1]/h3""").text
    DebugCommand("Current Account:" + str(accountType))
    if accType not in accountType:
        DebugCommand("Selecting Account:" + str(accType))
        driver.find_elements_by_xpath("//*[contains(text(), ' - ')]/../..")[1].click()
        time.sleep(1)
        driver.find_element_by_xpath("""//*[contains(text(), '""" + accType + """')]/..""").click()
        time.sleep(4)
        accountType = driver.find_element_by_xpath("""//*[@id="popup22"]/div[1]/h3""").text
        DebugCommand("Current Account:" + str(accountType))

                            ###### ORDERS ######

#Function: orderPie(amount, pie id)
#Usage: Purchases a M1 Pie based on the USD value (amount) and the pie ID (pid)
#Returns: True if successful
def orderPie(amount, pid):
    print ("Beginning Pie Purchase")
    url = "https://dashboard.m1finance.com/d/c/set-order/" + str(pid)
    driver.get(url)
    time.sleep(8)
    if amount < 0:
        startSell()
        amount = amount * -1
    if amount < 10:
        DebugCommand("Orders under $10 cannot be processed")
        return False
    try:
        usernameField = driver.find_element_by_name("cashFlow")
        usernameField.send_keys(str(amount))
    except:
        DebugCommand("There was an issue with the connection or the element 'cashFlow' could not be found.")
        return False
    confirmOrder()
    if (verifyPie(pid) == True):
        return True

def orderPV(amount, accType):
    pid = getPID(accType)
    orderPie(amount, pid)

#Function: getPID(accType)
#Usage: Gets the Pie ID of a certain account portfolio
#Returns: string
def getPID(accType):
    selectAccount(accType)
    #time.sleep(3)
    try:
        driver.find_element_by_xpath("""//*[contains(text(), 'Buy/Sell')]""").click()
    except:
        DebugCommand("Open order already exists.")
        return 0
    pid = substring_after(driver.current_url, "d/c/set-order/")
    driver.execute_script("window.history.go(-1)")
    time.sleep(5)
    return str(pid)

#Function: initiateDeposit(amount, accType, contributionYear)
#Usage: Deposits into the M1 Finance account (use contributionYear for IRA accounts)
#Returns: True if successful
def initiateDeposit(amount, accType, year=''):
    print ("Beginning Account Deposit")
    #Navigate
    url = "https://dashboard.m1finance.com/d/invest/funding"
    driver.get(url)
    time.sleep(5)
    selectAccount(accType)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[4]/div[1]/a/div/span""").click()
    #Type deposit...
    time.sleep(2)
    depositField = driver.find_element_by_name("amount")
    depositField.send_keys(str(amount))
    if year != '':
        element = driver.find_element_by_name("retirementContributionYear")
        options = element.find_elements_by_tag_name("option")
        for option in options:
            if option.get_attribute("value") == str(year):
                option.click()
    #Confirm deposit...
    try:
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/form/button/div/span""").click()
        time.sleep(3)
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[7]/button[2]/div/span""").click()
    except:
        DebugCommand("There was an error confirming the deposit.")
        return False
    return True

#Function: initiateWithdraw(amount, accType)
#Usage: withdraws from the M1 Finance account
#Returns: True if successful
def initiateWithdraw(amount, accType):
    print ("Beginning Account Withdraw")
    #Navigate
    url = "https://dashboard.m1finance.com/d/invest/funding"
    driver.get(url)
    time.sleep(5)
    selectAccount(accType)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[4]/div[2]/button""").click()
    #Type withdrawal...
    time.sleep(2)
    withdrawField = driver.find_element_by_name("amount")
    withdrawField.send_keys(str(amount))
    #Confirm withdrawal...
    try:
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/form/button""").click()
        time.sleep(3)
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[7]/button[2]/div/span""").click()
        time.sleep(4)
        #Close
        driver.find_element_by_xpath("""//*[@id="cover-close-button"]/span""").click()

    except:
        DebugCommand("There was an error confirming the withdrawal.")
        return False
    return True

#Function: changeAutoInvest(accType, option='', amount='')
#Usage: Use amount only when selecting a set amount to auto-invest over. Changes the auto invest settings against accType
#Returns: True if successful
def changeAutoInvest(accType, option='', amount=''):
    print ("Changing auto-invest feature")
    #Navigate
    url = "https://dashboard.m1finance.com/d/invest/funding"
    driver.get(url)
    time.sleep(5)
    selectAccount(accType)
    if option == "all":
        #Click
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/form/div/label[1]""").click()
        time.sleep(2)
        #Save
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/form/button""").click()
        time.sleep(3)
        return True
    elif option == "set":
        if amount == '':
            DebugCommand("Amount not Set for auto invest method 'set'")
            return False
        #Click
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/form/div/label[2]/div[1]""").click()
        time.sleep(2)
        withdrawField = driver.find_element_by_name("maxCashThreshold")
        withdrawField.send_keys(str(amount))
        #Save
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/form/button""").click()
        time.sleep(3)
        return True
    elif option == "off":
        #Click
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/form/div/label[3]/div[1]""").click()
        time.sleep(2)
        #Save
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/form/button""").click()
        time.sleep(3)
        return True
    elif option == "":
        DebugCommand("Auto Invest Option not selected")
        return False

#Function: searchTicker(ticker)
#Usage: Returns the price, marketcap, PE Ratio, and Dividend Yield of listed M1 Tickers
#Returns: [float(price), float(percent_change), float(div_yield), str(mkcap), float(pe_ratio)]
def searchTicker(ticker):
    url = "https://dashboard.m1finance.com/d/research/watchlist"
    driver.get(url)
    time.sleep(5)
    searchField = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div/div/input""")
    searchField.send_keys(str(ticker) + Keys.ENTER)
    time.sleep(5)
    price_element = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span[1]""")
    list_price = price_element.find_elements_by_tag_name("span")
    price = []
    for number in list_price:
        price.append(number.text)
    price = "".join(price)
    price = float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", price)[0])
    percent_change = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div/div[1]/span[2]/span[1]""").text
    percent_change = float(percent_change.replace("$", ""))
    percent_change = round((percent_change/(price-percent_change)*100), 2)
    #print (price)
    div_yield = float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[3]/div/div/div[3]/div[1]""").text)[0])
    #print (div_yield)
    mkcap = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[3]/div/div/div[1]/div[1]""").text
    #print (mkcap)
    pe_ratio = float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[3]/div/div/div[2]/div[1]""").text)[0])
    #print (pe_ratio)
    return [price, percent_change, div_yield, mkcap, pe_ratio]


#Function: getCurrentMarketData()
#Usage: Returns the % difference in the SPY, DIA, and QQQ tickers in a float
#Returns: float([SPY_DATA, DIA_DATA, QQQ_DATA])
def getCurrentMarketData():
    url = "https://dashboard.m1finance.com/d/research/market-news"
    driver.get(url)
    time.sleep(5)
    SPY = float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div[1]/div[3]/span/span[2]""").text)[0])
    DIA = float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div[3]/span/span[2]""").text)[0])
    QQQ = float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div[1]/div[3]/span/span[2]""").text)[0])
    return [SPY, DIA, QQQ]


#Function: tickerSearch(mk_min='',mk_max='',pe_min='',pe_max='',div_min='',div_max='',sector='',industry='')
#Usage: search m1 fianance's stock or fund database for what is queried
#Returns: list of tickers that match search
def tickerSearch(mk_min='',mk_max='',aum_min='',aum_max='',pe_min='',pe_max='',exp_min='',exp_max='',div_min='',div_max='',sector='',industry=''):
    #Determine Stock
    if mk_min != '' or mk_max != '' or pe_min != '' or pe_max != '':
        if aum_min == '' and aum_max == '' and exp_min == '' and exp_max == '':
            url = "https://dashboard.m1finance.com/d/research/stocks"
            driver.get(url)
            time.sleep(5)
        else:
            DebugCommand("aum_min, aum_max, exp_min, exp_max: one is declared")
            return tickerSearch(mk_min=mk_min,mk_max=mk_max,pe_min=pe_min,pe_max=pe_max,div_min=div_min,div_max=div_max,sector=sector,industry=industry)
    if aum_min != '' or aum_max != '' or exp_min != '' or exp_max != '':
        if mk_min == '' and mk_max == '' and pe_min == '' and pe_max == '':
            url = "https://dashboard.m1finance.com/d/research/funds"
            driver.get(url)
            time.sleep(5)
        else:
            DebugCommand("mk_min, mk_max, pe_min, pe_max: one is declared")
            return tickerSearch(aum_min=aum_min,aum_max=aum_max,exp_min=exp_min,exp_max=exp_max,div_min=div_min,div_max=div_max,sector=sector,industry=industry)
    if sector != '':
        sector_list = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div[5]/div/div""")
        sectors = sector_list.find_elements_by_class_name("style__label__3BGEW")
        sector_list = []
        for sector_item in sectors:
            sector_list.append(sector_item.text)
        #Select Sector
        for sector_item in sector_list:
            if str(sector).lower() in str(sector_item).lower():
                DebugCommand("Selected Sector Succesfully")
                i = sector_list.index(sector_item)
                sectors[i].click()
    if industry != '':
        time.sleep(2.5)
        sector_list = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div[5]/div/div[2]""")
        sectors = sector_list.find_elements_by_class_name("style__label__3BGEW")
        sector_list = []
        for sector_item in sectors:
            sector_list.append(sector_item.text)
        #Select Industry
        for sector_item in sector_list:
            if str(industry).lower() in str(sector_item).lower():
                DebugCommand("Selected Industry Succesfully")
                i = sector_list.index(sector_item)
                sectors[i].click()
    if mk_min != '':
        editField = driver.find_elements_by_name("min")[0]
        editField.send_keys(str(mk_min))
    if mk_max != '':
        editField = driver.find_elements_by_name("max")[0]
        editField.send_keys(str(mk_max))
    if aum_min != '':
        editField = driver.find_elements_by_name("min")[0]
        editField.send_keys(str(aum_min))
    if aum_max != '':
        editField = driver.find_elements_by_name("max")[0]
        editField.send_keys(str(aum_max))
    if pe_min != '':
        editField = driver.find_elements_by_name("min")[1]
        editField.send_keys(str(pe_min))
    if pe_max != '':
        editField = driver.find_elements_by_name("max")[1]
        editField.send_keys(str(pe_max))
    if exp_min != '':
        editField = driver.find_elements_by_name("min")[2]
        editField.send_keys(str(mk_min))
    if exp_max != '':
        editField = driver.find_elements_by_name("max")[2]
        editField.send_keys(str(mk_max))
    if div_min != '':
        if 'stocks' in driver.current_url:
            editField = driver.find_elements_by_name("min")[2]
            editField.send_keys(str(div_min))
        else:
            editField = driver.find_elements_by_name("min")[1]
            editField.send_keys(str(div_min))
    if div_max != '':
        if 'stocks' in driver.current_url:
            editField = driver.find_elements_by_name("max")[2]
            editField.send_keys(str(div_max))
        else:
            editField = driver.find_elements_by_name("max")[2]
            editField.send_keys(str(div_max))[1]
    time.sleep(2)
    results = driver.find_element_by_tag_name("tbody")
    result_list = results.find_elements_by_class_name("style__tableRow__1L9Tk")
    results = []
    for item in result_list:
        tickersymbol = item.find_element_by_tag_name("span").text
        results.append(tickersymbol)
        DebugCommand("Ticker " + str(tickersymbol))

    return results


                            ###### STATUS ######

#Function: verifyPie
#Usage: Checks if an open order is held against pid
#Returns: True/False
def verifyPie(pid):
    DebugCommand("Checking purchase of " + str(pid))
    url = "https://dashboard.m1finance.com/d/invest/portfolio/" + str(pid)
    driver.get(url)
    time.sleep(5)
    try:
        orderCompletion = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/span""").text
        DebugCommand("Order complete")
        return True
    except:
        DebugCommand("Order failed")
        return False


#Function: cancelOrder(pid)
#Usage: Cancels order
#Returns: True/False
def cancelOrder(pid):
    DebugCommand("Cancelling order of " + str(pid))
    url = "https://dashboard.m1finance.com/d/invest/portfolio/" + str(pid)
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/span/a""").click()
        time.sleep(3)
        driver.find_element_by_xpath("""//*[@id="modal-content-9"]/div[2]/div[4]/button[2]""").click()
        DebugCommand("Order cancelled")
        return True
    except:
        DebugCommand("Order failed")
        return False

#Function: rebalancePie(pid)
#Usage: Assigns rebalance
#Returns: True/False
def rebalancePie(pid):
    DebugCommand("Rebalancing Portfolio" + accType)
    url = "https://dashboard.m1finance.com/d/invest/portfolio/" + str(pid)
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[3]/div/button[2]""").click()
        time.sleep(3)
        driver.find_element_by_xpath("""//*[@id="modal-content-11"]/div[2]/div[5]/button[2]""").click()
        time.sleep(5)
        DebugCommand("Rebalance complete")
        return True
    except:
        DebugCommand("Rebalance failed")
        return False

def rebalancePV(accType):
    pid = getPID(accType)
    rebalancePie(pid)


#Function: CheckReturnsPV
#Usage: Provides the percentage return for the account Type
#Returns: % gain as float()
def checkReturnsPV(accType, timeframe):
    DebugCommand("Checking" + timeframe + " returns against: " + str(accType))
    selectAccount(accType)
    selectTimeframe(timeframe)
    time.sleep(3)
    DebugCommand("Returns Check Complete")
    return float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/span/span[2]""").text)[0])

#Function: checkReturnsPie
#Usage: Returns the percentage change over the timeframe for the pie (DOES NOT INCLUDE YOUR HOLDINGS)
#Returns: % gain as float()
def checkReturnsPie(pid, timeframe):
    url = "https://dashboard.m1finance.com/d/invest/portfolio/" + str(pid)
    driver.get(url)
    time.sleep(5)
    DebugCommand("Checking" + timeframe + " returns against: " + str(pid))
    selectTimeframe(timeframe)
    time.sleep(3)
    DebugCommand("Returns Check Complete")
    return float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/span/span[2]""").text)[0])

#Function: selectTimeframe
#Usage: Clicks the timeframe associated with the variable
#Returns:
def selectTimeframe(timeframe):
    if "day" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "week" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[2]""").click()
    elif "month" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[3]""").click()
    elif "quarter" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[4]""").click()
    elif "year" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[5]""").click()
    elif "all" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[6]""").click()
    else:
        DebugCommand("Timeframe not recognized.")

#Function: startSell()
#Usage: Selects the 'sell' button on an order page
#Returns:
def startSell():
    DebugCommand("Selecting Sell")
    SellButton = driver.find_elements_by_xpath("//*[contains(text(), 'Sell')]")
    for element in SellButton:
        try:
            element.click()
        except:
            pass
    time.sleep(2)

#Function: confirmOrder()
#Usage: Completes an opened order after the cashFlow element (amount) has been filled
#Returns:
def confirmOrder():
    DebugCommand("Confirming Order")
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[6]/button[2]""").click()
    time.sleep(3)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[9]/button[2]""").click()
    time.sleep(6)


                            ### INDICATORS/TRADING ###

#Function: orderWeight
#Usage: Returns a weighted value determined on a base and multiplier
#Returns: float()
def orderWeight(base, multiplier):
    if (multiplier > 0):
        multiplier = 1-(multiplier/10)
    else:
        multiplier = (-1*(multiplier/100))+1
    print (str(base))
    print (str(multiplier))
    newValue = float("{0:.2f}".format(base*multiplier))
    print("Base Amount: " + str(base) + "USD, after multiplier: " + str(newValue))
    return newValue

                            ### MUMBO JUMBO ###

#Function: substring_after
#Usage: Splits a string after the 'delim' string
#Returns: 2nd half of split string
def substring_after(s, delim):
    return s.partition(delim)[2] #Thanks StackOverflow
