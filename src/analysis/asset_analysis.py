import statsmodels.api as sm
import numpy as np
import pandas as pd
from providers.yfinance_provider import YFinanceProvider


class SingleAssetTechnicalAnalysis:
    def __init__(self, asset: str, start_time: str, end_time: str, data: pd.DataFrame, benchmark: pd.DataFrame):

        self.asset = asset
        self.start_time = start_time
        self.end_time = end_time
        self._data = data
        self._prepare_data()
        self.benchmark = benchmark
        self._prepare_benchmark()

    def get_asset_data(self):
        return self._data.copy()

    def _prepare_benchmark(self):
        """ Prepare benchmark data for next processing """
        benchmark = self.benchmark.copy()
        benchmark['^GSPC_pct_change'] = benchmark['Close'].pct_change(
            1)
        benchmark.rename(columns={'Close': '^GSPC'}, inplace=True)
        benchmark = benchmark[['^GSPC', '^GSPC_pct_change']]
        benchmark.dropna(inplace=True)
        self.benchmark = benchmark.copy()

    def _prepare_data(self):
        """ Prepare data for next processing """
        data = self._data.copy()
        data = data[['Close']].copy()
        data['pct_change'] = data['Close'].pct_change(periods=1)
        data['log_returns'] = np.log(
            data['Close']/data['Close'].shift(1))
        data.dropna(inplace=True)
        self._data = data.copy()

    def calc_drawdown(self):
        """ Calculation Of drowdown,  drawdown refers to the decline from a peak in the value of an investment or portfolio to a trough or
            valley. It is typically expressed as a percentage of the peak value and is used to measure the risk of an investment """
        # We compute Cumsum of the returns
        csum = self._data['pct_change'].dropna().cumsum()+1
        # We compute max of the cumsum on the period (accumulate max)(peak)
        running_max = np.maximum.accumulate(csum)
        # We compute drawdown
        drawdown = csum/running_max - 1
        # print(-np.min(self.drawdown))
        return np.round(np.min(drawdown*100), 3)

    def calc_sharp(self):
        """ Calculate Sharp ratio, Sharpe ratio is a measure of risk-adjusted return, which compares the return of an investment to that of a risk-free asset, such as a Treasury bond, and adjusts for the volatility of the investment """

        return_serie = self._data['pct_change']
        mean = return_serie.mean()
        sigma = return_serie.std()
        sharp = np.round(np.sqrt(252) * mean/sigma, 3)
        return sharp

    def calc_sortino(self):
        """ Calculate sortino ratio, The Sortino ratio is used to evaluate the risk-adjusted performance of an investment, and it can be used to compare the performance of different investments. A higher Sortino ratio indicates that an investment has delivered a higher return for a given level of downside risk"""

        return_serie = self._data['pct_change']
        vol = return_serie[return_serie < 0].std()
        mean = return_serie.mean()
        sortino = np.round(np.sqrt(252) * mean/vol, 3)
        return sortino

    def calc_alpha(self):
        """ calculate Alpha, In finance, alpha is a measure of a portfolio or fund's performance in relation to a benchmark index.
            An alpha of zero indicates that the portfolio or fund has performed in line with the benchmark, while a high alpha indicates that the portfolio manager has added significant value through security selection or market timing """

        # alpha > 0: The portfolio outperforms the market in terms of risk return
        # alpha < 0: The portfolio underperforms the market in terms of risk return
        mean = self._data['pct_change'].mean()
        beta = self.calc_beta()
        alpha = 252*(mean - beta*mean)
        return np.round(alpha*100, 3)

    def calc_beta(self):
        """ calculate Beta, beta is a measure of a stock's volatility in relation to the overall market.
            A beta of 1 indicates that the stock's price will move with the market, while a beta less than 1 means it is less volatile than the market, and a beta greater than 1 indicates higher volatility """

        # A stock with a beta of 1 is considered to be as volatile as the market, while a beta of 2 means the stock is twice as volatile as the market. Similarly, a beta of 0.5 means the stock is half as volatile as the market. Beta can be used to determine the risk of a stock relative to the market and thus it is used in portfolio diversification and risk management.

        data = pd.DataFrame()
        data = pd.concat(
            [self._data[['Close', 'pct_change']], self.benchmark[['^GSPC', '^GSPC_pct_change']]], axis=1)
        data.dropna(inplace=True)

        cov = np.cov(
            data[['pct_change', '^GSPC_pct_change']].values, rowvar=False)[0][1]
        var = np.var(data['^GSPC_pct_change'].values)
        beta = np.round(cov/var, 3)
        return beta

    def mean_return(self, freq=None):
        """ Calculate Mean Log Returns of an instrument depends on frequency, by default without frequency and add it to instrument statistics Series """
        if freq is None:
            # return 'Mean Returns {}'.format(round(self._data['log_returns'].mean()*100, 4))
            return round(self._data['log_returns'].mean()*100, 4)
        else:
            resampled_price = self._data['Close'].resample(
                freq).last()
            resampled_returns = np.log(
                resampled_price/resampled_price.shift(1))
            # return 'Mean Returns {} for {} frequency'.format(round(resampled_returns.mean()*100, 4), freq)
            return round(resampled_returns.mean()*100, 4)

    def std_return(self, freq: str = None):
        """ Calculate Standart deviation Log Returns of an instrument depends on frequency, by default without frequency and add it to instrument statistics Series"""
        if freq is None:
            # return 'STD Returns {}'.format(round(self._data['log_returns'].std()*100, 4))
            return round(self._data['log_returns'].std()*100, 4)
        else:
            resampled_price = self._data['Close'].resample(
                freq).last()
            resampled_returns = np.log(
                resampled_price/resampled_price.shift(1))
            # return 'STD Returns {} for {} frequency '.format(round(resampled_returns.std()*100, 4), freq)
            return round(resampled_returns.std()*100, 4)

    def annualized_performence(self):
        """ Calculation Of annualized Performence, Return/Risk and add it to instrument statistics Series"""
        mean_return = round(self._data['log_returns'].mean()*252, 3)
        risk = round(self._data['log_returns'].std()*np.sqrt(252), 3)
        # return 'Return: {}% | Risk: {}%'.format(round(mean_return*100, 3), round(risk*100, 3))
        return (round(risk*100, 3), round(mean_return*100, 3))
