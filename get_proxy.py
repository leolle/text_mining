#! coding: utf8
import requests
from bs4 import BeautifulSoup
import urllib
import socket
from tqdm import tqdm
import argparse

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

'''
获取所有代理IP地址
'''


def get_proxy_ip(number_of_pages=5):
    proxy = []
    for i in range(1, number_of_pages):
        try:
            url = 'http://www.xicidaili.com/nn/'+str(i)
            req = requests.get(url, headers=header)
            res = req.text
            soup = BeautifulSoup(res, 'lxml')
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0]+"\t" + \
                    tds[2].contents[0]+"\t"+tds[5].contents[0]
                proxy.append(ip_temp)
        except:
            continue
    return proxy


'''
验证获得的代理IP地址是否可用
'''


def validate_ip(proxy):
    http_url = "http://ip111.cn"
    https_url = "https://myip.cx/"
    # socket.setdefaulttimeout(3)
    # for i in tqdm(range(0, len(proxy))):

    def ping(string):
        try:
            ip = string.strip().split("\t")
            if ip[2] == 'HTTP':
                proxy_host = "http://"+ip[0]+":"+ip[1]
                proxy_temp = {"http": proxy_host}
                url = http_url
            elif ip[2] == 'HTTPS':
                proxy_host = "https://"+ip[0]+":"+ip[1]
                proxy_temp = {"https": proxy_host}
                url = https_url
            res = requests.get(url, proxies=proxy_temp, timeout=0.5)
            print(string)
            return True
        except Exception as e:
            return False

    return list(filter(lambda x: ping(x), proxy))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', type=int, default=5)
    args = parser.parse_args()
    proxy_new = get_proxy_ip(args.number)
    with open("ip.txt", "r") as fp:
        proxy_old = fp.readlines()
    proxy_new.extend(proxy_old)
    proxy_new = list(set(proxy_new))
    proxy = validate_ip(proxy_new)
    with open('ip.txt', 'w') as fp:
        for i in proxy:
            fp.write(i + '\n')
