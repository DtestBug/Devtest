import requests
from pyquery import PyQuery


url = 'http://www.netbian.com/s/wangzherongyao/'

data = requests.get(url)

data.encoding = 'utf-8'

datas = PyQuery(data.text)

print(datas)

