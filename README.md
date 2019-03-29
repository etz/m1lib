# M1 Finance Python 3 + Selenium Wrapper

There is no public API available for M1 Finance, which presents an opportunity...

`pid` = the string at the end of any Pie's URL, /d/invest/portfolio/`Q1BTOYwODE5MCw2jVRTjQyODE1LDMDk5MTc%3D`


## Dependencies:

You probably already have:
- Python 3+
- Python Package: `re`

You will need:
- Selenium `python3 -m pip install selenium`
- Chromedriver http://chromedriver.chromium.org/getting-started

## Installation:

1. Download ZIP or GIT with ```git clone https://github.com/etz/m1lib.git```
2. Use ```import m1lib``` in a new python file or modify main.py
3. In terminal, ```cd /path/to/m1lib```
4. Modify the `config.py` file
5. `python3 main.py`


## Usage:

### Basic / Authentication

`m1lib.login(config.username, config.password)` - Logs into the M1Finance Account using Chromedriver

`m1lib.selectAccount(config.accountType)` - Selects the account to make changes in

`m1lib.closeSession()` - Closes the associated account

### Trading

`m1lib.orderPie(config.BaseOrder, pid)` - Orders $`config.BaseOrder` of the M1 Pie with the PID being the `string` at the end of any particular Pie's URL.

`m1lib.cancelOrder(pid)` - Cancels the order associated with Pie ID (use getPID for `PV`s)

`m1lib.orderPV(amount, config.accType)` - Orders $`amount` of the M1 Portfolio labeled `config.accType`

`m1lib.checkReturnsPV(config.accountType, "week")` - Returns the gains/losses as a percentage(float) against a portfolio

`m1lib.checkReturnsPie(pid, "week")` - Returns the gains/losses as a percentage(float) against a pie

`m1lib.getPID(config.accountType)` - Returns the Pie ID of the `accountType` from the config file.

`m1lib.rebalancePie(pid)` - Sets a specific Pie ID for rebalance

`m1lib.rebalancePV(accType)` - Sets `accType` for rebalance

`m1lib.initiateDeposit(amount, accType, year='')`

`m1lib.initiateWithdraw(amount, accType)`

### Search & Options

`m1lib.tickerSearch(mk_min='',mk_max='',pe_min='',pe_max='',div_min='',div_max='',sector='',industry='')` - I'll document this one later.

`m1lib.searchTicker(ticker)` -  Returns [float(price), float(div_yield), str(mkcap), float(pe_ratio)]

`m1lib.getCurrentMarketData()` - Returns the [day] % difference in the SPY, DIA, and QQQ tickers similar to searchTicker

`m1lib.changeAutoInvest(accType, option='', amount='')` - options=`set/all/off`, use amount if options=`set`


## TODO

This project is not designed to re-invent the wheel, therefore the library functionality will be limited in trading features.

- Cash Only support
- "Borrow" balance support
- Misc. features
