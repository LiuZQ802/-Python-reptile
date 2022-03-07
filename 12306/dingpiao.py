from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
from selenium.webdriver.common.action_chains import ActionChains


class dingpiao(object):

    # 构造函数，初始化url、出发站、终点站、出发时间、登录用户名、登录密码
    def __init__(self, start, end, time, username, password, cc):
        self.url = "https://www.12306.cn/index/"  # 主页
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"  # 登录页面
        self.driver = None  # driver
        self.start = start  # 出发站
        self.end = end  # 终点站
        self.time = time  # 出发时间
        self.cc = cc
        self.username = username  # 用户名
        self.password = password  # 密码

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
        location = r"E:/Python/爬虫小项目/chrome-win/chrome.exe"  # chrome地址
        options.binary_location = location
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome("E:/Python/爬虫小项目/chromedriver.exe", options=options)
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
            username_input.send_keys("%s" % self.username)
            password_input.send_keys("%s" % self.password)
            # 登录
            login_button.click()

            sleep(1)  # 点击登录后等待一秒，让验证窗口出现

            # 验证
            hd = self.driver.find_element(by=By.ID, value="nc_1_n1z")
            huakuai = ActionChains(self.driver)  # 鼠标控制
            huakuai.click_and_hold(hd)  # 定位到滑块
            huakuai.move_by_offset(300, 0)
            huakuai.perform()

            sleep(2)
        except:
            traceback.print_exc()
            self.driver.quit()
        pass

    # 查询车票
    def search_ticket(self):
        try:
            # get网站
            self.driver.get(self.url)

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
            self.driver.execute_script("arguments[0].value='%s';" % self.start, outset)
            self.driver.execute_script("arguments[0].value='%s';" % self.end, terminal)
            self.driver.execute_script("arguments[0].value='%s';" % self.time, Time_input)

            # 查询
            search_.click()

            # 得到value
            # terminal_value = terminal.get_attribute('value')
            sleep(2)
        except:
            traceback.print_exc()
            self.driver.quit()

        pass

    # 选择需要买的的火车票
    def ticket_informations(self):
        self.driver.switch_to.window(self.driver.window_handles[1])  # 切换到查询的火车票窗口
        tr = self.driver.find_elements(by=By.XPATH, value="//div[@class='t-list']/table/tbody[1]/tr")  # 所有车次selenium列表
        # 目标车次的selenium对象
        mubiao = self.driver.find_element(by=By.XPATH,
                                          value="//div[@class='t-list']/table/tbody[1]/tr[contains(@datatran,'%s')]" % self.cc)
        index = tr.index(mubiao)  # 获得目标车次在所有车次列表中的位置
        # 点击预定，index-1是因为每个车次由两个tr标识，我们定位的是第二个，所以要减一
        tr[index - 1].find_element(by=By.XPATH, value="//div[@class='t-list']/table/tbody[1]/tr[13]/td[13]").click()

        sleep(2)
        pass

    # 购买车票
    def buy_ticket(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])  # 切换到当前窗口
            # 选择乘车人
            chengcheren = self.driver.find_element(by=By.ID, value="normal_passenger_id")
            chengcheren.find_element(by=By.XPATH, value="./li[2]").click()  # 选择乘车人，事先选择好
            # 提交订单
            self.driver.find_element(by=By.ID, value="submitOrder_id").click()

            sleep(20)
        except:
            traceback.print_exc()
            self.driver.quit()

        pass
