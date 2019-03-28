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
#Returns:
def DebugCommand(string):
    global debug_variable
    #Change me to debug!
    debug_variable = 1
    if debug_variable == 1:
        print ("DEBUG: " + string)


                            ###### AUTH ######


#Function: login(user,pass)
#Usage: Initalizes Chrome & logs into the associated M1 Finance account
#Returns: "0" if login successful
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
            return 1
    except:
        pass
    #Check if Credential login was successful
    try:
        if "Incorrect" in driver.find_element_by_xpath("""//*[@id="root"]/div/div/div/div[2]/div/div/form/div[1]/div/div/div/div""").text:
            print("Credentials incorrect. See config.py")
            return 1
    except:
        pass
    return 0

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
    driver.find_elements_by_xpath("//*[contains(text(), ' - ')]/../..")[1].click()
    accountType = driver.find_elements_by_xpath("//*[contains(text(), ' - ')]")[1].text
    DebugCommand(str(accountType))
    if accType not in accountType:
        driver.find_element_by_xpath("""//*[contains(text(), '""" + accType + """')]/..""").click()
        time.sleep(4)
    time.sleep(2)
    DebugCommand("Account Selected")

                            ###### ORDERS ######

#Function: orderPie(amount, pie id)
#Usage: Purchases a M1 Pie based on the USD value (amount) and the pie ID (pid)
#Returns: True if successful
def orderPie(amount, pid):
    print ("Beginning Pie Purchase")
    url = "https://dashboard.m1finance.com/d/c/set-order/" + pid
    driver.get(url)
    time.sleep(5)
    if amount < 0:
        startSell()
        amount = amount * -1
    if amount < 10:
        DebugCommand("Orders under $10 cannot be processed")
        return False
    try:
        usernameField = driver.find_element_by_name("cashFlow")
        usernameField.send_keys(amount)
    except:
        DebugCommand("There was an issue with the connection or the element 'cashFlow' could not be found.")
        return False
    confirmOrder()
    if (verifyPie(pid) == True):
        return True


                            ###### STATUS ######

#Function: verifyPie
#Usage: Checks if an open order is held against pid
#Returns: True/False
def verifyPie(pid):
    DebugCommand("Checking purchase of " + pid)
    url = "https://dashboard.m1finance.com/d/invest/portfolio/" + pid
    driver.get(url)
    time.sleep(5)
    try:
        orderCompletion = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/span""").text
        DebugCommand("Order complete")
        return True
    except:
        DebugCommand("Order failed")
        return False


#Function: CheckReturnsPV
#Usage: Provides the percentage return for the account Type
#Returns: % gain as float()
def checkReturnsPV(accType, timeframe):
    DebugCommand("Checking" + timeframe + " returns against: " + str(accType))
    selectAccount(accType)
    if "day" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "week" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "month" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "quarter" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "year" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "all" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    else:
        DebugCommand("Timeframe not recognized.")
        return 0
    time.sleep(3)
    DebugCommand("Returns Check Complete")
    return float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/span/span[2]""").text)[0])


#Function: checkReturnsPie
#Usage: Returns the percentage change over the timeframe for the pie (DOES NOT INCLUDE YOUR HOLDINGS)
#Returns: % gain as float()
def checkReturnsPie(pid, timeframe):
    url = "https://dashboard.m1finance.com/d/c/set-order/" + pid
    driver.get(url)
    time.sleep(5)
    DebugCommand("Checking" + timeframe + " returns against: " + str(pid))
    if "day" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "week" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "month" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "quarter" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "year" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    elif "all" in timeframe:
        timeframe = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    else:
        DebugCommand("Timeframe not recognized.")
        return 0
    time.sleep(3)
    DebugCommand("Returns Check Complete")
    return float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/span/span[2]""").text)[0])


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
