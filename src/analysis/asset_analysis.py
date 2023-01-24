
import numpy as np
import pandas as pd


class TechnicalAnalysis:
    def __init__(self, asset: str, start_time: str, end_time: str, data):
        self.asset = asset
        self.start_time = start_time
        self.end_time = end_time
        self.data = data

    def calc_drawdown(self):
        """ Calculation Of drowdown of an instrumet and add it to instrument statistics Series, refers to the decline in value of a single investment or an investment portfolio from a relative peak value to a relative trough """
        # We compute Cumsum of the returns
        csum = self.data['pct_change'].dropna().cumsum()+1
        # We compute max of the cumsum on the period (accumulate max)(peak)
        running_max = np.maximum.accumulate(csum)
        # We compute drawdown
        drawdown = csum/running_max - 1
        # print(-np.min(self.drawdown))
        return drawdown

    def calc_sharp(self):
        """ Calculate Sharp ratio and add it to instrument statistics Series, used to help investors understand the return of an investment compared to its risk """
        return_serie = self.data['pct_change']
        mean = return_serie.mean()
        sigma = return_serie.std()
        sharp = np.round(np.sqrt(252) * mean/sigma, 3)
        return sharp

    def calc_sortino(self):
        """ Calculate sortino ratio and add it to instrument statistics Series, useful way for investors, analysts, and portfolio managers to evaluate an investment's return for a given level of bad risk """
        return_serie = self.data['pct_change']
        vol = return_serie[return_serie < 0].std()
        mean = return_serie.mean()
        sortino = np.round(np.sqrt(252) * mean/vol, 3)
        return sortino

    def calc_alpha(self):
        """ calculate Alpha and add it to instrument statistics Series, Alpha measures the amount that the investment has returned in comparison to the market index or other broad benchmark that it is compared against """
        df = pd.DataFrame()
        df['pct_change'] = self.data['pct_change']
        df.dropna(inplace=True)
        mean = df['pct_change'].mean
        alpha = np.round(mean - self.beta * mean, 3)
        return alpha
