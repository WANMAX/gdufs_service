'''
Created on 2016年1月12日

@author: wan
抢课系统，暂不开放
'''
from http.cookiejar import LWPCookieJar
from urllib import request, parse
from urllib.request import build_opener
#from tool.proxy import build_opener
import re
import time
from threading import Thread
from bs4 import BeautifulSoup as Soup
null = ''
true = True
false = False

_HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}  
CHARSET = 'utf-8'

ERROR = False

def _get_opener(cookie):
    cookie_support = request.HTTPCookieProcessor(cookie)
    return build_opener(cookie_support , request.HTTPHandler)
def post(cookie, url, post_data, charset):
    post_data = parse.urlencode(post_data).encode(charset)
    req = request.Request(url, post_data, _HEADERS)
    opener = _get_opener(cookie)
    return opener.open(req).read()
def get(cookie, url):
    req = request.Request(url, None, _HEADERS)
    return _get_opener(cookie).open(req).read()

def login(username, password):
    login_url = 'http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap'
    cookie = LWPCookieJar()
    post_data = {'USERNAME':username, 'PASSWORD':password}
    try:
        html = post(cookie, login_url, post_data, CHARSET).decode(CHARSET)
        if not '首页' in html:
            raise
    except:
        raise
        print("%s's login was failed" % username)
        return None
    else:   
        print("%s's login was successful" % username)
        global ERROR
        ERROR = False
        return cookie
def attend_xk(cookie, course_time):
    url = 'http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xklc_list'
    soup = Soup(get(cookie, url), from_encoding=CHARSET)
    for item in soup.find('table', id='tbKxkc').find_all('tr'):
        try:
            if re.search(course_time, item.td.text.strip()):
                url = 'http://jxgl.gdufs.edu.cn%s'%item.a['href']
                break
        except:
            continue
    else:
        raise
    get(cookie, url)
    
def _get_course_id(cookie, course_name, course_time):
    url = 'http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xsxkXxxk'
    post_data = {'sEcho':'1', 'iColumns':'8', 'sColumns':'', 'iDisplayStart':'0', 'iDisplayLength':'15', 'mDataProp_0':'kch',
                 'mDataProp_1':'kcmc', 'mDataProp_2':'xf', 'mDataProp_3':'skls', 'mDataProp_4':'sksj', 'mDataProp_5':'skdd',
                 'mDataProp_6':'ctsm', 'mDataProp_7':'czOper'}
    data = eval(post(cookie, url, post_data, CHARSET).decode(CHARSET))
    dict_ = {}
    for item in data['aaData']:
        if course_name == '' or re.search(course_name, item['kcmc']):
            if course_time == '' or re.search(course_time, item['sksj']):
                dict_[item['kcmc']+' '+item['sksj']]=item['jx0404id']
    return dict_
def get_all_course_id(cookie, dict_):
    dict2 = {}
    for item in dict_.keys():
        dict3 = _get_course_id(cookie, item, dict_[item])
        for name in dict3.keys():
            dict2[name] = dict3[name]
    return dict2
numb =1
def get_course(cookie, name, dict_, time_):
    global numb
    try:
        url = 'http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=%s'%dict_[name]
        while True:
            result = eval(get(cookie, url).decode(CHARSET))
            print(name, ':', result['message'])
            if result['success']:
                numb -= 1
                del dict_[name]
                break
            elif re.search('已选|冲突', result['message']):
                del dict_[name]
                break
            time.sleep(time_)
    except:
        raise
        global ERROR
        ERROR = True
def get_all_course(cookie, dict_, time_):
    for course_name in dict_.keys():
        Thread(target=get_course, args=(cookie, course_name, dict_, time_)).start()
def crawler(username, password, course_time, course_dict, time_, numb2):
    global numb
    numb = numb2
    while True:
        cookie = login(username, password)
        attend_xk(cookie, course_time)
        dict_ = get_all_course_id(cookie, course_dict)
        get_all_course(cookie, dict_, time_)
        while not ERROR:
            time.sleep(1)
            if not len(dict_.keys()) or numb <= 0:
                exit()
if __name__ ==  '__main__':
    username = '20131003502'
    password = '13421573145'
    course_time = '2015-2016-2'
    course_dict = {'互联':'', '嵌入式':''}
    time_ = 0.33
    numb = 1;
    crawler(username, password, course_time, course_dict, time_, numb)
    
    