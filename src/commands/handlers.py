
from .analysis_commands_factory import AnalysisCommandFactory
from configs.bot import bot
from commands.texts import start_message, help_message


@bot.message_handler(commands=['start'])
def start_command(message):
    name = message.chat.first_name
    bot.send_message(message.chat.id, start_message.format(name))


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['single_asset', 'assets_group', 'asset_behavior'])
def analysis(message):
    command = AnalysisCommandFactory.create_command(bot=bot, message=message)
    command.proccese()
