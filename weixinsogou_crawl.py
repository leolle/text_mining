
# coding: utf-8

# # WechatSogou

# ### algorithm:
# 1. import module
# 2. get gzh historical articles
# 3. save the html to local disk
# 4. insert into database or update sids

# ## 1. import modules

# In[14]:


import wechatsogou
import random
import requests
import datetime
import time
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import os
import pathlib
from bs4 import BeautifulSoup
from tqdm import tqdm


# In[2]:


# 直连
ws_api = wechatsogou.WechatSogouAPI()

# 验证码输入错误的重试次数，默认为1
ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)

# 所有requests库的参数都能在这用
# 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
ws_api = wechatsogou.WechatSogouAPI(proxies={
    "http": "http://127.0.0.1:8888",
    "https": "https://127.0.0.1:8888",
})

# 如 设置超时
ws_api = wechatsogou.WechatSogouAPI(timeout=1)


# In[3]:


headers = {
    'Cookie': """SUID=2F2E40613921940A000000005C7C8A68; SUV=0054C7AB61402E2F5C7C8A6C4E9DE485; IPLOC=CN3100; UM_distinctid=16af8a3d10b1c6-00075670c610bf-e353165-1fa400-16af8a3d10c66e; ABTEST=5|1560408316|v1; JSESSIONID=aaafTsCy_KK2le_X5lqRw; PHPSESSID=38sddn82q3fr3mihpq5s9j09j7; SNUID=A3091D2C494FC612B1C5C56E4A2CA7BE; sct=7""",
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}


# In[4]:


ua = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


# ## get proxy tests

# In[115]:


with open('ip.txt') as fp:
    proxy_pool = fp.readlines()


# In[116]:


ls_proxy_pool = []
for string in proxy_pool:
    ip = string.strip().split("\t")
    if len(ip) > 1:
        try:
            if ip[2] == 'HTTP':
                proxy_host = ip[0]+":"+ip[1]
                ls_proxy_pool.append(proxy_host)
        except:
            continue

# In[117]:


def get_proxy():
    http_url = "http://ip111.cn"
    proxy_temp = random.choice(ls_proxy_pool)
    try:
        response = requests.get(http_url)
        if response.status_code == 200:
            return proxy_temp
        return None
    except ConnectionError:
        return None


# ## get articles

# In[ ]:


# ws_api.get_gzh_info('南航青年志愿者')

# ws_api.get_gzh_info('nanhangqinggong')
# In[ ]:


# gzh = ws_api.search_gzh('付鹏的财经世界')


# In[ ]:


# list(gzh)


# In[ ]:


# articles = ws_api.search_article('付鹏的财经世界')


# In[ ]:


# list(articles)


# In[ ]:


# ws_api.get_sugg('财经')


# ### Search historical articles

# In[32]:


proxy = None #将代理设为全局变量
max_count = 3 #最大请求次数


# In[33]:


def get_html(url,count = 1):
    #打印一些调试信息
    print('Crawling:', url)
    print('Trying Count:', count)

    global proxy #引用全局变量
    if count >= max_count: #如果请求次数达到了上限
        print('Tried too many counts！')
        return None

    try :
        uachoice = random.choice(ua)
        headers = {'Cookie': """SUID=2F2E40613921940A000000005C7C8A68; SUV=0054C7AB61402E2F5C7C8A6C4E9DE485; IPLOC=CN3100; UM_distinctid=16af8a3d10b1c6-00075670c610bf-e353165-1fa400-16af8a3d10c66e; ABTEST=5|1560408316|v1; JSESSIONID=aaafTsCy_KK2le_X5lqRw; PHPSESSID=38sddn82q3fr3mihpq5s9j09j7; SNUID=A3091D2C494FC612B1C5C56E4A2CA7BE; sct=7""",
        "User-Agent": uachoice}
        if proxy:# 如果现在正在使用代理
            proxies = {
                'http':'http://'+ proxy #设置协议类型
            }
            response = requests.get(url, headers=headers, proxies=proxies, timeout=3) #使用有代理参数的请求
        else: #否则使用正常的请求
            response = requests.get(url, headers=headers, timeout=3)#禁止自动处理跳转
        if response.status_code == 200:
            print("请求成功！")
            return response.text
        if response.status_code == 302:
            # 需要代理
            print("302！")
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)#打印错误信息
        proxy = get_proxy() #若失败，更换代理
        count += 1 #请求次数+1
        time.sleep(5)
        return get_html(url, count) #重试


# In[92]:


# 解析详情页
def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    wechat_name = doc('#js_profile_qrcode > div > strong').text()
    nickname = doc('.rich_media_meta_text').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    date = None
    return {
        'title':title,
        'wechat_name': wechat_name,
        'content':content,
        'date':date,
        'nickname':nickname,
        'wechat':wechat
    }

# article = get_html(url)
# ls_kol = []
# with open('KOL.txt') as fp:
#     try:
#         line = fp.read()
#         ls_kol.append(line.replace('\n', ''))
#     except:
#         pass
# # In[118]:


with open('KOL.txt') as fp:
    ls_kol = fp.readlines()
    ls_kol = [x.replace('\n', '') for x in ls_kol]


# In[119]:


# ls_kol


# loop in the list key of leaders:
# get history
# loop in the history article url
# if there's author's directory
# os.path.exists('data/a/a')pathlib.Path("/tmp/path/to/desired/directory").mkdir(parents=True, exist_ok=True)
# In[120]:


for au in tqdm(ls_kol):
    print('now: %s'%au)
    while True:
        # get latest 10 articles
        try:
            history = ws_api.get_gzh_article_by_history(au)
        except:
            pass
            print('continue on captcha')
        else:
            break
        time.sleep(5)
    # get articles
    if len(history) == 0:
        continue
    # make directory
    wechat_name = history['gzh']['wechat_name']
    export_dir = 'data/{0}/'.format(wechat_name)
    if not os.path.exists(export_dir):
        pathlib.Path(export_dir).mkdir(parents=True, exist_ok=True)
    for ci in history['article']:
        author = ci['author']
        title = ci['title']
        dt = ci['datetime']
        dt = datetime.datetime.fromtimestamp(
            int(dt)
        ).strftime('%Y_%m_%d')
        url = ci['content_url']
        print(title)
        # use requests
        title = title.replace('/', '')
        fpath = 'data/{0}/{1}_{2}_{3}.html'.format(wechat_name, dt, author, title)
        if not os.path.exists(fpath):
            article = get_html(url)
            if article:
                # export article
                with open(fpath, 'w') as fp:
                    fp.write(article)
        else:
            continue
        time.sleep(3)
    time.sleep(15)


# In[121]:


# history


# In[113]:


# parse_detail(article)


# In[ ]:


# list(history)


# In[ ]:


# history['gzh']

# title = history['article'][0]['title']
# url = history['article'][0]['content_url']
# urlfor ci in history['article']:
#     author = ci['author']
#     title = ci['title']
#     dt = ci['datetime']
#     dt = datetime.datetime.fromtimestamp(
#         int(dt)
#     ).strftime('%Y_%m_%d')
#     url = ci['content_url']
#     print(title)
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         article = response.text
#         fpath = '{0}_{1}_{2}.html'.format(author, dt, title)
#         fpath = fpath.replace('/', '')
#         print(fpath)
#         with open(fpath, 'w') as fp:
#             fp.write(response.text)
#     time.sleep(2)
