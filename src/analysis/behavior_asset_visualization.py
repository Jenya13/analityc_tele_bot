
import os
import pandas as pd
from pandas.api.types import CategoricalDtype
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
from .vizualization import Vizualization


class BehaviorAssetDataVisualization(Vizualization):

    def __init__(self, ticker: str, start_time: str, end_time: str, data: pd.DataFrame):
        super().__init__()
        self._data = data.copy()
        self._ticker = ticker
        self._start_time = start_time
        self._end_time = end_time

    def plot_avg_hourly_spread_trade(self):
        self._data['Hour'] = self._data['il_tz'].dt.hour
        by_hour = self._data.groupby('Hour')['Spread'].mean()
        if (by_hour == 0.0).all():
            return
        else:
            try:
                by_hour = by_hour.to_frame()
                by_hour = by_hour.reset_index()
                by_hour.set_index('Hour', inplace=True)
                title = f'Average Hourly Spread: {self._ticker} {self._start_time} - {self._end_time}'
                fig, ax = self.plt.subplots(figsize=(12, 8))
                by_hour.plot(kind='bar', ax=ax, title=title, fontsize=16)
                self.plt.xlabel('IL Time')
                self.plt.ylabel('Spread')
                plot_type = 'bh_avg_h_spread_plot'
                plot_id = self._generate_id()
                plot_name = plot_id + '-' + plot_type + '.png'
                plots_dir = self._plots_path
                img_path = os.path.join(plots_dir, plot_name)
                self.plt.savefig(img_path)
                self.plt.close()
            except Exception as e:
                print("An error occurred:", str(e))
            return img_path

    def plot_avg_hourly_price_change_trade(self):
        try:
            title = f'Average Hourly Price Change ABS: {self._ticker} {self._start_time} - {self._end_time}'
            self._data['Hour'] = self._data['il_tz'].dt.hour
            self._data.dropna().groupby('Hour')['Price Change ABS'].mean().plot(
                kind='bar', figsize=(12, 8), title=title, fontsize=16)
            self.plt.xlabel('IL Time')
            self.plt.ylabel('Price Change')
            plot_type = 'bh_avg_h_price_change_plot'
            plot_id = self._generate_id()
            plot_name = plot_id + '-' + plot_type + '.png'
            plots_dir = self._plots_path
            img_path = os.path.join(plots_dir, plot_name)
            self.plt.savefig(img_path)
            self.plt.close()
        except Exception as e:
            print("An error occurred:", str(e))
        return img_path

    def plot_avg_volume_trade(self, freq: str = None):
        freq_str = freq if freq is not None else "1H"

        if (self._data['Volume'] == 0.0).all():
            return

        title = f'Average Volume Traded ({freq_str}): {self._ticker} {self._start_time} - {self._end_time}'
        try:
            if freq is not None:
                self._data = self._data.resample(freq).last().dropna()
                self._data['Day Of Week'] = self._data['il_tz'].dt.strftime(
                    '%a')
                self._data.dropna().groupby('Day Of Week')['Volume'].mean().plot(
                    kind='bar', figsize=(12, 8), title=title, fontsize=16)
            else:
                self._data['Hour'] = self._data['il_tz'].dt.hour
                self._data.dropna().groupby('Hour')['Volume'].mean().plot(
                    kind='bar', figsize=(12, 8), title=title, fontsize=16)

            self.plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            self.plt.xlabel('IL Time')
            self.plt.ylabel('Volume')

            plot_type = f'bh_avg_{freq_str}_volume_plot'
            plot_id = self._generate_id()
            plot_name = plot_id + '-' + plot_type + '.png'
            plots_dir = self._plots_path
            img_path = os.path.join(plots_dir, plot_name)
            self.plt.savefig(img_path)
            self.plt.close()
        except Exception as e:
            print("An error occurred:", str(e))
        return img_path

    def plot_graularity_cover_cost(self, freq: str = '1H'):

        try:

            self._data['Cover Costs'] = self._data['Price Change ABS'] > self._data['Spread']
            if freq != '1H':
                self._data = self._data.resample(freq).last().dropna()
            if freq == '1D':
                self._data['Day Of Week'] = self._data['il_tz'].dt.strftime(
                    '%a')
                title = f'Cover Costs Granularity(1W): {self._ticker} {self._start_time} - {self._end_time}'
                self._data.dropna().groupby('Day Of Week')['Cover Costs'].mean().plot(
                    kind='bar', figsize=(12, 8), title=title, fontsize=16)
            else:
                self._data['Hour'] = self._data['il_tz'].dt.hour
                title = f'Cover Costs Granularity({freq}): {self._ticker} {self._start_time} - {self._end_time}'
                self._data.dropna().groupby('Hour')['Cover Costs'].mean().plot(
                    kind='bar', figsize=(12, 8), title=title, fontsize=16)

            # Set the y-axis tick format as a percentage
            formatter = ticker.PercentFormatter(xmax=1, decimals=0)
            self.plt.gca().yaxis.set_major_formatter(formatter)
            # Specify the y-axis tick positions
            self.plt.gca().yaxis.set_major_locator(
                ticker.FixedLocator(self.plt.gca().get_yticks()))
            self.plt.xlabel('IL Time')
            self.plt.ylabel('% Bars cover costs')
            plot_type = f'bh_{freq}_cover_costs'
            plot_id = self._generate_id()
            plot_name = plot_id + '-' + plot_type + '.png'
            plots_dir = self._plots_path
            img_path = os.path.join(plots_dir, plot_name)
            self.plt.savefig(img_path)
            self.plt.close()
        except Exception as e:
            print("An error occurred:", str(e))
        return img_path
