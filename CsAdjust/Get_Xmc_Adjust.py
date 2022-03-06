from selenium import webdriver


def getDriver():
    options = webdriver.ChromeOptions()
    location = r"E:\Python\CsAdjust\chrome-win\chrome.exe"  # chrome地址
    options.binary_location = location
    # 图片不加载
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs',prefs)
    driver = webdriver.Chrome("E:\Python\CsAdjust/chromedriver.exe", options=options)  # chromedriver地址
    return driver


# 获取新窗口的信息
def getCurrentMessage(driver, t):
    driver = driver
    try:
        tr = driver.find_elements_by_xpath("//table[@class='adjust_table']/tbody/tr")  # 基本信息
        bcxinxi = driver.find_element_by_xpath("//div[@class='t_fsz']/table/tbody/tr/td")  # 补充信息
        with open('计算机调剂信息.txt', 'a+', encoding='utf-8') as f:
            f.write(str(t) + "、\n")
            f.write(tr[1].text + '\n')
            f.write(tr[2].text + '\n')
            f.write(tr[4].text + '\n')
            f.write(tr[6].text + '\n')
            f.write("\n补充信息:\n")
            f.write(bcxinxi.text)
            f.write('\n\n\n\n\n\n')

    except Exception as e:
        print(e)
        driver.quit()


def main():
    driver = getDriver()
    t = 1  # 记录第几条数据
    try:
        driver.get(
            "http://muchong.com/bbs/kaoyan.php?formhash=fd1e0da0&school=&r1%5B%5D=08&r2%5B%5D=0812&r3%5B%5D=&year=2022&type=1&oksubmit=%C8%B7%B6%A8")

        # 不断爬取下一页
        while 1:
            tr = driver.find_elements_by_xpath("//tbody[@class='forum_body_manage']/tr")
            for i in tr:
                a = i.find_elements_by_xpath("./td[@class='xmc_lp20']/a")
                a[0].click()  # 点进去一条信息

                driver.switch_to.window(driver.window_handles[1])  # 切换到刚点击的窗口

                getCurrentMessage(driver, t)
                driver.close()  # 关闭当前窗口选项卡
                driver.switch_to.window(driver.window_handles[0])  # 切换到原来窗口
                t += 1

            try:
                driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()  # 点击下一页
            except:
                break  # 最后一页结束循环

        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
