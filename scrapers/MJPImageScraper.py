import time
import random
import requests
from lxml import html


def get_page_number(base_url, num):
    image_url = base_url + num
    print(image_url)
    response = requests.get(image_url).content
    selector = html.fromstring(response)
    urls = []
    for i in selector.xpath("//ul/li/a/@href"):
        urls.append(i)
    return urls


def get_image_title(image_url):
    response = requests.get(image_url).content
    selector = html.fromstring(response)
    image_title = selector.xpath("//h2/text()")[0]
    return image_title


def get_image_amount(image_url):
    response = requests.get(image_url).content
    selector = html.fromstring(response)
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    return image_amount


def get_image_detail_website(image_url):
    response = requests.get(image_url).content
    selector = html.fromstring(response)
    image_detail_websites = []
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    for i in range(int(image_amount)):
        image_detail_link = '{}/{}'.format(image_url, i + 1)
        response = requests.get(image_detail_link).content
        selector = html.fromstring(response)
        image_download_link = selector.xpath("//div[@class='content']/a/img/@src")[0]
        image_detail_websites.append(image_download_link)
    return image_detail_websites


def download_image(output_path, image_title, image_detail_websites):
    num = 1
    amount = len(image_detail_websites)
    for i in image_detail_websites:
        filename = output_path + '%s%s.jpg' % (image_title, num)
        print('downloading: %s %s/%s, ' % (image_title, num, amount))
        headers = {"Upgrade-Insecure-Requests": "1",
                   "Referer": i.rsplit('/', 1)[0],
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/39.0.2171.95 Safari/537.36"}
        response = requests.get(i, headers=headers)
        with open(filename, 'wb') as f:
            f.write(response.content)
        num += 1
        time.sleep(random.randint(1, 7))


if __name__ == '__main__':
    page_number = input('enter page: ')
    url = 'http://www.mmjpg.com/home/'
    file_path = ''
    for link in get_page_number(url, page_number):
        download_image(file_path, get_image_title(link), get_image_detail_website(link))
