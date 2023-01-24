import telebot
from .environment import get_from_env

BOT_TOKEN = get_from_env("BOT_TOKEN")
bot = telebot.TeleBot(token=BOT_TOKEN)
