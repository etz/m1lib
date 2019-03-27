from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import re

#Function: DebugCommand
#Usage: Prints debugging information in the console
#Returns:
def DebugCommand(string):
    global debug_variable
    #Change me to debug!
    debug_variable = 1
    if debug_variable == 1:
        print ("DEBUG: " + string)


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


#Function: selectAccount
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
        selectAccount(accType)
    time.sleep(2)
    DebugCommand("Account Selected")

#Function: CheckOpenOrder
#Usage: Returns Order value depending on accType
#Returns: Logs order information, "0" if pending order, "1" else
#TODO
def checkOpenPV(accType):
    DebugCommand("Checking orders against Portfolio: " + accType)
    selectAccount(accType)
    try:
        orderCompletion = driver.find_element_by_xpath("""//*[contains(text(), 'Pending')]""").text
        DebugCommand(str(orderCompletion))
        if "buy" in orderCompletion:

            #RETURNS A BUY ORDER

            print("PENDING BUY:" + str(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", orderCompletion)[0]))
            return 0
        elif "sell" in orderCompletion:

            #RETURNS A SELL ORDER

            print("PENDING SELL:" + str(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", orderCompletion)[0]))
            return 0
    except:
        return 1

#Function: VerifyPie
#Usage: Checks if an order was completed as requested
#Returns: Nothing
def VerifyPie(pid):
    print ("Beginning Order Verification")
    url = "https://dashboard.m1finance.com/d/invest/portfolio/" + pid
    driver.get(url)
    time.sleep(5)
    #selectAccount(accType)
    try:
        orderCompletion = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/span""").text
        DebugCommand("Order complete")
    except:
        DebugCommand("Order failed")
        pass


#Function: CheckDayGain
#Usage: Provides the USD return for the accType
#Returns: % gain as float()
def CheckDayGain(accType):
    DebugCommand("Checking Daily Returns against" + str(accType))
    selectAccount(accType)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    time.sleep(3)
    DebugCommand("Returns Check Complete")
    return float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/span/span[2]""").text)[0])


#Function: BuyPortfolio
#Usage: Purchases a M1 Portfolio based on the USD value (amount) and the accType
#Returns: "0" if purchase successful
def BuyPortfolio(amount, accType):
    print ("Beginning Portfolio Purchase")
    if (checkOpenPV(accType) == 1):
        if (int(amount) < 10):
            print("Orders under $10 cannot be processed")
            return
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[3]/div/button[1]""").click()
        time.sleep(4)
        try:
            usernameField = driver.find_element_by_name("cashFlow")
            usernameField.send_keys(amount)
        except:
            print("It appears there is already a concurrent order.")
            return 1
        ConfirmOrder()
    checkOpenPV(accType)



#Function: OrderPie
#Usage: Purchases a M1 Pie based on the USD value (amount) and the pie ID (pid)
#Returns: "0" if purchase successful
def OrderPie(amount, pid):
    print ("Beginning Pie Purchase")
    url = "https://dashboard.m1finance.com/d/c/set-order/" + pid
    driver.get(url)
    time.sleep(5)
    if amount < 0:
        print("Amount is less than 0")
        SellButton = driver.find_elements_by_xpath("//*[contains(text(), 'Sell')]")
        for element in SellButton:
            try:
                element.click()
            except:
                pass
        time.sleep(5)
        amount = amount * -1
    try:
        usernameField = driver.find_element_by_name("cashFlow")
        usernameField.send_keys(amount)
    except:
        DebugCommand("There was an issue with the connection or the element 'cashFlow' could not be found.")
        return 1
    ConfirmOrder()
    VerifyPie(pid)

#Function: ConfirmOrder
#Usage: Completes an opened order after the cashFlow element has been filled
#Returns:
def ConfirmOrder():
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[6]/button[2]""").click()
    time.sleep(3)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[9]/button[2]""").click()
    time.sleep(6)




#Function: OrderWeight
#Usage: Determines a new value determined on a base and multiplier
#Returns: float()
def OrderWeight(base, multiplier):
    if (multiplier > 0):
        multiplier = 1-(multiplier/10)
    else:
        multiplier = (-1*(multiplier/100))+1
    print (str(base))
    print (str(multiplier))
    newValue = float("{0:.2f}".format(base*multiplier))
    print("Base Amount: " + str(base) + "USD, after multiplier: " + str(newValue))
    return newValue


def closeSession():
    driver.close()

#PercentGain = CheckDayGain(accountType)
#OrderWeight(75, float(PercentGain[0]))
#BuyPie(OrderWeight(BaseBuy, CheckDayGain(accountType)), accountType)
