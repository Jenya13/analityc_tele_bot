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

    def is_valid_date(self, date: str):
        limit_date = "2000-01-05"
        match = re.match(r'^\d{4}-\d{2}-\d{2}$', date)
        if not match:
            raise ValueError("Wrong format of the date, try YYYY-MM-DD")

        try:
            datetime.strptime(date, "%Y-%m-%d")

        except ValueError:
            raise ValueError("Incorect date")
        else:
            date = datetime.strptime(date, '%Y-%m-%d')
            limit_date = datetime.strptime(limit_date, '%Y-%m-%d')
            if date < limit_date:
                raise ValueError("Date lower than 1995-01-01")
            return True

    def is_start_date_smaller(self, start_time: str, end_time: str):
        start_time = date.fromisoformat(start_time)
        end_time = date.fromisoformat(end_time)
        if start_time < end_time:
            return True
        else:
            return False

    def proccese(self):
        pass
