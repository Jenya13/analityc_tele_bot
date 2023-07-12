
import os
import pytz
import yfinance as yf
import pandas as pd
from functools import partial
from datetime import datetime, timedelta
from telebot import types
from providers.yfinance_provider import YFinanceProvider
from .analysis_command import Command
from analysis.behavior_asset_visualization import BehaviorAssetDataVisualization


class AssetBehaviorAnalysis(Command):

    def __init__(self, bot, message):
        super().__init__(bot, message)
        self._user_data = {"ticker": "", "start_time": "", "end_time": ""}
        try:
            self.register_handler()
        except Exception as e:
            # Handle the exception/error
            print("An error occurred:", str(e))

    def register_handler(self):
        try:
            # Registering callback query handler
            callback_func = partial(self.handle_callback_query, self)
            self.bot.register_callback_query_handler(
                callback_func, func=lambda call: True)
        except Exception as e:
            # Handle the exception/error
            print("An error occurred:", str(e))

    def process(self):
        self._asset_behavior(self.message)

    def _asset_behavior(self, message):
        self.message = message
        self.bot.send_message(self.message.chat.id, "Ticker symbol:")
        self.bot.register_next_step_handler(self.message, self._get_asset_name)

    @Command.stop_command
    def _get_asset_name(self, message):
        self.message = message
        ticker: str = self.message.text
        ticker = ticker.upper().strip()
        info = yf.Ticker(ticker).info
        if info["trailingPegRatio"] is None:
            self._user_data["ticker"] = ""
            self.bot.send_message(self.message.chat.id,
                                  "Symbol not found or may be delisted")
            self._asset_behavior(self.message)
        else:
            self._user_data["ticker"] = ticker
            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(
                text="3 Months", callback_data="90")
            btn2 = types.InlineKeyboardButton(
                text="6 Months", callback_data="180")
            btn3 = types.InlineKeyboardButton(
                text="12 Months", callback_data="365")
            btn4 = types.InlineKeyboardButton(
                text="15 Months", callback_data="450")
            btn5 = types.InlineKeyboardButton(
                text="18 Months", callback_data="540")
            btn6 = types.InlineKeyboardButton(
                text="24 Months", callback_data="720")
            keyboard.row(btn1, btn2)
            keyboard.row(btn3, btn4)
            keyboard.row(btn5, btn6)
            self.bot.send_message(
                self.message.chat.id, "Range of years to analyze:", reply_markup=keyboard)

    def handle_callback_query(self, call):
        print('behavior')
        try:
            selected_option = call.data
            current_datetime = datetime.now()
            end_time_str = current_datetime.strftime("%Y-%m-%d")
            start_time = current_datetime - \
                timedelta(days=int(selected_option))
            start_time_str = start_time.strftime('%Y-%m-%d')
            self._user_data["end_time"] = end_time_str
            self._user_data["start_time"] = start_time_str
            self._perform_behavior_analysis(self.message)
        except Exception as e:
            # Handle the exception/error
            print("An error occurred in handle_callback_query:", str(e))

    def _perform_behavior_analysis(self, message):
        self.message = message

        granularity_1h = '1h'
        provider = YFinanceProvider()

        data: pd.DataFrame = provider.get_symbol_history(
            self._user_data["ticker"], self._user_data['start_time'], self._user_data['end_time'], granularity_1h)

        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data['Spread'] = data['High'] - data['Low']
        data['Mid'] = (data['Low']+data['High'])/2
        data['Price Change ABS'] = data['Mid'].diff().abs()
        israel_tz = pytz.timezone('Israel')
        data['il_tz'] = data.index.tz_convert(israel_tz)
        df_data = data.copy()

        analysis = BehaviorAssetDataVisualization(
            self._user_data["ticker"], self._user_data['start_time'], self._user_data['end_time'], df_data)

        plots_list = []
        try:
            plots_list.append(analysis.plot_avg_volume_trade())
            plots_list.append(analysis.plot_avg_volume_trade('1D'))
            plots_list.append(analysis.plot_avg_hourly_spread_trade())
            plots_list.append(analysis.plot_avg_hourly_price_change_trade())
            plots_list.append(analysis.plot_graularity_cover_cost())
            plots_list.append(analysis.plot_graularity_cover_cost('3H'))
            plots_list.append(analysis.plot_graularity_cover_cost('6H'))
            plots_list.append(analysis.plot_graularity_cover_cost('12H'))
            plots_list.append(analysis.plot_graularity_cover_cost('1D'))

            media_group = []
            for plot in plots_list:
                with open(plot, 'rb') as f:
                    plot_data = f.read()
                    media_group.append(
                        types.InputMediaPhoto(plot_data))

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


# def register_handler(self):
#         try:
#             # Register the callback query handler
#             self.bot.register_callback_query_handler(self.handle_callback_query)
#         except Exception as e:
#             # Handle the exception/error
#             print("An error occurred:", str(e))
