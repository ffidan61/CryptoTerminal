# CryptoTerminal

[![Build Status](https://travis-ci.org/ffidan61/CryptoTerminal.svg?branch=master)](https://travis-ci.org/ffidan61/CryptoTerminal)

  

CryptoTerminal is a terminal application to create and track your cryptocurrency portfolio and watchlist using the [CryptoCompare API](https://min-api.cryptocompare.com), [CryptoCompare Wraper](https://github.com/lagerfeuer/cryptocompare) and [PrettyTable](https://github.com/mapio/prettytable-mirror).

## Install
using PyPi:
`pip install cryptoterminal`

You can also:
* clone this repo into a folder
-- `git clone https://github.com/ffidan61/CryptoTerminal/`
* install it
-- `python setup.py install`

## Usage
##### Portfolio management
Adding a currency to your portfolio:
*  `cryptoterminal -a eth --amt 2`

To remove a coin from your terminal:
*  `cryptoterminal -rm eth`

View portfolio:
*  `cryptoterminal -p`

##### Watchlist managment

Add coins to your watchlist:
*  `cryptoterminal -aw eth btc bch xmr`

View watchlist:
*  `cryptoterminal -w`

##### Get coin information
Get price and Marketcap data for specific symbols:
-  `cryptoterminal -i btc eth xrp`