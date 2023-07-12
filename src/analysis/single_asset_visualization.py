
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as mtick
from .vizualization import Vizualization


def calc_drawdown(data):

    # We compute Cumsum of the returns
    csum = data['log_returns'].dropna().cumsum()+1

    # We compute max of the cumsum on the period (accumulate max)(peak)
    running_max = np.maximum.accumulate(csum)

    # We compute drawdown
    drawdown = csum/running_max - 1

    return drawdown


class SingleAssetDataVisualization(Vizualization):
    def __init__(self, ticker: str, start_time: str, end_time: str, data: pd.DataFrame):
        super().__init__()
        self._data = pd.DataFrame()
        self._ticker = ticker
        self._start_time = start_time
        self._end_time = end_time
        if data is not None:
            self._data = data.copy()

    def plot_normalized(self, benchmark: pd.DataFrame):
        """
        Create an image of normalized instrument vs benckmark chart
        """
        bmark = benchmark.copy()
        bmark.rename(columns={'Close': 'S&P500'}, inplace=True)
        data = self._data.copy()
        data.rename(columns={'Close': self._ticker}, inplace=True)
        df = pd.merge(data[[self._ticker]], bmark['S&P500'],
                      left_index=True, right_index=True)
        df = df.div(df.iloc[0]).mul(100)

        title = 'Normalized Chart - {} vs S&P500'.format(self._ticker)
        ax = df.plot(figsize=(12, 8), title=title, fontsize=16)
        date_range = df.index[-1] - df.index[0]
        if date_range < pd.Timedelta(days=30):
            locator = mdates.DayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=30) and date_range <= pd.Timedelta(days=90):
            locator = mdates.WeekdayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=90) and date_range <= pd.Timedelta(days=730):
            locator = mdates.MonthLocator()
            formatter = mdates.DateFormatter('%Y-%m')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        self.plt.legend(fontsize=13)
        self.plt.xlabel('Date')
        self.plt.ylabel('')
        plot_type = 'normalized_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path

    def plot_price(self):
        """
        Create an image of instrument price chart
        """
        title = 'Price Chart - {}'.format(
            self._ticker)
        data = self._data.copy()
        data.rename(columns={'Close': self._ticker}, inplace=True)
        ax = data[[self._ticker]].plot(
            figsize=(12, 8), title=title, fontsize=16)
        date_range = data.index[-1] - data.index[0]
        if date_range < pd.Timedelta(days=30):
            locator = mdates.DayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=30) and date_range <= pd.Timedelta(days=90):
            locator = mdates.WeekdayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=90) and date_range <= pd.Timedelta(days=730):
            locator = mdates.MonthLocator()
            formatter = mdates.DateFormatter('%Y-%m')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        self.plt.legend(fontsize=13)
        self.plt.xlabel('Date')
        self.plt.ylabel('price')
        plot_type = 'price_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path

    def plot_returns(self, kind='ts'):
        """
        Create an image of instrument return chart

        Parameters
        ----------
        kind: str, optional
            kind of chart
        """
        if kind == 'ts':
            title = 'Returns - {}'.format(self._ticker)
            ax = self._data['log_returns'].plot(
                figsize=(12, 8), title=title, fontsize=16)
            date_range = self._data.index[-1] - self._data.index[0]
            if date_range < pd.Timedelta(days=30):
                locator = mdates.DayLocator()
                formatter = mdates.DateFormatter('%Y-%m-%d')
                ax.xaxis.set_major_locator(locator)
                ax.xaxis.set_major_formatter(formatter)
            elif date_range > pd.Timedelta(days=30) and date_range <= pd.Timedelta(days=90):
                locator = mdates.WeekdayLocator()
                formatter = mdates.DateFormatter('%Y-%m-%d')
                ax.xaxis.set_major_locator(locator)
                ax.xaxis.set_major_formatter(formatter)
            elif date_range > pd.Timedelta(days=90) and date_range <= pd.Timedelta(days=730):
                locator = mdates.MonthLocator()
                formatter = mdates.DateFormatter('%Y-%m')
                ax.xaxis.set_major_locator(locator)
                ax.xaxis.set_major_formatter(formatter)
            # format the y-axis tick labels as percentages
            ax.yaxis.set_major_formatter(
                FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
            self.plt.xlabel('Date')
            self.plt.ylabel('Returns (%)')
            self.plt.legend(fontsize=13)
            plot_type = 'ts_returns_plot'
            plot_id = self._generate_id()
            plot_name = plot_id + '-' + plot_type + '.png'
            plots_dir = self._plots_path
            img_path = os.path.join(plots_dir, plot_name)
            self.plt.savefig(img_path)
            self.plt.close()
            return img_path

        elif kind == 'hist':

            mu = self._data['log_returns'].mean()
            sigma = self._data['log_returns'].std()
            x = np.linspace(self._data['log_returns'].min(
            ), self._data['log_returns'].max(), 1000)
            y = stats.norm.pdf(x, loc=mu, scale=sigma)
            self.plt.figure(figsize=(20, 8))
            self.plt.hist(self._data['log_returns'], bins=int(np.sqrt(len(self._data))), density=True, rwidth=0.95,
                          label='Frequency distribution of returns ({})'.format(self._ticker))
            self.plt.plot(x, y, linewidth=3, color='red',
                          label='Normal Distribution')
            self.plt.title(
                'Frequency Distribution Of Returns - {}'.format(self._ticker), fontsize=16)
            self.plt.xlabel('Returns')
            self.plt.ylabel('pdf')
            self.plt.legend()
            plot_type = 'hist_returns_plot'
            plot_id = self._generate_id()
            plot_name = plot_id + '-' + plot_type + '.png'
            plots_dir = self._plots_path
            img_path = os.path.join(plots_dir, plot_name)
            self.plt.savefig(img_path)
            self.plt.close()
            return img_path

    def plot_drawdown(self):
        """
        Create an image of instrument drawdown chart
        """
        date_range = self._data.index[-1] - self._data.index[0]
        drawdown = calc_drawdown(self._data.copy())
        self.plt.figure(figsize=(12, 8))
        self.plt.fill_between(drawdown.index, drawdown, 0,
                              drawdown < 0, color="#CE5757", alpha=0.45)
        if date_range <= pd.Timedelta(days=30):
            locator = mdates.DayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            self.plt.gca().xaxis.set_major_locator(locator)
            self.plt.gca().xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=30) and date_range <= pd.Timedelta(days=90):
            locator = mdates.WeekdayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            self.plt.gca().xaxis.set_major_locator(locator)
            self.plt.gca().xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=90) and date_range <= pd.Timedelta(days=730):
            locator = mdates.MonthLocator()
            formatter = mdates.DateFormatter('%Y-%m')
            self.plt.gca().xaxis.set_major_locator(locator)
            self.plt.gca().xaxis.set_major_formatter(formatter)

        self.plt.gca().yaxis.set_major_formatter(
            FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        self.plt.gcf().autofmt_xdate(rotation=45, ha='right')
        self.plt.grid(True, which='major', axis='x')
        mean_drawdown = drawdown.mean()
        mean_drawdown_series = pd.Series(mean_drawdown, index=drawdown.index)
        mean_drawdown_series.plot(
            color='lightseagreen', linestyle="--", label='Average')
        self.plt.legend(loc='center right')
        self.plt.title('Drawdown - {}'.format(self._ticker), fontsize=16)
        self.plt.xlabel('Date')
        self.plt.ylabel('Drowdown (%)')
        plot_type = 'drowdown_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path

    def plot_cum_returns(self, benchmark: pd.DataFrame):
        """
        Create image of instrument vs benchmark cumulative returns chart
        """
        bmark = benchmark.copy()
        bmark['pct_change'] = bmark['Close'].pct_change(
            1)
        bmark = bmark[['Close', 'pct_change']]
        bmark.dropna(inplace=True)
        bmark['bm_cum_returns'] = (1 + bmark['pct_change']).cumprod() - 1

        data = self._data.copy()
        data['asset_cum_returns'] = (1 + data['pct_change']).cumprod() - 1

        df = pd.merge(data[['asset_cum_returns']], bmark[['bm_cum_returns']],
                      left_index=True, right_index=True)
        df.rename(columns={'asset_cum_returns': self._ticker,
                  'bm_cum_returns': 'S&P500'}, inplace=True)

        ax = df.plot(
            figsize=(12, 8))
        date_range = df.index[-1] - df.index[0]
        if date_range <= pd.Timedelta(days=30):
            locator = mdates.DayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=30) and date_range <= pd.Timedelta(days=90):
            locator = mdates.WeekdayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=90) and date_range <= pd.Timedelta(days=730):
            locator = mdates.MonthLocator()
            formatter = mdates.DateFormatter('%Y-%m')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        self.plt.xlabel('Date')
        self.plt.ylabel('')
        self.plt.title(
            'Cumulative Returns - {} vs S&P500'.format(self._ticker), fontsize=16)
        plot_type = 'cum_returns_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path

    def plot_top5_drawdown(self):
        """
        Create an image of instrument vs benchmark cumulative returns chart
        """

        cumulative_returns = (1 + self._data['pct_change']).cumprod() - 1
        drawdown = calc_drawdown(self._data.copy())

        # Find the start and end dates of each drawdown period
        dd_starts = []
        dd_ends = []
        dd_lengths = []
        current_dd_start = None
        current_dd_length = 0
        for i, dd in drawdown.items():
            if dd < 0:
                if current_dd_start is None:
                    current_dd_start = i
                current_dd_length += 1
            else:
                if current_dd_start is not None:
                    dd_starts.append(current_dd_start)
                    dd_ends.append(i)
                    dd_lengths.append(current_dd_length)
                    current_dd_start = None
                    current_dd_length = 0

        # Sort the drawdown periods by length and return the top 5
        sorted_dd_lengths = np.argsort(dd_lengths)[::-1][:5]
        top_5_dd_starts = [dd_starts[i] for i in sorted_dd_lengths]
        top_5_dd_ends = [dd_ends[i] for i in sorted_dd_lengths]
        top_5_dd_lengths = [dd_lengths[i] for i in sorted_dd_lengths]
        top_5_drawdowns = pd.DataFrame({'start_date': top_5_dd_starts,
                                        'end_date': top_5_dd_ends,
                                        'length': top_5_dd_lengths})

        title = "Top 5 Drawdown Periods - {}".format(self._ticker)
        ax = cumulative_returns.plot(
            figsize=(12, 8), color='blue', title=title, fontsize=16)

        self.plt.gca().yaxis.set_major_formatter(
            FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        self.plt.gcf().autofmt_xdate(rotation=45, ha='right')
        self.plt.grid(True, which='major', axis='x')
        self.plt.plot(cumulative_returns)

        for i, row in top_5_drawdowns.iterrows():
            self.plt.axvspan(row['start_date'],
                             row['end_date'], color="#CE5757", alpha=0.45)

        date_range = self._data.index[-1] - self._data.index[0]
        if date_range < pd.Timedelta(days=30):
            locator = mdates.DayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=30) and date_range <= pd.Timedelta(days=90):
            locator = mdates.WeekdayLocator()
            formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
        elif date_range > pd.Timedelta(days=90) and date_range <= pd.Timedelta(days=730):
            locator = mdates.MonthLocator()
            formatter = mdates.DateFormatter('%Y-%m')
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

        plot_type = 'top5_drawdowns_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path
