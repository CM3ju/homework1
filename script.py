import requests
from lxml import etree
import pathlib
import urllib.request
import os

URL = 'https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3&page='
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
            with open(page_name + '.html', 'w', encoding='utf-8') as f:
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
        download = tree.xpath('//*/div[@class="card file__card"]/a/@href')[0].strip(' \n')
        return name, time, download


def page(url, N):
    total_list = []
    for _ in range(N):
        main_page = MainPage(url + str(_))
        main_page.get_status()
        main_page.get_content(save=True)
        sub_page_list = main_page.decode()
        total_list += sub_page_list
    print(total_list)
    print(len(total_list))
    return total_list

def parse_subpages(sub_pages, save_file=False, save_dir='./lib/'):
  for sub_page in sub_pages:
        page_obj = SubPage(sub_page)
        page_obj.get_content(sub_page.replace(URL_HEAD + '/project', '').strip('/'))
        name, time, download = page_obj.get_info()
        filename = download.split('/')[-1]
        print(f'library name is: {name}, release time is: {time}, download link is: {download}')
        if save_file:
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            urllib.request.urlretrieve(download, save_dir + filename)
        print(save_dir + filename)

def run_multi_thread(total_list, n_thread, save_file=False, save_dir='./lib/'):
    subpage_div = [total_list[i:i + len(total_list) // n_thread] for i in range(0, len(total_list), len(total_list) // n_thread)]
    threads = []
    for sub_pages in subpage_div:
        thread = threading.Thread(target=parse_subpages, args=(sub_pages, save_file, save_dir))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_threads = 4
    num_pages = 20
    total_list = page(URL, num_pages)
    run_multi_thread(total_list, num_threads, save_file=True, save_dir='./lib/')
