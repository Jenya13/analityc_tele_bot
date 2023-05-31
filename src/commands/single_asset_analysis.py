import os
import yfinance as yf
import telebot
from providers.yfinance_provider import YFinanceProvider
from analysis.asset_analysis import SingleAssetTechnicalAnalysis
from analysis.single_asset_visualization import SingleAssetDataVisualization
from .analysis_command import Command
from .texts import single_asset_analitics_text, single_asset_returns_text


class SingleAssetAnalysis(Command):

    def __init__(self, bot, message):
        super().__init__(bot, message)
        self._user_data = {"ticker": "", "start_time": "", "end_time": ""}

    def proccese(self):
        self._single_asset(self.message)

    @Command.stop_command
    def _single_asset(self, message):

        self.message = message
        self.bot.send_message(self.message.chat.id,
                              "Ticker symbol:")
        self.bot.register_next_step_handler(self.message, self._get_asset_name)

    @Command.stop_command
    def _get_asset_name(self, message):

        self.message = message

        ticker: str = self.message.text
        ticker = ticker.upper().strip()
        info = yf.Ticker(ticker).info

        if info["trailingPegRatio"] is None:
            self._user_data["ticker"] = ""
            self.bot.send_message(
                self.message.chat.id, "Symbol not found or may be delisted")
            self._single_asset(self.message)
        else:
            self._user_data["ticker"] = ticker
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

        provider = YFinanceProvider()
        data = provider.get_symbol_history(
            self._user_data["ticker"], self._user_data["start_time"], self._user_data["end_time"])

        benchmark = provider.get_symbol_history(
            '^GSPC', self._user_data["start_time"], self._user_data["end_time"])

        single_asset = SingleAssetTechnicalAnalysis(
            self._user_data["ticker"], self._user_data["start_time"], self._user_data["end_time"], data, benchmark)

        drawdown = single_asset.calc_drawdown()
        sharp = single_asset.calc_sharp()
        sortino = single_asset.calc_sortino()
        beta = single_asset.calc_beta()
        alpha = single_asset.calc_alpha()
        mean_return = single_asset.mean_return()
        std_return = single_asset.std_return()
        skew = single_asset.calc_skew()
        kurtosis = single_asset.calc_kurtosis()
        anualized_perf = single_asset.annualized_performence()

        analitic_text = single_asset_analitics_text.format(
            self._user_data["ticker"], self._user_data["start_time"], self._user_data["end_time"], drawdown, sharp, sortino, alpha, beta, skew, kurtosis, anualized_perf[0], anualized_perf[1])

        self.bot.send_message(
            message.chat.id, text=analitic_text, parse_mode='Markdown')

        asset_data = single_asset.get_asset_data()

        asset_visualization = SingleAssetDataVisualization(
            self._user_data["ticker"], self._user_data["start_time"], self._user_data["end_time"], asset_data)

        plots_list = []
        try:
            plots_list.append(asset_visualization.plot_price())
            plots_list.append(
                asset_visualization.plot_normalized(benchmark=benchmark))
            plots_list.append(asset_visualization.plot_returns())
            plots_list.append(asset_visualization.plot_returns('hist'))
            plots_list.append(asset_visualization.plot_drawdown())
            plots_list.append(asset_visualization.plot_top5_drawdown())
            plots_list.append(
                asset_visualization.plot_cum_returns(benchmark=benchmark))

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
