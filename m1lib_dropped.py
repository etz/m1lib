# These functions are either no longer being used or have been replaced
# by a more efficient methodology.



#Function: orderPV()
#Usage: Purchases a M1 Portfolio based on the USD value (amount) and the accType
#Returns: True if purchase successful
def orderPV(amount, accType):
    print ("Beginning Portfolio Purchase")
    selectAccount(accType)
    if amount < 0:
        ticksell = 1
        amount = amount * -1
    if amount < 10:
        DebugCommand("Orders under $10 cannot be processed")
        return False
    #try:
    #    driver.find_element_by_xpath("""//*[contains(text(), 'Buy/Sell')]""").click()
    #except:
    #    pass
    time.sleep(4)
    try:
        if ticksell == 1:
            startSell()
        usernameField = driver.find_element_by_name("cashFlow")
        usernameField.send_keys(amount)
    except:
        DebugCommand("Could not access cashFlow element")
        return False
    confirmOrder()
    if (verifyPV(accType) == True):
        return True


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
