'''

https://www.dytt8.net/html/gndy/dyzz/list_23_1.html 最新电影
https://www.dytt8.net/html/gndy/jddy/list_63_1.html 综合电影

RuntimeError: Working outside of application context.

This typically means that you attempted to use functionality that needed
to interface with the current application object in some way. To solve
this, set up an application context with app.app_context().  See the
documentation for more information.

'''
import re
import requests
from requests.exceptions import RequestException
import html
from bs4 import BeautifulSoup
import threading
import pymysql
from app.db import get_db
from flask import g, Flask
from flask.cli import with_appcontext
from flask.cli import with_appcontext
from . import movie


def create_database(delete_old=False):
    db = get_db()
    cursor = db.cursor()
    if delete_old:
        sql = 'DROP TABLE IF EXISTS movies'
        cursor.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS movies(
        movie_id INTEGER UNSIGNED PRIMARY KEY,
        movie_name VARCHAR(200) NOT NULL,
        movie_transname VARCHAR(200),
        movie_dbscore FLOAT(3,1),
        movie_imdbscore FLOAT(3,1),
        movie_info TEXT
    )character set = utf8;'''
    cursor.execute(sql)
    db.commit()

def findsth(res='',string=''):
    item = re.search(res, string, re.S |re.I)
    if(item == None):
        return ''
    return item.group(1)

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = headers,timeout = 10)
        response.encoding = 'gb18030'
        if response.status_code == 200:
            return html.unescape(response.text)
        return None
    except RequestException:
        return None
    except:
        return None

def parse_one_page(html_page,id):
    soup = BeautifulSoup(html_page,'lxml')
    title = soup.find(name = 'title')
    soup = soup.find(name = 'div',attrs={'id': 'Zoom'})
    dict = {
        'movie_id':'',
        'movie_name':'',
        'movie_transname':'',
        'movie_dbscore':'',
        'movie_imdbscore':'',
        'movie_info':''
    }
    dict['movie_id'] = id
    dict['movie_name'] = findsth(res = '片　　名(.*?)<br',string = str(soup))
    dict['movie_transname'] = findsth(res = '译　　名(.*?)<br',string = str(soup))
    try:
        dict['movie_dbscore'] = float(findsth(res = '豆瓣评分.*?(\d\.\d)/',string = str(soup)))
    except:
        dict['movie_dbscore'] = 'NULL'
    try:
        dict['movie_imdbscore'] = float(findsth(res = 'IMDb评分.*?(\d\.\d)/',string = str(soup)))
    except:
        dict['movie_imdbscore'] = 'NULL'
    dict['movie_info'] = re.sub('<br/>','',findsth(res = '简　　介(.*?)(?:◎获奖情况.*?)?(?:(?:<i)|(?:</)|(?:<p)|(?:<s))',string = str(soup)))

    if (dict['movie_name']==None):
        dict['movie_name']= findsth(res = '《(.*?)》',string = str(title))
    return dict


def find_url(url):
    html = get_one_page(url)
    if html == None:
        return None
    soup = BeautifulSoup(html,'lxml')
    try:
        db = get_db()
        cursor=db.cursor()
        soup = soup.find(name = 'div',attrs={'class': 'co_content8'}).ul
        result = soup.find_all(name = 'a',attrs = {'class': 'ulink'})
        list = []
        for i in result:
            link = str(i.attrs['href'])
            try:
                link_id = int(findsth(res='/(\d+).html',string=link))

                cursor.execute("SELECT * FROM movies WHERE movie_id=%s"% (link_id))
                if cursor.fetchone() is not None:
                    continue
                list.append([link, link_id])
            except:
                print(link)



        return list
    except AttributeError:
        return None


def start(url_front) :
    id = 0
    url = url_front + '1' + '.html'
    num_max=int(findsth(res='共(\d+)页',string=get_one_page(url)))
    while id<=num_max:
        print(id)
        id += 1
        url = url_front+str(id)+'.html'
        url_list = find_url(url)
        for i in url_list:
            html_page = get_one_page('https://www.dytt8.net'+str(i[0]))
            if html_page == None:
                continue
            dict = parse_one_page(html_page,i[1])
            if dict['movie_name'] == '': continue

            sql = """
            INSERT INTO movies(
            movie_id,
            movie_name,
            movie_transname,
            movie_imdbscore,
            movie_dbscore,
            movie_info
            )VALUES(%s,'%s','%s',%s,%s,'%s')
            """\
                  %(
                      dict['movie_id'],
                      pymysql.escape_string(dict['movie_name']),
                      pymysql.escape_string(dict['movie_transname']),
                      dict['movie_imdbscore'],
                      dict['movie_dbscore'],
                      pymysql.escape_string(dict['movie_info'])
                  )


            db = get_db()
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()




class C_Thread(threading.Thread):
    def __init__(self,threadID,url_front,Lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url_front = url_front
        self.Lock = Lock
    def run(self):
        start(url_front=self.url_front, txtLock=self.Lock)





