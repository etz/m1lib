from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time

#Initalize Chrome Driver
chromeOptions = webdriver.ChromeOptions()
capabilities=webdriver.DesiredCapabilities.CHROME
driver= webdriver.Chrome(options=chromeOptions,desired_capabilities=capabilities)

username = ""
password = ""
accountType = "IRA"

#Go to M1 Finance's Website
#Log-in with the account information
def login(m1user, m1pass):
    url = "https://dashboard.m1finance.com/login"
    driver.get(url)
    time.sleep(5)
    usernameField = driver.find_element_by_name("username")
    usernameField.send_keys(m1user)
    pwField = driver.find_element_by_name("password")
    pwField.send_keys(m1pass)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div/div[2]/div/div/form/div[4]/div/button""").click()
    time.sleep(5)

login(username, password)

#Function: CheckOrderStatus
#Usage: Returns Order value depending on accType
def CheckOrderStatus(accType):
    selectAccount(accType)
    orderCompletion = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div[1]/span""").text
    if "Pending buy" in orderCompletion:
        print("PENDING:" + orderCompletion)

#Function: CheckDayGain
#Usage: Provides the USD return for the accType
def CheckDayGain(accType):
    selectAccount(accType)
    driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
    time.sleep(3)
    print (driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[2]/span""").text)

#Function: selectAccount
#Usage: Determines if the account being edited is the one we intend
def selectAccount(accType):
    accountType = driver.find_element_by_xpath("""//*[@id="popup22"]/div[1]/h3""").text
    if accType not in accountType:
        driver.find_element_by_xpath("""//*[@id="popup22"]/div[1]/h3""").click()
        time.sleep(2)
        driver.find_element_by_xpath("""//*[@id="popup22"]/div[2]/div/div[2]""").click()
        time.sleep(5)
        selectAccount(accType)
    time.sleep(2)

#Function: BuyPie
#Usage: Purchases a M1 Pie based on the USD value and the accType
def BuyPie(amount, accType):
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

CheckDayGain(accountType)
BuyPie(15, accountType)
CheckOrderStatus(accountType)

print("Script Complete")
time.sleep(20)
driver.close()
