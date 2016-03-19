'''
Created on 2015年9月1日

@author: wan
'''
from bs4 import BeautifulSoup as Soup
from spyne.model.complex import ComplexModel
from urllib import request, parse
from crawler import CHARSET, JW_BASE_URL
from spyne import Unicode


class Score(ComplexModel):
    def __init__(self, course_id, course_name, type1, type2, credit, grade_point, normal_performance, np_account_for,final_exam_score,
                 fes_account_for, score):
        self.course_id = course_id
        self.course_name = course_name
        self.type1 = type1
        self.type2 = type2
        self.credit = credit
        self.grade_point = grade_point
        self.normal_performance = normal_performance
        self.np_account_for = np_account_for
        self.final_exam_score = final_exam_score
        self.fes_account_for = fes_account_for
        self.score = score

    course_id = Unicode
    course_name = Unicode
    type1 = Unicode
    type2 = Unicode
    credit = Unicode
    grade_point = Unicode
    normal_performance = Unicode
    np_account_for = Unicode
    final_exam_score = Unicode
    fes_account_for = Unicode
    score = Unicode

def _score_to_grade_point(score):
    score = eval(score)
    if score >= 90:return '4.0'
    elif score >= 85:return '3.7'
    elif score >= 82:return '3.3'
    elif score >= 78:return '3.0'
    elif score >= 75:return '2.7'
    elif score >= 71:return '2.3'
    elif score >= 66:return '2.0'
    elif score >= 62:return '1.7'
    elif score == 61:return '1.3'
    elif score == 60:return '1.0'
    else:return '0'
def crawl(cookie, student_number, year, term):
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    url = 'http://jxgl.gdufs.edu.cn/jsxsd/kscj/cjcx_list'
    post_data = {'kksj':'%s-%s'%(year, term), 'xsfs':'all'}
    req = request.Request(url, parse.urlencode(post_data).encode())
    soup = Soup(opener.open(req), from_encoding=CHARSET)
    table = soup.find_all('table')[-1]
    score_list = []
    for item in table.find_all('tr')[1:]:
        tds = item.find_all('td')
        course_id = tds[2].text
        course_name = tds[3].text
        credit = tds[5].text
        type1 = tds[8].text
        type2 = tds[9].text
        url2 = item.a['href']
        url2 = url2[url2.find("'")+1: url2.rfind("'")]
        url2 = JW_BASE_URL + url2
        soup2 = Soup(opener.open(url2), from_encoding=CHARSET)
        table2 = soup2.table
        tds2 = table2.find_all('tr')[-1].find_all('td')
        normal_performance = tds2[1].text
        np_account_for = tds2[2].text
        final_exam_score = tds2[5].text
        fes_account_for = tds2[6].text
        score = tds2[7].text
        score_list.append(Score(course_id, course_name, type1, type2, credit, _score_to_grade_point(score), normal_performance, np_account_for,final_exam_score,
                 fes_account_for, score))
    return score_list

if __name__ == '__main__':
    from crawler import COOKIE_JW as COOKIE
    from util import cookie_from_str
    cookie = cookie_from_str(COOKIE)
    for item in crawl(cookie, '20131003502', '2015-2016', '1'):
        print(item)