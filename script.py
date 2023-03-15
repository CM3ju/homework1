import requests
import pandas

URL = 'https://pypi.org/search/'


class Web:
    def __init__(self, url=URL):
        self.url = url
        self.status = None

    def get_status(self):
        status = requests.request('GET', self.url)
        self.status = status
        status = int(str(status).split(" ")[1][1:-2])
        if status == 200:
            print('request successful')
            print(f'url is: {self.url}')
        else:
            print(f'request failed your response is: {status}')
        return self.status

    def get_content(self):
        content = requests.get(self.url)
        return content.text




a = Web().get_content()
print(a)
