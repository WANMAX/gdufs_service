from http.cookiejar import LWPCookieJar
from urllib import request, parse


CHARSET = 'utf-8'
JW_BASE_URL = 'http://jxgl.gdufs.edu.cn'

def login(username, password):
    cookie = LWPCookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    post_data = {'username':username, 'password':password, 'login-form-type':'pwd'}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request('http://auth.gdufs.edu.cn/pkmslogin.form', post_data)
    try:
        opener.open(req).read().decode('utf-8')
    except:
        print("%s's login was failed" % username)
        return None
    else:   
        print("%s's login was successful" % username)
        return cookie
    
def login_jw(username, password):
    cookie = LWPCookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    post_data = {'USERNAME':username, 'PASSWORD':password}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request('http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap', post_data)
    try:
        opener.open(req).read().decode(CHARSET)
    except:
        print("%s's login was failed" % username)
        return None
    else:   
        print("%s's login was successful" % username)
        return cookie

COOKIE = '''Set-Cookie3: PD-ID="FmQR1/TZNsp8/gUGsqm1p2/HOq/dFxcp35uLV1DHr7UhJs1XkCmHhBXE3RIcDiT3Mxaq8B9aYqhqJl4v2xX92jdOAZWfE0/xHOkicg/y+ZozfgZWketyHyXujn6565klplKSgz3TlYghv6C0oIl7S5R4G9Yx3RG2+IqQodLELAUZ9ei6Dp+0veGIt6Qu33NdLPxRrJO+B5j7Ca1RjVpnwlMhiiAaB69BHj0AQZcG7+8Wy59nEAT4S14tK2Q2w0vkM6ilhAppGEM="; path="/"; domain=".gdufs.edu.cn"; path_spec; domain_dot; discard; version=0
Set-Cookie3: PD-H-SESSION-ID=4_pbtban4jtfzEj8NtYUg3KO73j1oo8UxTiQ6hDt1fwcRkumyQ; path="/"; domain="auth.gdufs.edu.cn"; path_spec; discard; version=0
'''
COOKIE_JW = '''Set-Cookie3: JSESSIONID=9358F4E4457E4EC61A560F5754519B7D; path="/jsxsd"; domain="jxgl.gdufs.edu.cn"; path_spec; discard; version=0
'''
if __name__ == '__main__':
    print(login_jw('20131003502', '13421573145').as_lwp_str(True, True))