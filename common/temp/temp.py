import xlrd

QINIU_AREA_DICT = {
    'shandong': '山东省',
    'jiangsu': '江苏省',
    'zhejiang': '浙江省',
    'anhui': '安徽省',
    'fujian': '福建省',
    'jiangxi': '江西省',
    'guangdong': '广东省',
    'hainan': '海南省',
    'henan': '河南省',
    'hunan': '湖南省',
    'hubei': '湖北省',
    'hebei': '河北省',
    'shanxi': '山西省',
    'qinghai': '青海省',
    'gansu': '甘肃省',
    'shaanxi': '陕西省',
    'sichuan': '四川省',
    'guizhou': '贵州省',
    'yunnan': '云南省',
    'liaoning': '辽宁省',
    'jilin': '吉林省',
    'heilongjiang': '黑龙江省',
    'hongkong': '香港',
    'macau': '澳门',
    'taiwan': '台湾',
    'beijing': '北京',
    'tianjin': '天津',
    'chongqing': '重庆',
    'shanghai': '上海',
    'xizang': '西藏',
    'xinjiang': '新疆',
    'guangxi': '广西',
    'ningxia': '宁夏',
    'Inner Mongolia': '内蒙古',
    # 'unknown': '其他',
}

def foo():
    """"""

    data = xlrd.open_workbook('aa.xlsx')
    print(data)
    table = data.sheets()[0]

    c = table.col_values(0)
    e = table.col_values(1)
    f = table.col_values(2)

    dict_a = {}
    for i in zip(e, f):
        dict_a[i[0]] = i[1].capitalize()

    for k in QINIU_AREA_DICT:
        v = QINIU_AREA_DICT[k]

        if '省' in v:
            v = v[:-1]

        dict_a[v] = k.capitalize()

    print(dict_a)


def foo1():
    """"""

    data = xlrd.open_workbook('aa.xlsx')
    print(data)
    table = data.sheets()[0]

    c = table.col_values(0)
    e = table.col_values(1)
    f = table.col_values(2)

    dict_a = {}
    for i in zip(e, c):
        dict_a[i[0]] = i[1]

    for k in QINIU_AREA_DICT:
        v = QINIU_AREA_DICT[k]

        if '省' in v:
            v = v[:-1]

        dict_a[v] = 'CN'

    print(dict_a)


if __name__ == '__main__':
    foo1()