import requests
import json


class IPUApi:

    def __init__(self):
        self.baseurl = "http://127.0.0.1:5000/"

    def getMarks(self, enrollNum):
        url = self.baseurl + 'api?rollNo={}'.format(enrollNum)
        r = requests.get(url)
        return json.loads(r.content)
