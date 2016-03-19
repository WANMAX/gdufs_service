'''
Created on 2015年9月2日

@author: wan
'''
from spyne import Unicode
from spyne.model.complex import ComplexModel
from bs4 import BeautifulSoup as Soup
from urllib import request
from crawler import CHARSET
from crawler.ykt_crawler import YKT_TRY_URL, YKT_INFORMATION_URL


INFORMATION_URL = 'http://auth.gdufs.edu.cn'

class Information(ComplexModel):
    def __init__(self, name, photo_url, identity, academy):
        self.name = name
        self.photo_url = photo_url
        self.identity = identity
        self.academy = academy

    name = Unicode
    photo_url = Unicode
    identity = Unicode
    academy = Unicode
    
'''  
def crawl(cookie):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    soup = Soup(opener.open(INFORMATION_URL), from_encoding=CHARSET)
    td = soup.find('td', class_='portletBody')
    text = td.text
    try:
        name = re.search('([\u4e00-\u9fa5]+),', text).group(1)
    except:
        name = ''
    photo_url = 'http://auth.gdufs.edu.cn%s' % td.img['src']
    identity = re.search('身份:[\\s\\S]*?([\u4e00-\u9fa5]+)', text).group(1)
    try:
        academy = re.search('院系:[\\s\\S]*?([\u4e00-\u9fa5]+)', text).group(1)
    except:
        academy = ''
    return Information(name, photo_url, identity, academy)
'''

def crawl(cookie):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    soup = Soup(opener.open(INFORMATION_URL), from_encoding=CHARSET)
    td = soup.find('td', class_='portletBody')
    photo_url = 'http://auth.gdufs.edu.cn%s' % td.img['src']
    opener.open(YKT_TRY_URL)
    soup = Soup(opener.open(YKT_INFORMATION_URL), from_encoding=CHARSET)
    table = soup.table.table
    name = table.find('div', text='姓        名：').findNext('td').text.strip()
    identity = table.find('div', text='身份类型：').findNext('td').text.strip()
    academy = table.find('div', text='所属部门：').findNext('td').text.strip()
    academy = academy[:academy.find('-')]
    return Information(name, photo_url, identity, academy)

if __name__ == '__main__':
    from crawler import COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    print(crawl(cookie)) 
