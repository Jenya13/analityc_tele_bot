from abc import ABC, abstractmethod


class MarketProvider(ABC):

    @abstractmethod
    def get_symbols_history(self, symbol: str, start_date: str, end_date: str, interval: str = '1d'):
        pass

    @abstractmethod
    def get_symbol_history(self, symbol: str, start_date: str, end_date: str, interval: str = '1d'):
        pass
