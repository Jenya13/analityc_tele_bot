
from abc import ABC
import random
import string
import time
import os
from matplotlib import cycler
import matplotlib.pyplot as plt
plt.switch_backend('Agg')


class PlotSettings:
    def __init__(self):
        self._set_rc_params()

    def _set_rc_params(self):
        colors = cycler('color',
                        ['#669FEE', '#66EE91', '#9988DD',
                         '#EECC55', '#88BB44', '#FFBBBB'])
        plt.rc('figure', facecolor='#313233')
        plt.rc('axes', facecolor="#313233", edgecolor='none',
               axisbelow=True, grid=True, prop_cycle=colors,
               labelcolor='gray')
        plt.rc('grid', color='474A4A', linestyle='solid')
        plt.rc('xtick', color='gray')
        plt.rc('ytick', direction='out', color='gray')
        plt.rc('legend', facecolor="#313233", edgecolor="#313233")
        plt.rc("text", color="#C9C9C9")
        plt.rc('figure', facecolor='#313233')

    def set_plot_settings(self, font_family='serif', fontdict=None):
        plt.rc('font', family=font_family)
        if fontdict:
            plt.rc('axes', labelsize=fontdict.get('fontsize'))
            plt.rc('axes', labelweight=fontdict.get('fontweight'))
            plt.rc('axes', labelcolor=fontdict.get('color'))
            plt.rc('axes', titlesize=fontdict.get('fontsize'))
            plt.rc('axes', titleweight=fontdict.get('fontweight'))
            plt.rc('axes', titlecolor=fontdict.get('color'))
            plt.rc('xtick', labelsize=fontdict.get('fontsize'))
            plt.rc('xtick', color=fontdict.get('color'))
            plt.rc('ytick', labelsize=fontdict.get('fontsize'))
            plt.rc('ytick', color=fontdict.get('color'))


class Vizualization(ABC):
    def __init__(self):
        self._plots_path = self._get_plots_path()
        self.plt = plt
        self.plot_settings = PlotSettings()
        self.plot_settings.set_plot_settings(font_family='arial',
                                             fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'gray'})

    def _get_plots_path(self):
        current_dir = os.getcwd()
        plots_dir = os.path.join(current_dir, "src",  "plots")
        return plots_dir

    def _generate_id(self):
        current_time = str(int(time.time()))
        random_str = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        return current_time + '_' + random_str
