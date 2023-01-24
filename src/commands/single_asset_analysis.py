
import yfinance as yf
from providers.yfinance_provider import YFinanceProvider
from .analysis_command import Command


class SingleAssetAnalysis(Command):
    def __init__(self, bot, message):
        super().__init__(bot, message)

    def proccese(self):
        self._single_asset(self.message)

    @Command.stop_command
    def _single_asset(self, message):

        self.message = message
        self.bot.send_message(self.message.chat.id,
                              "What is the ticker symbol?")
        self.bot.register_next_step_handler(self.message, self._get_asset_name)

    @Command.stop_command
    def _get_asset_name(self, message):

        self.message = message
        if "ticker" in self._user_data:
            self.bot.send_message(
                self.message.chat.id, "What is the start time (YYYY-MM-DD) ?")
            self.bot.register_next_step_handler(
                self.message, self._get_start_time)

        else:
            ticker: str = self.message.text
            ticker = ticker.upper().strip()
            info = yf.Ticker(ticker).info
            if info is None:
                self.bot.send_message(
                    self.message.chat.id, "Symbol not found or may be delisted")
                self._single_asset(self.message)
            else:
                self._user_data["ticker"] = ticker
                self.bot.send_message(
                    self.message.chat.id, "What is the start time (YYYY-MM-DD) ?")
                self.bot.register_next_step_handler(
                    self.message, self._get_start_time)

    @Command.stop_command
    def _get_start_time(self, message):

        self.message = message
        if "start_time" in self._user_data:
            self.bot.send_message(
                self.message.chat.id, "What is the end time (YYYY-MM-DD) ?")
            self.bot.register_next_step_handler(
                self.message, self._get_end_time)
        else:
            start_time = self.message.text
            try:
                super().is_valid_date(start_time)
            except ValueError as err:
                self.bot.send_message(
                    self.message.chat.id, err)
                self._get_asset_name(self.message)
            else:
                self._user_data["start_time"] = start_time
                self.bot.send_message(
                    self.message.chat.id, "What is the end time (YYYY-MM-DD) ?")
                self.bot.register_next_step_handler(
                    self.message, self._get_end_time)

    @Command.stop_command
    def _get_end_time(self, message):

        self.message = message
        end_time = self.message.text
        try:
            super().is_valid_date(end_time)
        except ValueError as err:
            self.bot.send_message(
                self.message.chat.id, err)
            self._get_start_time(self.message)
        else:
            self._user_data["end_time"] = end_time
            if not super().is_start_date_smaller(self._user_data["start_time"], self._user_data["end_time"]):
                self.bot.send_message(
                    self.message.chat.id, "Start date bigger than end date")
                self._get_asset_name(self.message)
            else:
                self._perform_analytical_analysis(self.message)

    def _perform_analytical_analysis(self, message):
        self.bot.send_message(self.message.chat.id, "Asset data received: \n"
                              "Ticker: {}\n"
                              "Start Time: {}\n"
                              "End Time: {}".format(self._user_data["ticker"], self._user_data["start_time"], self._user_data["end_time"]))
        self.message = message
        print('in perform analysis')

        # provider = YFinanceProvider()
        # data = provider.get_symbols_history("AAPL", "2022-01-01", "2022-12-31")
        # print(data)
        # bot.send_message(message.chat.id, 'in single')
