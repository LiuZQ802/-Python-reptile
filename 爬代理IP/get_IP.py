import requests
from bs4 import BeautifulSoup
import json
import random


# 请求并获得IP和port
def getIp(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.82 Safari/537.36",
        "referer": "www.baidu.com"
    }
    # 代理
    ip_lists = readIp()
    proxies_ip = random.choice(ip_lists)
    proxies = {'http': 'http://' + proxies_ip['ip'] + ':' + proxies_ip['port']}
    # 请求并转化为文本内容
    try:
        res = requests.get(url, headers=headers, proxies=proxies)
        html_doc = res.content.decode("utf-8")
        # 转换为bp类型
        soup = BeautifulSoup(html_doc)
        # 获得所有表项
        table = soup.select("tbody>tr")

        ip_list = []
        # 处理
        for item in table:
            td = item.select("td")
            ip = td[0].getText().strip()
            port = td[1].getText().strip()
            data = {'ip': ip, 'port': port}
            ip_list.append(data)
        return ip_list
    except:
        print('请求失败')
        return []


# 请求每一页
def req_page():
    url = "https://www.kuaidaili.com/free/inha/{}/"
    for index in range(8, 101):
        real_url = url.format(index)
        ip = getIp(real_url)  # 得到代理ip列表
        ip = isUseful(ip)  # 去除不可用代理
        save(ip)  # 存储
        print('第'+str(index)+'页抓取完毕')


# 判断IP是否可以用
def isUseful(ip_list):
    check_url = 'https://www.ip.cn/'  # 访问这个地址判断代理是否可以用
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.82 Safari/537.36",
        "referer": "www.baidu.com"
    }
    for ip in ip_list:
        ip_url = ip['ip'] + ':' + ip['port']  # 代理ip
        proxies = {'http': 'http://' + ip_url}  # 代理
        res = False
        try:
            req = requests.get(url=check_url, headers=headers, proxies=proxies, timeout=3)
            if req.status_code == 200:  # 判断代理是否可用
                res = True
        except:
            res = False
        if not res:
            ip_list.remove(ip)
    return ip_list


# 转换成json并存入文件中
def save(ip_list):
    with open('代理.json', 'a+', encoding="utf-8") as f:
        for ip in ip_list:
            item = json.dumps(ip)
            f.write(item)
            f.write('\n')


# 读代理ip
def readIp():
    ip_lists = []
    with open('代理.json', 'r', encoding='utf-8') as f:
        for item in f.readlines():
            ip = json.loads(item)
            ip_lists.append(ip)
    return ip_lists


if __name__ == '__main__':
    req_page()
    # readIp()
