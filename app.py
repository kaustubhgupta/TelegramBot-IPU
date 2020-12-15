import os
import telegram
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])

def webhook():
    bot = telegram.Bot(token=os.environ["APIKEY"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id
        text = update.message.text
        if text == '/start':
            message = '*Welcome to IPU Results Checker Portal!*' + '\n\nTo get your results, input the query as following format:\n*EnrollmentNumber  BatchNumber  Semester*\n' + \
                'For example,\n12345678910 18 2\nIt would give results for 2018-2022 batch 2nd semester results'
            bot.sendMessage(chat_id=chat_id, text=message)
            return 'ok'

        elif len(text) != 16:
            message = '*Input given in wrong format!*' + \
                "\nYou need to input as:\n*EnrollmentNumber BatchNumber Semester*"
            bot.sendMessage(chat_id=chat_id, text=message)
            return 'ok'

        else:
            msg = text.split(' ')
            if len(msg) != 3:
                message = '*Input given in wrong format!*' + \
                    "\nYou need to input as:\n*EnrollmentNumber BatchNumber Semester*"
                bot.sendMessage(chat_id=chat_id, text=message)
                return 'ok'
            else:
                url = "https://ipubackendapi.herokuapp.com/score?eNumber={}&semester={}&batch={}".format(
                    msg[0], msg[2], msg[1])
                headers = {
                    'Authorization': 'Bearer {}'.format(os.environ['IPU_API_KEY'])
                }
                received = requests.request("GET", url, headers=headers)
                if received['result'] is not None:
                    bot.sendMessage(chat_id=chat_id, text=received)
                    return 'ok'
                else:
                    send = "*Error! Possible Reasons:*\n1. Wrong enrollment number or combination selected\n2. Result not available in our database"
                    bot.sendMessage(chat_id=chat_id, text=send)
                    return 'ok'

    return 'error'


def index():
    return webhook()
