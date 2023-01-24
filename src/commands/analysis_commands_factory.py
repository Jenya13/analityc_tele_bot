from .single_asset_analysis import SingleAssetAnalysis
from .assets_group_analysis import AssetGroupAnalysis


class AnalysisCommandFactory:
    @staticmethod
    def create_command(bot, message):
        if message.text == '/single_asset':
            return SingleAssetAnalysis(bot, message)
        elif message.text == '/assets_group':
            return AssetGroupAnalysis(bot, message)
        # elif message.text == '/portfolio':
        #     return PortfolioAnalysis(bot, message)
        else:
            return None
