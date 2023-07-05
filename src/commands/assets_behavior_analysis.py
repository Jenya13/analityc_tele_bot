
import os
from datetime import datetime, timedelta
import yfinance as yf
from telebot import types
from providers.yfinance_provider import YFinanceProvider
from .analysis_command import Command


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
            self.bot.register_callback_query_handler(
                self.handle_callback_query, func=lambda call: True)
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
            self._single_asset(self.message)
        else:
            self._user_data["ticker"] = ticker
            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text="1 Year", callback_data="1")
            btn2 = types.InlineKeyboardButton(text="2 Year", callback_data="2")
            btn3 = types.InlineKeyboardButton(text="4 Year", callback_data="4")
            btn4 = types.InlineKeyboardButton(text="6 Year", callback_data="6")
            btn5 = types.InlineKeyboardButton(text="8 Year", callback_data="8")
            btn6 = types.InlineKeyboardButton(
                text="10 Year", callback_data="10")
            keyboard.row(btn1, btn2)
            keyboard.row(btn3, btn4)
            keyboard.row(btn5, btn6)
            self.bot.send_message(
                self.message.chat.id, "Range of years to analyze:", reply_markup=keyboard)

    def handle_callback_query(self, call):
        try:
            selected_option = call.data
            current_datetime = datetime.now()
            end_time_str = current_datetime.strftime("%Y-%m-%d")
            start_time = current_datetime - \
                timedelta(days=int(selected_option)*365)
            start_time_str = start_time.strftime('%Y-%m-%d')
            self._user_data["end_time"] = end_time_str
            self._user_data["start_time"] = start_time_str
            self._perform_behavior_analysis(self.message)
        except Exception as e:
            # Handle the exception/error
            print("An error occurred in handle_callback_query:", str(e))

    def _perform_behavior_analysis(self, message):
        self.message = message
        print('Ticker: {}, start: {}, end {}'.format(
            self._user_data["ticker"], self._user_data["start_time"], self._user_data["end_time"]))
