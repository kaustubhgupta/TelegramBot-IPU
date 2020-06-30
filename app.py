from telebot import TelegramBot
from ipuAPI import IPUApi
import json
import requests


update_id = None
bot = TelegramBot(config='config.cfg')
api = IPUApi()


def give_results(msg):
    if msg is not None:
        ans = api.getMarks(enrollNum=msg)
        print(ans)
        return ans


while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for i in updates:
            update_id = i['update_id']
            try:
                message = i['message']['text']
            except:
                message = None
            sender = i['message']['from']['id']
            reply = give_results(message)
            bot.send_message(msg=reply, chat_id=sender)
