import requests
import json
import os


class IPUApi:

    def __init__(self):
        self.local = False
        if self.local:
            self.baseurl = "http://127.0.0.1:5000/"
        else:
            self.baseurl = "https://ipuresultskg.herokuapp.com/"

    def token(self):
        if self.local:
            url = self.baseurl + 'getToken'
        else:
            url = self.baseurl + 'getToken?key={}'.format(os.environ.get('Service'))
        r = requests.get(url)
        return json.loads(r.content)

    def getMarks(self, enrollNum, batch, semester, token):
        url = self.baseurl + 'api?rollNo={}&batch={}&semester={}&token={}'.format(enrollNum, batch, semester, token)
        r = requests.get(url)
        return json.loads(r.content)
