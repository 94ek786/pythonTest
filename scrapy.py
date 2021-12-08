#selenium_icook_5.py 完成寫入資料庫
#pip install SQLAlchemy
#pip install mysql-connector-python
import sys
import time
import random
import re
import ntpath
import loguru
import configparser
import json

from datetime import datetime
from lxml import etree

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import sqlalchemy
import sqlalchemy.ext.automap
import sqlalchemy.orm
import sqlalchemy.schema

from captcha_solver import CaptchaSolver

def main():
    global pageLinks
    #登入
    #login()
    
    driver.get(config['icook']['Url'])
    hasNext = search() 
    
    #取得資料
    loop = 4
    while loop !=-56:
        #只取一個月的資料
        results = driver.find_element_by_xpath('/html/body/blockquote[2]/p[3]/table/tbody/tr['+str(loop)+']').get_attribute('innerHTML')
        dom = etree.HTML(results)
        #print(dom.xpath('////td[@class="stub1"]/text()'))
        if dom.xpath('////td[@class="stub1"]/text()') == []:
            break
        parseDetail(dom)
        loop = loop + 1
    #print(articles)

    #寫入資料庫
    create_db_scrapy()

    sys.exit('爬蟲結束')

#確認尚未讀取的月份
def SStart():
    sqlalchemy.Table(__articletable__, metadata, autoload=True)
    t = automap.classes[__articletable__]

    aList = []
    #取得現在年跟月
    Ti = str(datetime.now()).split('-')
    Ti = [int(Ti[0]),int(Ti[1])]
    #做第一次判斷這個月是否已被記錄過
    ans = session.query(
        t
    ).filter(
        t.month == '%dM%02d'%(Ti[0],Ti[1])
    ).first()

    #時間往前判斷是否有讀取過該資料
    while not ans:
        aList.append([Ti[0],Ti[1]])
        #月份-1
        if Ti[1] == 1:
            Ti[1] = 12
            Ti[0] = Ti[0] - 1
        else:
            Ti[1] = Ti[1] - 1
        #判斷
        ans = session.query(
            t
        ).filter(
            t.month == '%dM%02d'%(Ti[0],Ti[1])
        ).first()
        #內政部資料只給到1981年
        if Ti[0] == 1980:
            break
    
    return aList

        
        


#搜尋(關鍵字，材料)
def search():
    #確認尚未讀取過的資料月份
    Y_M = SStart()
    #要查詢的月份
    searching = driver.find_element_by_xpath('/html/body/form/blockquote[1]/table[2]/tbody/tr[4]/td[1]/input[1]')
    confirm = driver.find_element_by_xpath('/html/body/form/blockquote[1]/table[2]/tbody/tr[4]/td[1]/img')
    for loop in Y_M:
        searching.clear()
        searching.send_keys('%dM%02d'%(loop[0],loop[1]))
        confirm.click()
    #要查詢的基本分類暨項目群
    searching = driver.find_element_by_name('context2')
    confirm = driver.find_element_by_xpath('//table[@class="table2"]//img[@onmousedown="showcontext1(document.main.values2, document.main.context2, document.main.begin2);howmany(2,1)"]')
    for loop in range(int(config['search']['length'])):
        searching.clear()
        searching.send_keys(config['search'][str(loop)])
        confirm.click()
    # 顯示種類全選
    confirm = driver.find_element_by_xpath('//table[@class="table2"]//td[@class="tdtop"]/a[@onmousedown="onSelectAll(\'values3\',1);howmany(3,1)"]')
    confirm.click()
    #按下繼續
    confirm = driver.find_element_by_name('sel')
    time.sleep(3)
    confirm.click()

    return True


#解析內容頁
def parseDetail(dom):
    global articles

    total = []
    #依照順序抓入資料
    dataList=1
    while dataList != -37756:
        try:
            if dom.xpath('//td['+str(dataList)+']/text()')[0] == '-':
                total.append('0')
            else:
                total.append(str(dom.xpath('//td['+str(dataList)+']/text()')[0]))
        except:
            break
        dataList =dataList+1
    #判斷抓到的資料數量是否與資料庫一致
    #以防止以後政府更改物價分類物價指數而會產生的錯誤
    
    if len(total) != int(config['mysql']['amount']):
        sys.exit('讀取數量與資料庫不符程式需要更新')
    
    articles.append(total)


def create_db_article(item):
    created = int(time.mktime(datetime.now().timetuple()))
    sqlalchemy.Table(__articletable__, metadata, autoload=True)
    Article = automap.classes[__articletable__]
    
    #for i in item:
        #print(type(i))

    article = Article()
    article.month = item[0]
    article.total = item[1]
    article.totalPercent = item[2]
    article.food = item[3]
    article.foodPercent = item[4]
    article.cloth = item[5]
    article.clothPercent = item[6]
    article.house = item[7]
    article.housePercent = item[8]
    article.traffic = item[9]
    article.trafficPercent = item[10]
    article.medicine = item[11]
    article.medicinePercent = item[12]
    article.Education = item[13]
    article.EducationPercent = item[14]
    article.others = item[15]
    article.othersPercent = item[16]
    session.add(article)
    return

def create_db_scrapy():
    for item in articles:
        create_db_article(item)
        try:
            session.commit()
        except Exception as e:
            loguru.logger.error('新增資料失敗')
            loguru.logger.error(e)
            session.rollback()

    #session.close()
    loguru.logger.info('完成爬蟲及寫入資料.')
    return

if __name__ == '__main__':
    loguru.logger.add(
        f'{datetime.today().strftime("%Y%m%d")}.log',
        rotation='1 day',
        retention='7 days',
        level='DEBUG'
    )

    config = configparser.RawConfigParser()
    config.read("config.ini")

    #Selenium with webdriver
    options = Options()
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    webdriver_path = 'C:\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    #資料庫定義
    __articletable__ = 'price'
    __articlemetatable__ = 'crawler_articlemeta'
    __fieldstable__ = 'crawler_fields'
    __listtable__ = 'crawler_list'
    __mediatable__ = 'crawler_media'

    __wp_posts_table__ = 'wp_posts'
    __wp_postmeta_table__ = 'wp_postmeta'
    __wp_term_relationships_table__ = 'wp_term_relationships'
    __wp_term_taxonomy_table__ = 'wp_term_taxonomy'
    __wp_termmeta_table__ = 'wp_termmeta'
    __wp_terms_table__ = 'wp_terms'

    __post_type__ = 'scrapy'
    __taxonomy_name__ = 'scrapies'

    #取得資料庫連線設定
    config = configparser.RawConfigParser()
    config.read("config.ini")

    host = config['mysql']['Host']
    port = int(config['mysql']['Port'])
    username = config['mysql']['User']
    password = config['mysql']['Password']
    database = config['mysql']['Database']
    chartset = config['mysql']['Charset']

    # 建立連線引擎
    connect_string = connect_string = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset={}'.format(username, password, host, port, database, chartset)
    connect_args = {'connect_timeout': 10}
    engine = sqlalchemy.create_engine(connect_string, connect_args=connect_args, echo=False)
    
    # 取得資料庫元資料
    metadata = sqlalchemy.schema.MetaData(engine)
    # 產生自動對應參照
    automap = sqlalchemy.ext.automap.automap_base()
    automap.prepare(engine, reflect=True)
    # 準備 ORM 連線
    session = sqlalchemy.orm.Session(engine)

    #全域變數
    pageLinks = []
    articles = []


    main()