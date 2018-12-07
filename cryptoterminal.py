import cryptocompare as cc
import json
import argparse
import sys
import os
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description="Track your crypto currencies portfolio in the terminal")
parser.add_argument("-a", "--add", help="Crypto currency to add to portfolio")
parser.add_argument("--amt", help="Amount of crypto currency to add to portfolio")
parser.add_argument("-rm", "--remove", help="Remove crypto currency from portfolio")
parser.add_argument("-p", "--portfolio", help="View portfolio", action="store_true")
parser.add_argument("-i","--info", help= "Get information of an or multiple crypto currencies", nargs= "+")
parser.add_argument("-c","--convert", help="Change fiat currency")
parser.add_argument("-w ", "--watchlist", help="Print watchlist", action="store_true")
parser.add_argument("-aw","--addwatchlist", help="Add a coin to your watchlist", nargs= "+")
parser.add_argument("-rmw","--removewatchlist", help="Remove coin from watchlist",nargs= "+")
args = parser.parse_args()

class CryptoTerminal():
    def __init__(self):
        self.currency="USD"
        self.fiat_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",\
         "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"]

    def parse_commandline(self):
        if args.convert:
            self.change_currency(args.convert)
        
        if args.add:
            amt = args.amt
            self.add_portfolio(args.add, args.amt)
        elif args.remove:
            self.remove_portfolio(args.remove)
        elif args.portfolio:
            self.print_portfolio()
        elif args.info:
            self.print_info(args.info)
        elif args.addwatchlist:
            self.add_watchlist(args.addwatchlist)
        elif args.removewatchlist:
            self.remove_watchlist(args.removewatchlist)
        elif args.watchlist:
            self.print_watchlist()
    
    def change_currency(self, currency):
        if currency.upper() not in self.fiat_currencies:
            sys.exit("{} is not supported".format(currency))
        self.currency = currency.upper()

    def get_all_coins(self):
        coins = cc.get_coin_list(format=True)
        return coins

    def get_portfolio(self):
        if not os.path.exists(os.path.expanduser("~/portfolio.json")):
            return {}
        try:
            return json.load(open(os.path.expanduser("~/portfolio.json")))
        except IOError:
            self.save_portfolio({})
            return {}

    def add_portfolio(self, symbol, amount):
        if symbol.upper() in self.get_all_coins():
            portfolio_data = self.get_portfolio()
            portfolio_data[symbol.upper()] = float(amount)
            self.save_portfolio(portfolio_data)
        else:
            sys.exit("{} is not supported".format(symbol))
    
    def remove_portfolio(self, symbol):
        portfolio_data = self.get_portfolio()
        if symbol.upper() in portfolio_data:
            del portfolio_data[symbol.upper()]
            self.save_portfolio(portfolio_data)

    def save_portfolio(self, data):
        json.dump(data, open(os.path.expanduser("~/portfolio.json"), 'w'))

    def get_watchlist(self):
        if not os.path.exists(os.path.expanduser("~/watchlist.json")):
            return {}
        try:
            return json.load(open(os.path.expanduser("~/watchlist.json")))
        except IOError:
            self.save_watchlist({})
            return {}

    def add_watchlist(self, coins):
        all_coin_data = self.get_all_coins()
        watchlist = self.get_watchlist()
        for coin in coins:
            if coin.upper() in watchlist:
                pass
                #print("{} is already in your watchlist".format(coin.upper()))
            elif coin.upper() in all_coin_data:
                watchlist.append(coin.upper())
                self.save_watchlist(watchlist)      

    def remove_watchlist(self, coins):
        watchlist_data = self.get_watchlist()
        for coin in coins:
            if coin.upper() in watchlist_data:
                watchlist_data.remove(coin.upper())
                #print("Removed {} from your watchlist".format(coin.upper()))
        
        self.save_watchlist(watchlist_data)

    def save_watchlist(self, data):
        json.dump(data, open(os.path.expanduser("~/watchlist.json"), 'w'))

    def print_portfolio(self):
        round_coin = 4
        round_fiat = 2
        portfolio = self.get_portfolio()
        
        coins = []
        for coin in portfolio:
            coins.append(coin)

        if len(coins) != 0:
            api_data = cc.get_price(coins, curr=self.currency, full=True)["DISPLAY"]
            price_data = cc.get_price(coins,curr=self.currency)

            field_names = ["Name","Price ({})".format(self.currency),"Change","MarketCap ({})".format(self.currency),"Holdings",\
            "Value ({})".format(self.currency)]
            p = PrettyTable()
            p.field_names = field_names

            total_value = 0
            for k,v in self.get_portfolio().items():
                p.add_row([\
                #name
                "{}".format(k),\
                #price
                "{}".format(api_data[k][self.currency]["PRICE"]),\
                #change
                "{} %".format(api_data[k][self.currency]["CHANGEPCT24HOUR"]),\
                #marketcap
                "{}".format(api_data[k][self.currency]["MKTCAP"]),\
                #holdings
                "{}".format(round(v,round_coin)),\
                #value
                "{}".format(round(price_data[k][self.currency]*v,round_fiat))\
                ])
                total_value += price_data[k][self.currency]*v
            print(p)
            print("Total Value: {v} {c}".format(v=round(total_value,2), c=self.currency))
        else:
            sys.exit("Please add coins to your portfolio")

    def print_info(self, coins):
        all_coin_data = self.get_all_coins()
        
        my_coins = []
        for coin in coins:
            if coin.upper() in all_coin_data:
                my_coins.append(coin.upper())

        if len(my_coins) != 0:
            field_names = ["Symbol","Price ({})".format(self.currency),"Change","MarketCap ({})".format(self.currency)]
            p = PrettyTable()
            p.field_names = field_names


            api_data = cc.get_price(my_coins, curr=self.currency, full=True)["DISPLAY"]

            for coin in my_coins:
                p.add_row([\
                #Name
                "{}".format(coin),\
                #price
                "{}".format(api_data[coin][self.currency]["PRICE"]),\
                #cange
                "{} %".format(api_data[coin][self.currency]["CHANGEPCT24HOUR"]),\
                #marketcap
                "{}".format(api_data[coin][self.currency]["MKTCAP"])\
                ]
                )
            print(p)
        else:
            sys.exit("No supported coin found")
    
    def print_watchlist(self):
        watchlist = self.get_watchlist()

        if len(watchlist) != 0:
            field_names = ["Symbol","Price ({})".format(self.currency),"Change","MarketCap ({})".format(self.currency)]
            p = PrettyTable()
            p.field_names = field_names


            api_data = cc.get_price(watchlist, curr=self.currency, full=True)["DISPLAY"]

            for coin in watchlist:
                p.add_row([\
                #Name
                "{}".format(coin),\
                #price
                "{}".format(api_data[coin][self.currency]["PRICE"]),\
                #cange
                "{} %".format(api_data[coin][self.currency]["CHANGEPCT24HOUR"]),\
                #marketcap
                "{}".format(api_data[coin][self.currency]["MKTCAP"])\
                ]
                )
            print(p)
        else:
            sys.exit("No watchlist file found")


def main():
    p = CryptoTerminal()
    p.parse_commandline()

if __name__ == "__main__":
    main()