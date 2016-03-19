from suds.client import Client

from crawler import COOKIE

c = Client('http://4304e92d.nat123.net:24110/?wsdl')
#c = Client('http://127.0.0.1:8000/?wsdl')
import threading
def printFunc(func):
    def temp(*args):
        print(func(*args))
    return temp
#threading.Thread(target=printFunc(c.service.crawl_weather)).start()
#threading.Thread(target=printFunc(c.service.crawl_news), args=(1,)).start()
threading.Thread(target=printFunc(c.service.crawl_announcement), args=(1,)).start()
