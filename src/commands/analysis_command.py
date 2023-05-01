import re
from datetime import datetime, date


class Command:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self._user_data = {}

    @staticmethod
    def stop_command(func):
        def wrapper(self, message):
            if message.text == '/stop':
                return
            return func(self, message)
        return wrapper

    def valid_dates(self, dates: str):
        limit_date = "2000-01-01"

        dates = dates.split("-")

        if len(dates) != 2:
            raise ValueError("Wrong format of the date, try YYYY-MM-DD")

        start_date_str = dates[0].replace("/", "-")
        end_date_str = dates[1].replace("/", "-")

        match_start_date = re.match(r'^\d{4}-\d{2}-\d{2}$', start_date_str)
        match_end_date = re.match(r'^\d{4}-\d{2}-\d{2}$', end_date_str)

        if not match_start_date or not match_end_date:
            raise ValueError("Wrong format of dates, try YYYY-MM-DD")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        except ValueError:
            raise ValueError("Incorect dates")
        else:

            limit_date = datetime.strptime(limit_date, '%Y-%m-%d')
            today_date = datetime.now()

            if start_date < limit_date or end_date < limit_date:
                raise ValueError("Start or end date lower than 2000-01-01")

            if start_date > today_date or end_date > today_date:
                raise ValueError("Start or end date greater then current date")

            return [start_date_str, end_date_str]

    def is_start_date_smaller(self, start_time: str, end_time: str):
        start_time = date.fromisoformat(start_time)
        end_time = date.fromisoformat(end_time)
        if start_time < end_time:
            return True
        else:
            return False

    def proccese(self):
        pass
