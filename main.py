import time
import requests
import csv
from lxml import etree

from db import *


class Tieba(object):
    def __init__(self, name):
        self.session = None
        self.url = f'https://tieba.baidu.com/f?kw={name}'
        self.headers = {
            'User-Agent': '/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) '     #  低端浏览器没有被<!--  -->注释掉
        }

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        with open(f"tmp/{url.split('/')[-1].replace('?', '.')}.html", 'wb') as f:
            f.write(response.content)
        return response.content

    def parse_data(self, data):
        data = data.decode().replace("<!--", "").replace("-->", "")
        el_html = etree.HTML(data)
        # el_list = el_html.xpath('//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a')  #  此处输出的是对象
        el_list = el_html.xpath('//*[@id="thread_list"]/li/div')  # 此处输出的是对象
        if not len(el_list):
            print("请求被拦截，请尝试更换代理")
            exit()
        print(len(el_list))
        data_list = []
        for el in el_list:
            tmp = {}
            tmp['title'] = el.xpath('./div[2]/div[1]/div[1]/a/text()')[0]  # 此处xpath取出的数据是列表，所以加上索引[0]
            tmp['href'] = 'http://tieba.com' + el.xpath('./div[2]/div[1]/div[1]/a/@href')[0]  # 此处取出的索引是相对路径，所以前面还要拼接字符串
            try:
                tmp['author'] = el.xpath('./div[2]/div[1]/div[2]/span[1]/span[1]/a/text()')[0]
            except:
                tmp['author'] = el.xpath('./div[2]/div[1]/div[2]/span[1]/span[1]/a/text()')
            try:
                tmp['reviewer'] = el.xpath('./div[2]/div[2]/div[2]/span[1]/a/text()')[0]
            except:
                tmp['reviewer'] = el.xpath('./div[2]/div[2]/div[2]/span[1]/a/text()')
            try:
                tmp['last_comment_time'] = el.xpath('./div[2]/div[2]/div[2]/span[2]/text()')[0]
            except:
                tmp['last_comment_time'] = el.xpath('./div[2]/div[2]/div[2]/span[2]/text()')
            try:
                tmp['comment'] = el.xpath('./div[2]/div[2]/div[1]/div/text()')[0]
            except:
                tmp['comment'] = el.xpath('./div[2]/div[2]/div[1]/div/text()')
            data_list.append(tmp)
        # print(data_list)

        #  获取csv他属性值
        a = []
        dict = data_list[0]
        for headers in sorted(dict.keys()):  # 把字典的键取出来
            a.append(headers)
        header = a  # 把列名给提取出来，用列表形式呈现
        print(a)

        try:
            # next_url = 'https' + el_html.xpath('//a[@class="next pagination-item "]/@href')
            next_url = 'https:' + el_html.xpath('//a[contains(text(),"下一页")]/@href')[0]
        except:
            next_url = None
        return data_list, next_url, header

    def save_data(self, data_list, header):
        for 帖子 in data_list:
            print(帖子)
            try:
                帖子['comment'] = 帖子['comment'].strip().replace('\r', '').replace('\n', '')
                tid = int(帖子['href'].split('/')[-1])
                if not session.query(Thread).where(Thread.tId == tid).first():
                    author = '' if not 帖子['author'] else 帖子['author']
                    new_thread = Thread(tId=tid, Title=帖子['title'], Href=帖子['href'],
                                        Author=author, Content=帖子['comment'])
                    session.add(new_thread)
                    session.commit()
            except Exception as e:
                print('Failed on saving data ' + e)
        for data in data_list:
            print(data)

    def run(self):
        next_url = self.url
        self.session = Session(bind=engine)
        while True:
            #  发送请求，获取响应
            data = self.get_data(next_url)
            #  从响应中提取数据（数据和翻页用的url）
            data_list, next_url, a = self.parse_data(data)
            print(data_list)
            self.save_data(data_list, a)

            #  判断是否终结
            if next_url is None:
                break
            time.sleep(30)


if __name__ == '__main__':
    tieba = Tieba('核战避难所')
    tieba.run()
