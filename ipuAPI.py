import requests
import json


class IPUApi:

    def __init__(self):
        #self.baseurl = "http://127.0.0.1:5000/"
        self.baseurl = "https://ipuresultskg.herokuapp.com/"

    def getMarks(self, enrollNum, batch, semester):
        url = self.baseurl + 'api?rollNo={}&batch={}&semester={}'.format(enrollNum, batch, semester)
        r = requests.get(url)
        return json.loads(r.content)
