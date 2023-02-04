from ts3API.TS3Connection import TS3Connection
import ts3API.Events as Events
import telebot
import os

# TeamSpeak
HOST = os.environ.get("TS_HOST")
PORT = os.environ.get("TS_PORT")
USER = os.environ.get("TS_USER")
PASS = os.environ.get("TS_PWD")
DEFAULTCHANNEL = os.environ.get("TS_CHANNEL")
SID = 1

# Telegram
TOKEN = os.environ.get("TG_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")

TELEGRAM_BOT = telebot.TeleBot(TOKEN, parse_mode=None)
ONLINE_USERS = {}


@TELEGRAM_BOT.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    TELEGRAM_BOT.reply_to(message, "Hello :)")


def send_tg_message(message):
    TELEGRAM_BOT.send_message(CHAT_ID, message)


def on_ts_event(sender, **kw):
    event = kw["event"]
    if isinstance(event, Events.ClientEnteredEvent):
        msg = event.client_nickname + " si è connesso a teamspeak"
        send_tg_message(msg)
        ONLINE_USERS[str(event.clid)] = event.client_nickname
    if isinstance(event, Events.ClientLeftEvent):
        try:
            msg = ONLINE_USERS.pop(str(event.client_id)) + \
                " si è disconnesso da teamspeak"
        except KeyError:
            msg = "Sconosciuto è uscito da teamspeak"
        send_tg_message(msg)


def ts3BotConnect():
    ts3conn = TS3Connection(HOST, PORT)
    ts3conn.login(USER, PASS)
    ts3conn.use(sid=SID)
    ts3conn.register_for_server_events(on_ts_event)
    ts3conn.register_for_private_messages(on_ts_event)
    ts3conn.start_keepalive_loop()


def main():
    print("Starting bot...")
    ts3BotConnect()
    TELEGRAM_BOT.infinity_polling()


if __name__ == '__main__':
    main()
