from telebot import TelegramBot
from ipuAPI import IPUApi

update_id = None
bot = TelegramBot(config='config.cfg')
api = IPUApi()


def give_results(msg):
    if msg is not None:
        if msg == '/start':
            return '*Welcome to IPU Results Checker Portal!*' + '\n\nTo get your results, input the query as following format:\n*EnrollmentNumber  BatchNumber  Semester*\n' + 'For example,\n12345678910 18 2\nIt would give results for 2018-2022 batch 2nd semester results'

        if len(msg) != 16:
            return '*Input given in wrong format!*' + "\nYou need to input as:\n*EnrollmentNumber BatchNumber Semester*"

        else:
            msg = msg.split(' ')
            if len(msg) != 3:
                return "*Error! Possible Reasons:*\n1. Wrong enrollment number or combination selected\n2. Result not available in our database"
            else:
                ans = api.getMarks(enrollNum=msg[0], batch=msg[1], semester=msg[2])
                if ans is not None:
                    marks = ' '.join([' '.join(i)+str('\n') for i in [[j.strip() for j in i.split('  ') if j != ''] for i in ans[0].split('\n')[1:]]])
                    to_send = "*MARKS SUMMARY Semester-*" + str(msg[2]) + str('\n') + "Name: " + str(ans[4]) + str('\n') + "Enrollment Number: " + str(ans[5]) + str('\n') + "College: " + str(ans[1]) + str('\n') + str("Branch: ") + str(ans[2]) + str('\n') + "Percentage: " + str(ans[10]) + str('%\n') + "College Rank :{}/{}".format(ans[6], ans[7]) + str('\n') + "University Rank :{}/{}\n".format(ans[8], ans[9]) + '\nMarks Format\n*Subject  Internal  External  Total*\n\n\n' + marks
                    return to_send
                else:
                    return "*Error! Possible Reasons:*\n1. Wrong enrollment number or combination selected\n2. Result not available in our database"


while True:
    try:
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
                bot.send_action(chat_id=sender)
                bot.send_message(msg=reply, chat_id=sender)
    except:
        print('Getting No updates!')
