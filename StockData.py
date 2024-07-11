import requests
import os

ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
ALPHA_VANTAGE = "https://www.alphavantage.co/query"
FMP_GENERAL_SEARCH = "https://financialmodelingprep.com/api/v3/search"


class Stock:

    def __init__(self, ticker: str, shares: int):
        self.ticker = ticker
        self.shares = shares
        self.stock_details = self.get_stock_details()
        additional_data = self.get_stock_name()
        self.name = additional_data["name"]
        self.currency = additional_data["currency"]
        stock_data_list = [value for key, value in self.stock_details["Time Series (Daily)"].items()]
        self.opening = float(stock_data_list[0]["1. open"])
        self.previousClosing = float(stock_data_list[0]["4. close"])
        self.high_price = float(stock_data_list[0]["2. high"])
        self.low_price = float(stock_data_list[0]["3. low"])
        self.last_refreshed = self.stock_details["Meta Data"]["3. Last Refreshed"]
        yesterday_closing = float(stock_data_list[1]["4. close"])
        self.closing_difference = round(self.previousClosing - yesterday_closing, 2)
        self.closing_difference_percent = round(
            ((self.previousClosing - yesterday_closing) / self.previousClosing) * 100, 2)

    def get_stock_details(self):
        #YH_FINANCE_PRICE_URL_JSON = {"ticker": self.ticker}
        #response = requests.get(YH_FINANCE_PRICE_URL, params=YH_FINANCE_PRICE_URL_JSON,headers=YH_FINANCE_PRICE_URL_HEADERS)
        alpha_vantage_params = {
            "function": "TIME_SERIES_DAILY",
            "apikey": ALPHA_VANTAGE_KEY,
            "outputsize": "full",
            "symbol": self.ticker
        }
        response = requests.get(ALPHA_VANTAGE, params=alpha_vantage_params)
        response.raise_for_status()
        return response.json()

    def get_stock_name(self):
        params = {
            "apikey": os.environ.get("FMP_KEY"),
            "query": self.ticker,
            "limit": 1

        }
        response = requests.get(FMP_GENERAL_SEARCH, params=params)
        response.raise_for_status()
        return response.json()[0]


def calc_grand_total(stockList: [Stock]):
    grandTotal = 0
    for stock in stockList:
        grandTotal += stock.shares * stock.previousClosing
    return round(grandTotal, 2)
