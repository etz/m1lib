# M1 Finance Python 3 + Selenium Wrapper

## Installation:

1. Download ZIP or GIT with ```https://github.com/etz/m1lib.git```
2. Use ```import m1lib``` in a new python file or modify main.py
3. In terminal, ```cd /path/to/m1lib```
4. `python3 main.py`

## Usage:

`m1lib.login(config.username, config.password)` - Logs into the M1Finance Account using Chromedriver
`m1lib.selectAccount(config.accountType)` - Selects the account to make changes in
`m1lib.OrderPie(config.BaseOrder, "Q1BTOjVRTjQyODE1LDYwODE5MCw2MDk5MTc%3D")` - Orders $`config.BaseOrder` of the M1 Pie with the ID `Q1BTOjVRTjQyODE1LDYwODE5MCw2MDk5MTc` 
`m1lib.closeSession()` - Closes the work environment
