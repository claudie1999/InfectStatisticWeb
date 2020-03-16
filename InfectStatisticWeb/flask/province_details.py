# 运行说明：
# Python 3.x版本，先使用pip install安装第三方库
# pip install fake_useragent
# pip install pyecharts
# pip install requests

import time
from fake_useragent import UserAgent
from pyecharts.charts import Map
from pyecharts import options as opts
import requests
import json

ua = UserAgent()
headers = {'User-Agent': ua.random}
url = "https://c.m.163.com/ug/api/wuhan/app/index/feiyan-data-list"
province = input("请输入省名称(如：湖北)：\n")
print(str('点击相应html文件查看'+province+'疫情地图'))



# 爬取疫情数据
def geturl(url):
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            content_field = json.loads(response.text)
            list_datas_1 = content_field['data']['list']
            return list_datas_1
        else:
            print('返回代码：' + response.status_code)
            return None
    except Exception as e:
        print('此页有问题！', e)
        return None


# 制作疫情地图
def makemap(dict):
    # 省和直辖市
    province_distribution = dict
    value = province_distribution.values()
    # maptype='china' 只显示全国直辖市和省级
    title = str(int(time.strftime("%Y%m%d")) - 1) + province + "疫情地图"
    map = Map()
    map.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True,
                                          pieces=[
                                              # 数据范围分段，分颜色，可以根据数据大小具体分配大小
                                              {"max": 200, "min": 101, "label": ">200", "color": "#780707"},
                                              {"max": 100, "min": 51, "label": "101-200", "color": "#8A0808"},
                                              {"max": 50, "min": 41, "label": "41-50", "color": "#B40404"},
                                              {"max": 40, "min": 31, "label": "31-40", "color": "#CD1111"},
                                              {"max": 30, "min": 21, "label": "21-30", "color": "#DF0101"},
                                              {"max": 20, "min": 11, "label": "11-20", "color": "#F68181"},
                                              {"max": 10, "min": 1, "label": "1-10", "color": "#F5A9A9"},
                                              {"max": 0, "min": 0, "label": "0", "color": "#FFFFFF"},
                                          ], )  # 最大数据范围，分段
    )
    map.add(title, data_pair=province_distribution.items(), maptype=province, is_roam=True)
    map.render(province + '疫情地图.html')


# 生成本省疫情列表
def makedict(list):
    dictProvince = {}
    for item in list:
        for k, v in item.items():
            if (v == province):  # 替换“安徽”，可以查各省的数据
                if (item["confirm"] != None):
                    dictProvince[item['name'] + '市'] = int(item["confirm"])
    return dictProvince


if __name__ == '__main__':
    list_data = geturl(url)
    dict_data = makedict(list_data)
    makemap(dict_data)
