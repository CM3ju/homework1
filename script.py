import requests
from lxml import etree

URL = 'https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3'


class Web:
    def __init__(self, url=URL, save_dir='./'):
        self.url = url
        self.status = None
        self.encoding = None
        self.save_dir = save_dir
        self.content = None

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
        with open('main_page.html', 'w', encoding='utf-8') as f:
            f.write(content.text)
        self.content = content.text

    def decode(self):
        tree = etree.HTML(self.content)
        list_li = tree.xpath('//ul[@class="unstyled"]/li')
        for li in list_li:
            list_herl = li.xpath('./a[@href]')[0]
        print()

a = Web()
a.get_content()
a.decode()