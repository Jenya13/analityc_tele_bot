import yfinance as yf
from .market_provider import MarketProvider


class YFinanceProvider(MarketProvider):
    def __init__(self):
        self.yf = yf

    def get_symbols_history(self, symbol: str, start_date: str, end_date: str):
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
