import os
import re
import telegram
import requests
from time import sleep
from flask import Flask, request
from functions import marksImage

app = Flask(__name__)

TELEBOT_TOKEN = os.environ["APIKEY"]
IPU_API_KEY = os.environ['IPU_API_KEY']


@app.route(f"/{TELEBOT_TOKEN}", methods=['GET', 'POST'])
def webhook():

    bot = telegram.Bot(token=TELEBOT_TOKEN)
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id
        text = update.message.text
        if text == '/start':
            message = 'Welcome to IPU Results Bot!' + '\n\nTo get your results, input the query as following format:\n<b>EnrollmentNumber  BatchNumber  Semester</b>\n\n' + \
                'For example,\n<b>12345678910 18 2</b>\n\nIt would give results for 2018-2022 batch 2nd semester results'
            bot.sendChatAction(chat_id=chat_id, action="typing")
            sleep(0.7)
            bot.sendMessage(chat_id=chat_id, text=message, parse_mode='HTML')
            return 'ok'

        elif len(re.findall(r'\d+', text)) == 0:
            message = 'Why are you sending random text? Please input the query as suggested. Forgot the pattern? Type /start'
            bot.sendChatAction(chat_id=chat_id, action="typing")
            sleep(0.7)
            bot.sendMessage(chat_id=chat_id, text=message)
            return 'ok'
        elif len(text) != 16:
            message = '<b>Wrong Input Format!</b>\n' + \
                "\nYou need to provide input as:\n<b>EnrollmentNumber BatchNumber Semester</b>\n\nForgot the pattern? Type /start"
            bot.sendChatAction(chat_id=chat_id, action="typing")
            sleep(0.7)
            bot.sendMessage(chat_id=chat_id, text=message, parse_mode='HTML')
            return 'ok'

        else:
            msg = text.split(' ')
            if len(msg) != 3:
                message = '<b>Wrong Input Format!</b>\n' + \
                    "\nYou need to provide input as:\n<b>EnrollmentNumber BatchNumber Semester</b>\nForgot the pattern? Type /start"
                bot.sendChatAction(chat_id=chat_id, action="typing")
                sleep(0.7)
                bot.sendMessage(chat_id=chat_id, text=message,
                                parse_mode='HTML')
                return 'ok'
            else:
                url = "https://ipuresultskg.herokuapp.com/api/v1/fetchscore?eNumber={}&semester={}&batch={}".format(
                    msg[0], msg[2], msg[1])
                headers = {
                    'Authorization': 'Bearer {}'.format(IPU_API_KEY)
                }
                received = requests.request("GET", url, headers=headers)
                data = received.json()
                if data['result'] is not None:
                    bot.sendChatAction(chat_id=chat_id, action="typing")
                    sleep(0.6)
                    to_send = "Semester-{}".format(msg[2]) + str('\n') + "Name: " + str(data['result']['name']) + str(
                        '\n') + "Enrollment Number: " + str(data['result']['enroll_num']) + str('\n') + "College: " + str(data['result']['college_name']) + str('\n') + str(
                        "Branch: ") + str(data['result']['branch_name']) + str('\n') + "Percentage: " + str(data['result']['percentage']) + str(
                        '%\n') + "SGPA: " + str(data['result']['sgpa']) + str('\n') + "College Overall Rank :{}/{}".format(data['result']['ranks']['college_rank'], data['result']['ranks']['college_total']) + str('\n') + "College Branch Rank :{}/{}".format(data['result']['ranks']['college_branch_rank'], data['result']['ranks']['college_branch_total']) + str('\n') + "University Rank :{}/{}".format(data['result']['ranks']['uni_rank'], data['result']['ranks']['uni_total']) + str('\n') + "University Branch Rank :{}/{}".format(data['result']['ranks']['uni_branch_rank'], data['result']['ranks']['uni_branch_total'])
                    marks = [[i, j, k, z, t] for i, j, k, z, t in zip(data['result']['subjects'], data['result']['int_marks'],
                                                                      data['result']['ext_marks'], data['result']['total_marks'], data['result']['grade_points'])]
                    bot.sendMessage(chat_id=chat_id, text=to_send)

                    bot.sendChatAction(chat_id=chat_id, action="upload_photo")
                    marksImage(marks, str(chat_id))
                    with open(f'marks_image_{chat_id}.png', 'rb') as file:
                        bot.sendPhoto(chat_id=chat_id, photo=file)
                    os.remove(f'marks_image_{chat_id}.png')
                    return 'ok'
                else:
                    send = "<b>Error! Possible Reasons:</b>\n\n1. Wrong enrollment number or combination selected\n2. Result not available in our database"
                    bot.sendChatAction(chat_id=chat_id, action="typing")
                    sleep(0.6)
                    bot.sendMessage(chat_id=chat_id, text=send,parse_mode="HTML")
                    return 'ok'

    return 'error'


if __name__ == '__main__':
    app.run(debug=True)
