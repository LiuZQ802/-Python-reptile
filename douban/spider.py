import urllib.error
import urllib.request
import xlwt
from lxml import etree
import sqlite3
import pymysql


class spider:
    url = 'https://movie.douban.com/top250?start='  # 访问的url
    saveName = 'doubanMovieTop250'  # 保存的名字
    dataList = []  # 网页返回列表
    film_data = []  # 电影
    name = []  # 电影名
    foreign_name = []  # 外国名
    link = []  # 电影链接
    score = []  # 评分
    comment_number = []  # 评论数
    relate_information = []  # 相关信息
    sentence = []  # 精选语句
    col = ("影片中文名", "影片外国名", "影片链接", "评分", "评价数", "概况", "相关信息")  # 列名

    sqlite3_con = ''  # sqlite数据库连接
    mysql_con = ''  # mysql数据库连接

    # 构造函数
    def __init__(self):
        self.getData()  # 爬取每一页，获得每一页的etree
        self.get_fileData()  # 获得所有电影etree
        self.get_data()  # 获得每一部电影的数据
        self.save_to_excel()  # 数据保存到excel表

        #self.connect_sqlite()  # 连接sqlite数据库，并且创建表
        #self.save_to_database(self.sqlite3_con)  # 数据保存到sqlite数据库中
        #self.conncet_mysql()  # 连接mysql数据库
        #self.save_to_database(self.mysql_con)  # 保存信息到mysql数据库
        pass

    # 析构函数
    def __del__(self):
        try:
            self.sqlite3_con.close()  # 关闭数据库
        except:
            print("sqlite数据库没有打开")
        try:
            self.mysql_con.close()  # 关闭mysql数据库
        except:
            print("mysql数据库没有打开")
        pass

    # 爬取每一页网页
    def getData(self):
        for i in range(0, 10):
            url = self.url + '%d' % (i * 25)
            html = self.askURL(url)
            self.dataList.append(html)
        pass

    # 访问url,返回html,可以用xpath
    def askURL(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            response = urllib.request.urlopen(req)
            html_doc = response.read().decode("utf-8")
            html = etree.HTML(html_doc)  # 转换为可以用xpath的element对象
            return html
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        pass

    # 获得每一部电影
    def get_fileData(self):
        # 遍历每一页
        for item in self.dataList:
            li = item.xpath("//div[@class='article']/ol/li")  # 获得该页所有电影数组
            # 将每部电影加入数组
            for film in li:
                self.film_data.append(film)
        pass

    # 获得每一部电影的相关数据
    def get_data(self):
        # 遍历每一部电影
        for item in self.film_data:
            name = item.xpath("./div/div[@class='info']/div[@class='hd']/a/span[@class='title'][1]/text()")[0]  # 电影名
            foreign_name = item.xpath(
                "./div/div[@class='info']/div[@class='hd']/a/span[@class='title'][2]/text()")  # 电影外国名
            # 有的电影没有外国名
            if foreign_name:
                foreign_name = foreign_name[0].strip(' / ')
            else:
                foreign_name = ''
            link = item.xpath("./div/div[@class='info']/div[@class='hd']/a/@href")[0]  # 电影链接
            score = item.xpath("./div/div[@class='info']/div[@class='bd']/div/span[@class='rating_num']/text()")[
                0]  # 评分
            comment_number = item.xpath("./div/div[@class='info']/div[@class='bd']/div/span[4]/text()")[0]  # 评论数
            relate_information = item.xpath("./div/div[@class='info']/div[@class='bd']/p[1]/text()")[0].strip()  # 相关信息
            sentence = item.xpath("./div/div[@class='info']/div[@class='bd']/p[2]/span/text()")  # 精选语句
            # 有的电影没有精选语句
            if sentence:
                sentence = sentence[0]
            else:
                sentence = ''
            # 将信息全部加入相应列表
            self.name.append(name)
            self.foreign_name.append(foreign_name)
            self.link.append(link)
            self.score.append(score)
            self.comment_number.append(comment_number)
            self.relate_information.append(relate_information)
            self.sentence.append(sentence)

        pass

    # 保存数据到excel表

    def save_to_excel(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(self.saveName)
        # 写列名
        for td in range(7):
            worksheet.write(0, td, self.col[td])
        # 写影片信息
        for tr in range(250):
            worksheet.write(tr + 1, 0, self.name[tr])
            worksheet.write(tr + 1, 1, self.foreign_name[tr])
            worksheet.write(tr + 1, 2, self.link[tr])
            worksheet.write(tr + 1, 3, self.score[tr])
            worksheet.write(tr + 1, 4, self.comment_number[tr])
            worksheet.write(tr + 1, 5, self.sentence[tr])
            worksheet.write(tr + 1, 6, self.relate_information[tr])
        workbook.save(self.saveName + ".xls")  # 保存到excel文件
        pass

    # 连接sqlite数据库,并创建表
    def connect_sqlite(self):
        self.sqlite3_con = sqlite3.connect(self.saveName)
        cursor = self.sqlite3_con.cursor()
        try:
            sql = '''
                    create table if not exists movie250
                    (
                    id integer primary key autoincrement,
                    cname text,
                    ename text,
                    info_link text,
                    score  numeric,
                    related text,
                    instroduction text,
                    info text
                    );
                    '''
            cursor.execute(sql)
            self.sqlite3_con.commit()
        except:
            self.sqlite3_con.rollback()  # 回滚
        pass

    # 连接mysql数据库，并创建表
    def conncet_mysql(self):
        host = "localhost"
        user = "root"
        passwd = "root"
        db = "douban"
        self.mysql_con = pymysql.connect(host=host, user=user, password=passwd, db=db)  # 连接数据库
        cursor = self.mysql_con.cursor()
        try:
            sql = '''
                                        create table if not exists movie250
                                        (
                                            id int primary key AUTO_INCREMENT,
                                        cname text,
                                        ename text,
                                        info_link text,
                                        score  float,
                                        related text,
                                        instroduction text,
                                        info text
                                        );
                                        '''
            cursor.execute(sql)
            self.mysql_con.commit()
        except:
            self.mysql_con.rollback()  # 回滚
        pass

    # 保存信息到数据库,db表示数据库
    def save_to_database(self, db):
        cursor = db.cursor()
        try:
            for item in range(250):
                sql = '''
                               insert into movie250(cname,ename,info_link,score,related,instroduction,info)
                               VALUES("%s","%s",'%s',%f,"%s","%s","%s");          
                               ''' % (
                    self.name[item], self.foreign_name[item], self.link[item], float(self.score[item]),
                    self.comment_number[item],
                    self.sentence[item],
                    self.relate_information[item])  # 要注意单双引号的使用
                cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()  # 回滚
            print(e)
            print("插入失败")
        pass
