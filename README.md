# M1 Finance Python 3 + Selenium Wrapper

## Installation:

1. Download ZIP or GIT with ```https://github.com/etz/m1lib.git```
2. Use ```import m1lib``` in a new python file or modify main.py
3. In terminal, ```cd /path/to/m1lib```
4. `python3 main.py`

## Usage:

`m1lib.login(config.username, config.password)` - Logs into the M1Finance Account using Chromedriver
`m1lib.selectAccount(config.accountType)` - Selects the account to make changes in
`m1lib.OrderPie(config.BaseOrder, pid)` - Orders $`config.BaseOrder` of the M1 Pie with the PID being the `string` at the end of any particular Pie's URL.
`m1lib.OrderPV(amount, config.accType)` - Orders $`amount` of the M1 Portfolio labeled `config.accType`
`m1lib.checkReturnsPV(config.accountType, "week")` - Returns the gains/losses as a percentage against a portfolio
`m1lib.checkReturnsPie(pid, "week")` - Returns the gains/losses as a percentage against a pie
`m1lib.getPID(config.accountType)` - Returns the Pie ID of the accountType
`m1lib.closeSession()` - Closes the work environment
