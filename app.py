from telebot import TelegramBot
from ipuAPI import IPUApi
import pandas as pd
import json
import requests


update_id = None
bot = TelegramBot(config='config.cfg')
api = IPUApi()


def give_results(msg):
    if msg is not None:
        if msg == '/start':
            return '*Welcome to IPU Results Checker Portal!*'

        else:
            msg = msg.split(' ')
            ans = api.getMarks(enrollNum=msg[0], batch=msg[1], semester=msg[2])
            #temp = json.loads(msg[0])
            #marks = temp
            to_send = "*MARKS SUMMARY Semester-*" + str(msg[2]) + str('\n') + "Name: "+ str(ans[4]) + str('\n') + "Enrollment Number: "+ str(ans[5]) + str('\n') + "College: " + str(ans[1]) + str('\n') + str("Branch: ") + str(ans[2])+ str('\n') + "Percentage: " + str(ans[10])

            print(to_send)
            return to_send


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
