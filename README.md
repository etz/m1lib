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
3. In terminal, ```cd /path/to/m1lib```
4. Modify the `py` file
5. `python3 main.py`


## Usage:

```
from m1lib import *
from config import *
```

### Basic / Authentication

`login(username, password)` - Logs into the M1Finance Account using Chromedriver

`selectAccount(accountType)` - Selects the account to make changes in

`closeSession()` - Closes the associated account

### Trading

`orderPie(amount, pid)` - Orders amount of pie based on string `pid`

`cancelOrder(pid)` - Cancels the order associated with Pie ID (use getPID for `PV`s)

`orderPV(amount, accountType)` - Orders $`amount` of the M1 Portfolio labeled `accountType`

`checkReturnsPV(accountType, "week")` - Returns the gains/losses as a percentage(float) against a portfolio

`checkReturnsPie(pid, "week")` - Returns the gains/losses as a percentage(float) against a pie

`getPID(accountType)` - Returns the Pie ID of the `accountType` from the config file.

`rebalancePie(pid)` - Sets a specific Pie ID for rebalance

`rebalancePV(accountType)` - Sets `accountType` for rebalance

`initiateDeposit(amount, accountType, year='')` - Initiate a deposit for a selected account. If IRA, set a third variable year=`2019`

`initiateWithdraw(amount, accountType)` - Initiate a withdraw for a selected account.

### Search & Options

`tickerSearch(mk_min='',mk_max='',pe_min='',pe_max='',div_min='',div_max='',sector='',industry='')` - searches M1 for all stocks within set parameters. 

`tickerSearch(aum_min='',aum_max='',exp_min='',exp_max='',div_min='',div_max='',sector='',industry='')` - searches M1 for all funds within set parameters.

`searchTicker(ticker)` -  Returns [float(price), float(div_yield), str(mkcap), float(pe_ratio)] of string ticker

`getCurrentMarketData()` - Returns the [day] % difference in the SPY, DIA, and QQQ tickers similar to searchTicker

`changeAutoInvest(accountType, option='', amount='')` - options=`set/all/off`, use amount if options=`set`


## TODO

This project is not designed to re-invent the wheel, therefore the library functionality will be limited in trading features.

- Cash Only support
- "Borrow" balance support
- Misc. features
