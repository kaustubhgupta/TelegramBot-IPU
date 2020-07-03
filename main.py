from flask import Flask, request
import telegram
from credentials import bot_token, URL
from ipuAPI import IPUApi

api = IPUApi()
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    if text == "/start":
        bot_welcome = """
        *Welcome to IPU Results Checker Portal!*' + '\n\nTo get your results, input the query as following format:\n*EnrollmentNumber  BatchNumber  Semester*\n' + 'For example,\n12345678910 18 2\nIt would give results for 2018-2022 batch 2nd semester results
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    if len(text) < 16:
        error_message = """
        *Input given in wrong format!*' + "\nYou need to input as:\n*EnrollmentNumber BatchNumber Semester*
        """
        return bot.sendMessage(chat_id=chat_id, text=error_message, reply_to_message_id=msg_id)

    else:
        msg = text.split(' ')
        ans = api.getMarks(enrollNum=msg[0], batch=msg[1], semester=msg[2])
        if ans is not None:
            marks = ' '.join([' '.join(i) + str('\n') for i in
                              [[j.strip() for j in i.split('  ') if j != ''] for i in ans[0].split('\n')[1:]]])
            to_send = "*MARKS SUMMARY Semester-*" + str(msg[2]) + str('\n') + "Name: " + str(ans[4]) + str(
                '\n') + "Enrollment Number: " + str(ans[5]) + str('\n') + "College: " + str(ans[1]) + str('\n') + str(
                "Branch: ") + str(ans[2]) + str('\n') + "Percentage: " + str(ans[10]) + str(
                '%\n') + "College Rank :{}/{}".format(ans[6], ans[7]) + str('\n') + "University Rank :{}/{}\n".format(
                ans[8], ans[9]) + '\nMarks Format\n*Subject  Internal  External  Total*\n\n\n' + marks
            return bot.sendMessage(chat_id=chat_id, text=to_send, reply_to_message_id=msg_id)
        else:
            error_message2 = """
            *Error! Possible Reasons:*\n1. Wrong enrollment number or combination selected\n2. Result not available in our database
            """
            return bot.sendMessage(chat_id=chat_id, text=error_message2, reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(URL)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
