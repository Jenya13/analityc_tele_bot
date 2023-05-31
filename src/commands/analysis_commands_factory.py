from .single_asset_analysis import SingleAssetAnalysis
from .assets_group_analysis import AssetGroupAnalysis
from .assets_behavior_analysis import AssetBehaviorAnalysis


class AnalysisCommandFactory:
    @staticmethod
    def create_command(bot, message):
        if message.text == '/single_asset':
            return SingleAssetAnalysis(bot, message)
        elif message.text == '/assets_group':
            return AssetGroupAnalysis(bot, message)
        elif message.text == '/asset_behavior':
            return AssetBehaviorAnalysis(bot, message)
        else:
            return None
