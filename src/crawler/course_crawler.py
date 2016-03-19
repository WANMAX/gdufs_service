'''
Created on 2015年8月18日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
import re
from spyne import Unicode, Integer
from spyne.model.complex import ComplexModel
from urllib import request, parse

from crawler import CHARSET


__START_DICT = {1:2, 2:4, 3:7, 4:8, 5:10, 6:12, 7:14}
__NUM_DICT = {1:2, 2:3, 3:1, 4:2, 5:2, 6:2, 7:2}
class Course(ComplexModel):
    course_name = Unicode
    teacher_name = Unicode
    place = Unicode
    start_time = Integer
    numb = Integer
    def __init__(self, course_name, teacher_name, place, start_time, numb):
        self.course_name, self.teacher_name, self.place, self.start_time, self.numb =\
        course_name, teacher_name, place, start_time, numb
def crawl(cookie, student_number, year, term):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    url = 'http://jxgl.gdufs.edu.cn/jsxsd/xskb/xskb_list.do'
    post_data = {'xnxq01id':'%s-%s'%(year, term)}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(url, post_data)
    soup = Soup(opener.open(req), from_encoding=CHARSET)
    table = soup.find_all('table')[-1]
    course_table = [[], [], [], [], [], [], []]
    course_index = 0
    for tr in table.find_all('tr')[1:-1]:
        course_index += 1
        day_index = -1
        for td in tr.find_all('td'):
            day_index += 1
            if re.match('\\s+', td.div.text):
                continue
            contents = td.find_all('div')[1]
            course_name = contents.contents[0]
            try:
                teacher_name = contents.find('font', {"title":"老师"}).text
            except:
                teacher_name = ''
            try:
                place = contents.find('font', {"title":"教室"}).text
            except:
                place = ''
            start_time = __START_DICT[course_index]
            numb = __NUM_DICT[course_index]
            course = Course(course_name, teacher_name, place, start_time, numb)
            if len(course_table[day_index])>0:
                temp = course_table[day_index][-1]
                if (temp.course_name, temp.teacher_name, temp.place) == (course.course_name, course.teacher_name, course.place):
                    if (temp.start_time + temp.numb) == course.start_time:
                        temp.numb += course.numb
                        continue
            course_table[day_index].append(course)
    return course_table

if __name__ == '__main__':
    from crawler import COOKIE_JW as COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    for day in crawl(cookie, '20131003502', '2015-2016', '1'):
        if not day:print('nothing')
        else:print(day)
