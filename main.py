import m1lib
import config

if (m1lib.login(config.username, config.password) == 0):
    print("I successfully ran from a new module.")
    m1lib.selectAccount(config.accountType)
