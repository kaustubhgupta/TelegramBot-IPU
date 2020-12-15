import os
import telegram
import requests
import pandas as pd
from time import sleep
from flask import Flask, request
from telegram import ParseMode

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
            bot.sendChatAction(chat_id=chat_id, action="typing")
            sleep(1)
            bot.sendMessage(chat_id=chat_id, text=message)
            return 'ok'

        elif len(text) != 16:
            message = '*Input given in wrong format!*' + \
                "\nYou need to input as:\n*EnrollmentNumber BatchNumber Semester*"
            bot.sendChatAction(chat_id=chat_id, action="typing")
            sleep(1)
            bot.sendMessage(chat_id=chat_id, text=message)
            return 'ok'

        else:
            msg = text.split(' ')
            if len(msg) != 3:
                message = '*Input given in wrong format!*' + \
                    "\nYou need to input as:\n*EnrollmentNumber BatchNumber Semester*"
                bot.sendChatAction(chat_id=chat_id, action="typing")
                sleep(1)
                bot.sendMessage(chat_id=chat_id, text=message)
                return 'ok'
            else:
                url = "https://ipubackendapi.herokuapp.com/score?eNumber={}&semester={}&batch={}".format(
                    msg[0], msg[2], msg[1])
                headers = {
                    'Authorization': 'Bearer {}'.format(os.environ['IPU_API_KEY'])
                }
                received = requests.request("GET", url, headers=headers)
                data = received.json()
                if data['result'] is not None:
                    bot.sendChatAction(chat_id=chat_id, action="typing")
                    sleep(1)
                    to_send = "Semester-{}".format(msg[2]) + str('\n') + "Name: " + str(data['result']['name']) + str(
                        '\n') + "Enrollment Number: " + str(data['result']['enroll_num']) + str('\n') + "College: " + str(data['result']['college_name']) + str('\n') + str(
                        "Branch: ") + str(data['result']['branch_name']) + str('\n') + "Percentage: " + str(data['result']['percentage']) + str(
                        '%\n') + "SGPA: " + str(data['result']['sgpa']) + str('\n') + "College Overall Rank :{}/{}".format(data['result']['ranks']['college_rank'], data['result']['ranks']['college_total']) + str('\n') + "College Branch Rank :{}/{}".format(data['result']['ranks']['college_branch_rank'], data['result']['ranks']['college_branch_total']) + str('\n') + "University Rank :{}/{}".format(data['result']['ranks']['uni_rank'], data['result']['ranks']['uni_total']) + str('\n') + "University Branch Rank :{}/{}".format(data['result']['ranks']['uni_branch_rank'], data['result']['ranks']['uni_branch_total'])
                    marks = [(i, j, k, z, t) for i, j, k, z, t in zip(data['result']['subjects'], data['result']['int_marks'],
                                                                      data['result']['ext_marks'], data['result']['total_marks'], data['result']['grade_points'])]
                    bot.sendMessage(chat_id=chat_id, text=to_send)
                    df = pd.DataFrame(marks, columns=['Subjects', 'Internals', 'Externals', 'Total', 'Grade Points'])
                    marksData = df.to_markdown()
                    bot.sendMessage(chat_id=chat_id, text=marksData, parse_mode=ParseMode.MarkdownV2)
                    return 'ok'
                else:
                    send = "*Error! Possible Reasons:*\n1. Wrong enrollment number or combination selected\n2. Result not available in our database"
                    bot.sendChatAction(chat_id=chat_id, action="typing")
                    sleep(1)
                    bot.sendMessage(chat_id=chat_id, text=send)
                    return 'ok'

    return 'error'


def index():
    return webhook()
