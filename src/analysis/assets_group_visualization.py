import os
import numpy as np
import pandas as pd
import seaborn as sns
from .vizualization import Vizualization


class AssetsDataVisualization(Vizualization):
    def __init__(self, tickers: list, start_time: str, end_time: str, data: pd.DataFrame):
        super().__init__()
        self._tickers = tickers
        self._start_time = start_time
        self._end_time = end_time
        if data is not None:
            self._data = data.copy()

    def plot_risk_returns(self):
        data = self._data.copy()
        log_returns = data.apply(
            lambda x: np.log(x.dropna()/x.dropna().shift()))

        summary: pd.DataFrame = log_returns.agg(['mean', 'std']).T
        summary.columns = ['Mean', 'Std']

        summary.plot(kind="scatter", x="Std", y="Mean",
                     figsize=(12, 8), s=50, fontsize=16)
        for i in summary.index:
            self.plt.annotate(
                i, xy=(summary.loc[i, "Std"]+0.00005, summary.loc[i, "Mean"]+0.00005), size=15)
        self.plt.xlabel('Risk (std)')
        self.plt.ylabel('Mean Return')
        self.plt.title("Mean-Variance")

        plot_type = 'mean_variance'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path

    def plot_normalized(self):
        data = self._data.copy()
        norm = data.div(data.iloc[0]).mul(100)
        norm.dropna(inplace=True)
        title = 'Normalized Chart Of Instruments'
        norm.plot(figsize=(12, 8), title=title, fontsize=16, logy=True)
        self.plt.legend(fontsize=13)
        self.plt.xlabel('Date')
        self.plt.ylabel('')
        plot_type = 'normalized_group_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path

    def plot_correlation(self):
        # correlation coefficent:
        # three cases:
        #  1. corr == 0 -> no correlation
        #  2. 0 < corr <= 1 -> moving together (positive)
        #  3. -1 <= corr < 0 -> moving in oposite direction (negative)

        data = self._data.copy()
        log_returns = data.apply(
            lambda x: np.log(x.dropna()/x.dropna().shift()))

        self.plt.figure(figsize=(12, 8))
        self.plt.title('Correlation')
        sns.set(font_scale=1.4)
        colormap = sns.color_palette("flare", as_cmap=True)
        sns.heatmap(log_returns.corr(),  annot=True, cmap=colormap,
                    annot_kws={'size': 15}, vmin=-1, vmax=1)
        plot_type = 'correlation_plot'
        plot_id = self._generate_id()
        plot_name = plot_id + '-' + plot_type + '.png'
        plots_dir = self._plots_path
        img_path = os.path.join(plots_dir, plot_name)
        self.plt.savefig(img_path)
        self.plt.close()
        return img_path
