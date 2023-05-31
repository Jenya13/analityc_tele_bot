
import os
import pandas as pd
import yfinance as yf
import telebot
from providers.yfinance_provider import YFinanceProvider
from .analysis_command import Command
from analysis.assets_group_visualization import AssetsDataVisualization


class AssetGroupAnalysis(Command):

    def __init__(self, bot, message) -> None:
        super().__init__(bot, message)
        self._user_data = {"ticker": [], "start_time": "", "end_time": ""}
        self._data = pd.DataFrame()

    def proccese(self):
        # self._assets_group(self.message)
        self.test(self.message)

    @Command.stop_command
    def _assets_group(self, message):

        self.message = message
        self.bot.send_message(self.message.chat.id,
                              "Tickers symbols:")
        self.bot.register_next_step_handler(
            self.message, self._get_assets_name)

    @Command.stop_command
    def _get_assets_name(self, message):

        self.message = message

        tickers: str = self.message.text
        tickers_list = tickers.split(',')
        tickers_list = [ticker.upper().strip() for ticker in tickers_list]

        for ticker in tickers_list:
            info = yf.Ticker(ticker).info
            if info["trailingPegRatio"] is None:
                tickers_list.remove(ticker)

        if len(tickers_list) < 2:
            self.bot.send_message(
                self.message.chat.id, "Only one ticker provided or Symbol not found or may be delisted")
            self._assets_group(self.message)

        else:
            self._user_data["tickers"] = tickers_list
            self.bot.send_message(
                self.message.chat.id, "Start-End dates (YYYY/MM/DD-YYYY/MM/DD):")
            self.bot.register_next_step_handler(
                self.message, self._get_start_end_dates)

    @Command.stop_command
    def _get_start_end_dates(self, message):

        self.message = message

        start_end_dates: str = self.message.text
        try:
            start_end_dates = super().valid_dates(start_end_dates)
            start_date = start_end_dates[0]
            end_date = start_end_dates[1]

        except ValueError as err:
            self._user_data["start_time"] = ""
            self._user_data["end_time"] = ""
            self.bot.send_message(
                self.message.chat.id, err)
            self.bot.send_message(
                self.message.chat.id, "Start-End dates (YYYY/MM/DD-YYYY/MM/DD):")
            self.bot.register_next_step_handler(
                self.message, self._get_start_end_dates)
        self._user_data["start_time"] = start_date
        self._user_data["end_time"] = end_date
        if not super().is_start_date_smaller(self._user_data["start_time"], self._user_data["end_time"]):
            self._user_data["start_time"] = ""
            self._user_data["end_time"] = ""
            self.bot.send_message(
                self.message.chat.id, "Start date bigger than end date")
            self.bot.send_message(
                self.message.chat.id, "Start-End dates (YYYY/MM/DD-YYYY/MM/DD):")
            self.bot.register_next_step_handler(
                self.message, self._get_start_end_dates)
        else:
            self._perform_analytical_analysis(self.message)

    def _perform_analytical_analysis(self, message):
        print('analytical analysis')

    def test(self, message):
        self._user_data = {"tickers": ['AAPL', 'JPM', 'GC=F', 'MA'
                                       ], "start_time": "2019-03-01", "end_time": "2022-03-01"}
        sp500_ticker = '^GSPC'
        if sp500_ticker not in self._user_data["tickers"]:
            self._user_data["tickers"].append(sp500_ticker)

        provider = YFinanceProvider()
        assets_data = provider.get_symbols_history(
            self._user_data["tickers"], self._user_data["start_time"], self._user_data["end_time"])

        assets_data = assets_data['Close']

        assets_vizualization = AssetsDataVisualization(
            self._user_data["tickers"], self._user_data["start_time"], self._user_data["end_time"], assets_data)

        plots_list = []
        try:
            plots_list.append(assets_vizualization.plot_risk_returns())
            plots_list.append(assets_vizualization.plot_normalized())
            plots_list.append(assets_vizualization.plot_correlation())
            media_group = []
            for plot in plots_list:
                with open(plot, 'rb') as f:
                    plot_data = f.read()
                    media_group.append(
                        telebot.types.InputMediaPhoto(plot_data))
                f.close()
                os.remove(plot)
        except Exception as e:
            # Catch any exceptions that occur during the loop and print an error message
            print(f"An error occurred: {str(e)}")
            # Delete any image files that were created before the exception was raised
            for plot in plots_list:
                if os.path.exists(plot):
                    os.remove(plot)
        else:
            # If no exceptions were raised during the loop, send the media group
            self.bot.send_media_group(
                self.message.chat.id, media=media_group)
        finally:
            # Ensure that all image files are deleted, even if an exception was raised
            for plot in plots_list:
                if os.path.exists(plot):
                    os.remove(plot)
