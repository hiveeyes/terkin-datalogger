#!/usr/bin/python3 -u

# CONFIG START
telegram_bot_token = "TOKEN"
tg_user_id = TELEGRAM_USER_ID
app_id     = "TTN_APP_ID"
access_key = "TTN_ACCESS_KEY"
dev_id     = "TTN_DEV_ID"
conf       = True # confirmed downlinks
# CONFIG END

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import ttn
import logging
import base64
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Starting Terkin Control Bot')

bot = telegram.Bot(token=telegram_bot_token)

updater = Updater(token=telegram_bot_token, use_context=True)

dispatcher = updater.dispatcher

updater.start_polling()

handler = ttn.HandlerClient(app_id, access_key)
mqtt_client = handler.data()

# initial bot message after /start command
def start(update, context):
    message = "I'm the Terkin Control bot, please command me! Your chat_id is " + str(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

start_handler = CommandHandler('start', start, Filters.user(user_id=tg_user_id))
dispatcher.add_handler(start_handler)

# TTN callback functions
def connect_callback(res, client):
    if res:
        logging.info('[connect_callback] (Re)connected to TTN broker')
    else:
        logging.info('[connect_callback] (Re)connecting to TTN broker failed')
        bot.send_message(chat_id=tg_user_id, text="(Re)connecting to TTN broker failed")

def close_callback(res, client):
    if res:
        logging.info('[close_callback] Successfully disconnected from TTN broker')
    else:
        logging.info('[close_callback] Lost connection to TTN broker')
        mqtt_client.connect()

def uplink_callback(msg, client):
    logging.info('[uplink_callback] Uplink received from %s', msg.dev_id)

# not triggered by the framework at the moment
def downlink_callback(msg, client):
    logging.info('[downlink_callback] Downlink sent to %s', msg.dev_id)
    bot.send_message(chat_id=tg_user_id, text="(Downlink sent)")

# TTN callbacks
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.set_downlink_callback(downlink_callback)
mqtt_client.set_connect_callback(connect_callback)
mqtt_client.set_close_callback(close_callback)

# connect to TTN MQTT broker on startup
mqtt_client.connect()

# command handler functions
def sleep(update, context):
    if len(context.args) == 1:
        if 1 <= int(context.args[0]) <= 255:
            payload = base64.b64encode(bytes([int(context.args[0])])).decode()
            mqtt_client.connect()
            time.sleep(2)
            logging.info('[sleep] Sending new DEEP_SLEEP interval as payload "%s" on port 1', payload)
            mqtt_client.send(dev_id=dev_id, pay=payload, port=1, conf=conf, sched="replace")
            message = 'unit *' + dev_id + '* will deep sleep for ' + context.args[0] + ' minute(s) (after next uplink)'
        else:
            message = 'Chose a deep sleep interval between 1 and 255 minutes!'
    else:
        payload = base64.b64encode(bytes([0])).decode()
        mqtt_client.connect()
        time.sleep(2)
        logging.info('[sleep] Sending SLEEP command payload "%s" on port 1', payload)
        mqtt_client.send(dev_id=dev_id, pay=payload, port=1, conf=conf, sched="replace")
        message = 'unit *' + dev_id + '* returns to default deep sleep interval (after next uplink)'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

def pause(update, context):
    payload = base64.b64encode(bytes([1])).decode()
    mqtt_client.connect()
    time.sleep(2)
    logging.info('[pause] Sending Pause command as payload "%s" on port 2', payload)
    mqtt_client.send(dev_id=dev_id, pay=payload, port=2, conf=conf, sched="replace")
    message = 'unit *' + dev_id + '* will pause data submission (after next uplink)'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

def unpause(update, context):
    payload = base64.b64encode(bytes([0])).decode()
    mqtt_client.connect()
    time.sleep(2)
    logging.info('[unpause] Sending Unpause command as payload "%s" on port 2', payload)
    mqtt_client.send(dev_id=dev_id, pay=payload, port=2, conf=conf, sched="replace")
    message = 'unit *' + dev_id + '* should continue data submission (after next uplink)'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')

#define command handlers
sleep_handler = CommandHandler('sleep', sleep, Filters.user(user_id=tg_user_id), pass_args=True)
dispatcher.add_handler(sleep_handler)

pause_handler = CommandHandler('pause', pause, Filters.user(user_id=tg_user_id), pass_args=False)
dispatcher.add_handler(pause_handler)

unpause_handler = CommandHandler('unpause', unpause, Filters.user(user_id=tg_user_id), pass_args=False)
dispatcher.add_handler(unpause_handler)
