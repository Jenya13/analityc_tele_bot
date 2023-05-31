import yfinance as yf
from yfinance import shared
from .market_provider import MarketProvider


class YFinanceProvider(MarketProvider):
    def __init__(self):
        self.yf = yf

    def get_symbols_history(self, tickers: list, start_date: str, end_date: str, interval: str = '1d'):

        data = yf.download(tickers, start=start_date,
                           end=end_date, interval=interval)

        return data

    def get_symbol_history(self, symbol: str, start_date: str, end_date: str, interval: str = '1d'):

        ticker = yf.Ticker(symbol)
        data = ticker.history(
            start=start_date, end=end_date, interval=interval)
        return data
