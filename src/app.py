import flask
from flask import Flask, request, Response
import telebot
from configs.environment import get_from_env
from commands.handlers import bot

BOT_TOKEN: str = get_from_env("BOT_TOKEN")
WEBHOOK_URL: str = get_from_env("WEBHOOK_URL").format(BOT_TOKEN)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def process():

    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(
            request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return {"ok": True}
    else:
        flask.abort(403)


@app.route('/health', methods=["GET"])
def health():
    return Response(response='Server is running', status=200)


if __name__ == '__main__':
    app.run()
