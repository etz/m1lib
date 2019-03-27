from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import re


#Function: login(user,pass)
#Usage: Initalizes Chrome & logs into the M1 Finance Account
#Returns: "0" if login successful
def login(m1user, m1pass):
    global driver
    #Initalize Chrome Driver
    chromeOptions = webdriver.ChromeOptions()
    capabilities=webdriver.DesiredCapabilities.CHROME
    driver= webdriver.Chrome(options=chromeOptions,desired_capabilities=capabilities)
    #Navigate to M1 Website
    url = "https://dashboard.m1finance.com/login"
    driver.get(url)
    #Allow time to load
    time.sleep(4)
    #Send user Credentials
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

def getAccounts():
    accounts = []
    #driver.find_elements_by_class("style__trigger__6kog7")[0].click()
    #Finds parent element by Account text
    driver.find_elements_by_xpath("//*[contains(text(), ' - ')]/../..")[1].click()
    accountList = driver.find_elements_by_xpath("//*[contains(text(), ' - ')]")
    print(accountList)
#    for account in accountList:
#        if account.text in accounts:
#            pass
#        else:
#            print(account.text)
#            accounts.append(account.text)
#    return accounts


#Function: selectAccount
#Usage: Selects the account determined in the Config file
#Returns: Nothing

def selectAccount(accType):
    accountList = getAccounts()
    print ("Beginning Account Selection")
    accountType = driver.find_elements_by_xpath("//*[contains(text(), ' - ')]")[1].text
    print (accountType)
    if accType not in accountType:
        driver.find_element_by_xpath("""//*[contains(text(), '""" + accType + """')]/..""").click()
        time.sleep(2)
        selectAccount(accType)
        pass
    time.sleep(2)
    print ("Account Selected!")

#Function: CheckOpenOrder
#Usage: Returns Order value depending on accType
#Returns: "0" if pending buy order, "1" else

def CheckOpenOrder(accType):
    selectAccount(accType)
    orderCompletion = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/span""").text
    if "Pending buy" in orderCompletion:
        print("PENDING:" + orderCompletion)
        return 0
    else:
        return 1

#Function: CheckDayGain
#Usage: Provides the USD return for the accType
def CheckDayGain(accType):
    print ("Beginning Return Check")
    selectAccount(accType)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    time.sleep(3)
    print ("RC Complete")
    return float(re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/span/span[2]""").text)[0])


#Function: BuyPie
#Usage: Purchases a M1 Pie based on the USD value and the accType
#Returns: Nothing
def BuyPie(amount, accType):
    print ("Beginning Pie Purchase")
    selectAccount(accType)
    if (amount < 10):
        print("Orders under $10 cannot be processed")
        return
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[3]/div/button[1]""").click()
    time.sleep(4)
    try:
        usernameField = driver.find_element_by_name("cashFlow")
        usernameField.send_keys(amount)
    except:
        print("It appears there is already a concurrent order.")
        return
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[6]/button[2]""").click()
    time.sleep(3)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/span/div/div[2]/div/div/div/div/div[9]/button[2]""").click()
    time.sleep(6)
    try:
        orderCompletion = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/span""").text
    except:
        print ("There was an issue completing your order as intended.")
        BuyPie(amount, accType)
    if "buy" in orderCompletion:
        print ("Purchase successful! " + amount + "$ bought")

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




#PercentGain = CheckDayGain(accountType)
#OrderWeight(75, float(PercentGain[0]))
#BuyPie(OrderWeight(BaseBuy, CheckDayGain(accountType)), accountType)
