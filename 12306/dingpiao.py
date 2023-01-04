from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
import os
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class dingpiao(object):

    # 构造函数，初始化url、出发站、终点站、出发时间、登录用户名、登录密码
    def __init__(self, info):
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"  # 登录页面
        self.driver = None  # driver
        self.info = info  # 基本信息

        self.set_driver()  # 设置driver
        self.login()  # 登录
        self.search_ticket()  # 查票
        self.ticket_informations()  # 选择需要买的的火车票
        self.buy_ticket()  # 买票

    # 析构函数，结束driver
    def __del__(self):
        self.driver.quit()
        pass

    # 获得driver
    def set_driver(self):
        options = webdriver.ChromeOptions()
        location = os.path.join(os.path.dirname(__file__), 'chrome-win/chrome.exe')  # chrome地址
        options.binary_location = location
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 反反爬虫
        chromdriverLocation = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')  # chromdriver地址
        self.driver = webdriver.Chrome(chromdriverLocation, options=options)
        self.driver.maximize_window()  # 设置窗口最大化
        pass

        # 登录

    # 登录
    def login(self):
        try:
            self.driver.get(self.login_url)
            # 防止被识别为selenium登录
            script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,});'
            self.driver.execute_script(script)
            # 用户名输入框
            username_input = self.driver.find_element(by=By.XPATH,
                                                      value="//div[@class='login-account']/div[@class='login-item'][1]/input")
            # 密码输入框
            password_input = self.driver.find_element(by=By.XPATH,
                                                      value="//div[@class='login-account']/div[@class='login-item'][2]/input")
            # 登录按钮
            login_button = self.driver.find_element(by=By.XPATH,
                                                    value="//div[@class='login-account']/div[@class='login-btn']")
            # 输入用户名密码
            username_input.send_keys("%s" % self.info['username'])
            password_input.send_keys("%s" % self.info['password'])
            # 登录
            login_button.click()

            sleep(1)  # 点击登录后等待一秒，让验证窗口出现

            # 验证
            self.verify()

            # 如果跳出刷新按钮
            while self.isExist("//a[@id='nc_1_refresh1']"):
                self.driver.find_element(by=By.XPATH, value="//a[@id='nc_1_refresh1']").click()
                sleep(0.5)
                self.verify()
            sleep(3)
        except:
            traceback.print_exc()
            self.driver.quit()
        pass

    # 查询车票
    def search_ticket(self):
        try:
            # 处理弹窗
            if self.isExist("//div[@class='modal']/div[@class='modal-ft']/a"):
                self.driver.find_element(by=By.XPATH, value="//div[@class='modal']/div[@class='modal-ft']/a").click()
            # 点击首页 切换到首页
            shouye = self.driver.find_element(by=By.ID, value="J-index")
            shouye.find_element(by=By.XPATH, value="./a").click()

            sleep(1)

            # 单程搜索框
            search_form = self.driver.find_element(by=By.XPATH,
                                                   value="//div[@class='search-main-item'][1]/div/div/div[@class='search-tab-item'][1]/div[@class='search-form'] ")
            # 出发输入框  input
            outset = search_form.find_element(by=By.XPATH, value=
            "./div[@class='form-item-group']/div[@class='form-item'][1]/div/div/input[1]")
            # 终点输入框  input
            terminal = search_form.find_element(by=By.XPATH, value=
            "./div[@class='form-item-group']/div[@class='form-item'][2]/div/div/input[1]")
            # 时间输入框
            Time_input = search_form.find_element(by=By.XPATH, value="./div[@class='form-item']/div/div/input")
            # 查询
            search_ = search_form.find_element(by=By.XPATH, value="./div[@class='form-item form-item-btn']")

            # 设置出发点与终点和时间
            self.driver.execute_script("arguments[0].value='%s';" % self.info['start'], outset)
            self.driver.execute_script("arguments[0].value='%s';" % self.info['end'], terminal)
            self.driver.execute_script("arguments[0].value='%s';" % self.info['time'], Time_input)

            # 查询
            search_.click()

            # 得到value
            # terminal_value = terminal.get_attribute('value')
            sleep(3)
        except:
            traceback.print_exc()
            self.driver.quit()

        pass

    # 选择需要买的的火车票
    def ticket_informations(self):
        self.driver.switch_to.window(self.driver.window_handles[1])  # 切换到查询的火车票窗口
        tr = self.driver.find_elements(by=By.XPATH, value="//div[@id='t-list']/table/tbody[1]/tr")  # 所有车次selenium列表
        # 目标车次的selenium对象
        if not self.isExist("//div[@id='t-list']/table/tbody[1]/tr[contains(@datatran,'%s')]" % self.info['cc']):
            print("指定车票班次不存在，请修改")
            return

        mubiao = self.driver.find_element(by=By.XPATH,
                                          value="//div[@id='t-list']/table/tbody[1]/tr[contains(@datatran,'%s')]" %
                                                self.info['cc'])
        index = tr.index(mubiao)  # 获得目标车次在所有车次列表中的位置
        print(index)
        target = tr[index - 1].find_element(by=By.XPATH, value="//td[13]")
        # 点击预定，index-1是因为每个车次由两个tr标识，我们定位的是第二个，所以要减一
        tr[index - 1].find_element(by=By.XPATH, value="//td[13]").click()

        sleep(0.5)

        # 如果出现车票临近弹窗
        if self.isExist("//a[@id='qd_closeDefaultWarningWindowDialog_id']"):
            self.driver.find_element(by=By.XPATH, value="//a[@id='qd_closeDefaultWarningWindowDialog_id']").click()
        sleep(1)
        pass

    # 购买车票
    def buy_ticket(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])  # 切换到当前窗口
            # 选择乘车人
            chengcheren = self.driver.find_element(by=By.ID, value="normal_passenger_id")
            chengcheren.find_element(by=By.XPATH,
                                     value="./li[%d]/label" % self.info['index_ccr']).click()  # 选择乘车人，事先选择好
            while not self.isExist("//select[@id='seatType_1']//option[@value='O']"):
                # 无座就刷新
                sleep(1)
                self.driver.refresh()
                sleep(1)
            # 选择坐席
            self.driver.find_element(by=By.XPATH,
                                     value="//select[@id='seatType_1']//option[@value='M']")
            # 提交订单
            self.driver.find_element(by=By.ID, value="submitOrder_id").click()
            # 选坐席
            if self.isExist("//div[@id='erdeng1']/ul/li/a[@id='%s']" % self.info['xz']):
                a = self.driver.find_element(by=By.XPATH,
                                             value="//div[@id='erdeng1']/ul/li/a[@id='%s']" % self.info['xz'])
                # 判断元素是否可以交互
                if a.is_enabled():
                    a.click()
            # 确定信息
            if self.isExist("//a[@id='qr_submit_id']"):
                self.driver.find_element(by=By.XPATH, value="//a[@id='qr_submit_id']")
            # 发送邮箱
            self.set_message('您于{}的{}次列车抢票成功，请自行前往12306App付款'.format(self.info['time'], self.info['cc']))
            # input()
            sleep(20)
        except:
            traceback.print_exc()
            self.driver.quit()

        pass

    # 验证方块
    def verify(self):
        hd = self.driver.find_element(by=By.ID, value="nc_1_n1z")
        huakuai = ActionChains(self.driver)  # 鼠标控制
        huakuai.click_and_hold(hd)  # 定位到滑块
        huakuai.move_by_offset(300, 0)
        huakuai.perform()

    # 登录邮箱
    def __login(self):
        smtp_obj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        smtp_obj.login("1254307036@qq.com", "ivhdphyzovqrgeic")
        smtp_obj.set_debuglevel(0)
        return smtp_obj

    # 发送邮件
    def set_message(self, nr):
        msg = MIMEText(nr, "plain", "utf-8")
        msg['From'] = Header("抢票机器人", 'utf-8')
        msg['To'] = Header('Lucker', 'utf-8')
        msg['Subject'] = Header("Result", "utf-8")

        login = self.__login()  # 登录邮箱
        login.sendmail("1254307036@qq.com", "%s" % self.info['email'], msg.as_string())

        return msg

    # 补充方法，判断某个元素是否存在
    def isExist(self, value):
        try:
            self.driver.find_element(by=By.XPATH, value=value)
            # 运行成功返回true
            return True
        except:
            return False  # 失败返回false
