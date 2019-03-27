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

#Access the Roth IRA
def selectAccount(accType):
    accountType = driver.find_element_by_xpath("""//*[@id="popup22"]/div[1]/h3""").text
    if accType not in accountType:
        driver.find_element_by_xpath("""//*[@id="popup22"]/div[1]/h3""").click()
        time.sleep(2)
        driver.find_element_by_xpath("""//*[@id="popup22"]/div[2]/div/div[2]""").click()
        time.sleep(5)
        selectAccount(accType)
    if accType in accountType:
        driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/span[1]""").click()
        time.sleep(3)
        print (driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[2]/span""").text)

selectAccount("IRA")

print("Done")
time.sleep(20)
driver.close()
