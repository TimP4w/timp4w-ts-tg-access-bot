from ts3API.TS3Connection import TS3Connection
import ts3API.Events as Events
import telebot
import os
import i18n

# TODO: use env variable to set locale
i18n.load_path.append('translations')
i18n.set('locale', 'it')
i18n.set('fallback', 'en')

# TeamSpeak
HOST = os.environ.get("TS_HOST")
PORT = os.environ.get("TS_PORT")
USER = os.environ.get("TS_USER")
PASS = os.environ.get("TS_PWD")
DEFAULTCHANNEL = os.environ.get("TS_CHANNEL")
SID = 1
TS3_CONN = TS3Connection(HOST, PORT)

# Telegram
TOKEN = os.environ.get("TG_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")
TELEGRAM_BOT = telebot.TeleBot(TOKEN, parse_mode=None)

# App
ONLINE_USERS = {}

def check_env_variables_set():
    env_names = ["TS_HOST", "TS_PORT", "TS_USER", "TS_PWD", "TS_CHANNEL", "TG_TOKEN", "TG_CHAT_ID"]
    for env_name in env_names:
        if (os.environ.get(env_name) == None):
            raise Exception("Missing env variable {name}. Ensure that the variables are all set!".format(name = env_name)) 
            


@TELEGRAM_BOT.message_handler(commands=['start'])
def send_welcome(message):
    TELEGRAM_BOT.reply_to(message, i18n.t('app.greeting'))

@TELEGRAM_BOT.message_handler(commands=['online'])
def send_how_many_online(message):
    all_clients = TS3_CONN.clientlist()
    filtered_clients = filter(lambda client: client['client_type'] == str(0), all_clients)
    clients_nicknames = map(lambda client: client['client_nickname'], list(filtered_clients))
    clients_nicknames_list = list(clients_nicknames)
    msg = "====== {users} ======\n\n".format(users = i18n.t('app.online_users', total = len(clients_nicknames_list)))
    for nickname in clients_nicknames_list:
        msg = msg + "    🟢    " + nickname + "\n"
    TELEGRAM_BOT.reply_to(message, msg)

def send_tg_message(message):
    TELEGRAM_BOT.send_message(CHAT_ID, message)


def on_ts_event(sender, **kw):
    event = kw["event"]
    if isinstance(event, Events.ClientEnteredEvent):
        msg = i18n.t('app.connected', name = event.client_nickname)
        send_tg_message(msg)
        ONLINE_USERS[str(event.clid)] = event.client_nickname
    if isinstance(event, Events.ClientLeftEvent):
        try:
            nickname = ONLINE_USERS.pop(str(event.client_id))
        except KeyError:
            nickname = i18n.t('app.unknown')
        msg = i18n.t('app.disconnected', name = nickname)
        send_tg_message(msg)


def init_ts3_bot():
    TS3_CONN.login(USER, PASS)
    TS3_CONN.use(sid=SID)
    TS3_CONN.register_for_server_events(on_ts_event)
    TS3_CONN.register_for_private_messages(on_ts_event)
    TS3_CONN.start_keepalive_loop()


def main():
    print("Starting bot...")
    check_env_variables_set()
    init_ts3_bot()
    TELEGRAM_BOT.infinity_polling()
    send_tg_message("I'm alive!")


if __name__ == '__main__':
    main()
