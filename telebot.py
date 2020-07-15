import requests
import json
import configparser as cfg
import os


class TelegramBot:

    def __init__(self, config):
        self.token = os.environ.get('authkey')
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset+1)

        r = requests.get(url)

        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + 'sendMessage?chat_id={}&text={}&parse_mode=Markdown'.format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def send_action(self, chat_id):
        url = self.base + 'sendChatAction?chat_id={}&action=TYPING'.format(chat_id)
        requests.get(url)
