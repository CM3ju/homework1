import requests
from lxml import etree
import pathlib

URL = 'https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3'
URL_HEAD = 'https://pypi.org/'


class MainPage:
    def __init__(self, url, save_dir='./'):
        self.url = url
        self.status = None
        self.encoding = None
        self.save_dir = save_dir
        self.content = None
        self.list = None

    def get_status(self):
        status = requests.request('GET', self.url)
        self.status = status
        status = int(str(status).split(" ")[1][1:-2])
        if status == 200:
            print('request successfully')
            print(f'url is: {self.url}')
        else:
            print(f'request failed your response is: {status}')
        return self.status

    def get_content(self, page_name='main_page', save=False):
        content = requests.get(self.url)
        if save:
            with open(page_name+'.html', 'w', encoding='utf-8') as f:
                f.write(content.text)
            print(f'get content successfully, file path is: {pathlib.Path.absolute(pathlib.Path(self.save_dir))}')
            print(f'{page_name + ".html"}')
        self.content = content.text

    def decode(self):
        tree = etree.HTML(self.content)
        list_li = tree.xpath('//ul[@class="unstyled"]/li')
        list_herl = []
        for li in list_li:
            list_herl.append(URL_HEAD + str(li.xpath('./a/@href')[0]))
        self.list = list_herl
        return list_herl


class SubPage(MainPage):
    def __init__(self, sub_page_url):
        super().__init__(sub_page_url)

    def get_info(self):
        tree = etree.HTML(self.content)
        name = tree.xpath('//*/h1[@class="package-header__name"]')[0].text.strip(' \n')
        time = tree.xpath('//*/p[@class="package-header__date"]/time')[0].text.strip(' \n')
        return name, time,

def page(url):
    main_page = MainPage(url)
    main_page.get_status()
    main_page.get_content(save=True)
    sub_page_list = main_page.decode()
    print(sub_page_list)
    for sub_page in sub_page_list:
        page_obj = SubPage(sub_page)
        page_obj.get_content(sub_page.replace(URL_HEAD+'/project', '').strip('/'))
        name, time = page_obj.get_info()
        print(f'library name is: {name}, release time is: {time}')


if __name__ == "__main__":
    page(URL)