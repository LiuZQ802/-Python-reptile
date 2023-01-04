from dingpiao import dingpiao


def main():
    #默认二等座、成人票
    info = {
        # SHH:上海 CZH:常州 ...其余自查
        'start': 'SHH:',  # 起始站
        'end': 'CZH',  # 终点站
        'time': '2023-01-18',  # 出发日期
        'username': '14762711008',  # 12306用户名
        'password': 'liuJIA001003',  # 12306密码
        'cc': 'G7066',  # 车次
        'index_ccr': 2,  # 选择第几个乘车人（事先看好）
        'xz':'1A',#选座,1A:A  1C:C 1D:D 1F:F
        'email': '1254307036@qq.com',  # 用于接收结果的邮箱
    }
    action = dingpiao(info)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
