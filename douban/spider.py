import urllib.error
import urllib.request
import xlwt
from lxml import etree


class spider:
    url = 'https://movie.douban.com/top250?start='  # 访问的url
    saveName = '豆瓣电影Top250'  # 保存的名字
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

    # 构造函数
    def __init__(self):
        self.getData()  # 爬取每一页，获得每一页的etree
        self.get_fileData()  # 获得所有电影etree
        self.get_data()  # 获得每一部电影的数据
        self.save_to_excel()  # 数据保存到excel表
        pass

    # 析构函数
    def __del__(self):
        pass

    # 爬取每一页网页
    def getData(self):
        for i in range(0, 15):
            url = self.url + 'i*25'
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
            if foreign_name:
                foreign_name = foreign_name[0].strip(' / ')
            else:
                foreign_name = ''
            link = item.xpath("./div/div[@class='info']/div[@class='hd']/a/@href")[0]  # 电影链接
            score = item.xpath("./div/div[@class='info']/div[@class='bd']/div/span[@class='rating_num']/text()")[
                0]  # 评分
            comment_number = item.xpath("./div/div[@class='info']/div[@class='bd']/div/span[4]/text()")[0]  # 评论数
            relate_information = item.xpath("./div/div[@class='info']/div[@class='bd']/p[1]/text()")[0].strip()  # 相关信息
            sentence = item.xpath("./div/div[@class='info']/div[@class='bd']/p[2]/span/text()")[0]  # 精选语句
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
