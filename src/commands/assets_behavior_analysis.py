from .analysis_command import Command


class AssetBehaviorAnalysis(Command):

    def __init__(self, bot, message):
        super().__init__(bot, message)
        self._user_data = {"ticker": "", "start_time": "", "end_time": ""}

    def proccese(self):
        pass
