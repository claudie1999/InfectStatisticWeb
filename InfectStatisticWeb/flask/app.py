from flask import Flask, render_template,jsonify
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Line
from pyecharts.globals import ChartType, SymbolType
from pyecharts.globals import ThemeType

from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import json
import pandas as pd

app = Flask(__name__, static_folder="templates",)


# 第一部分：图表创建
# 01.实时疫情地图
def map_base()->Map:
    # 数据暂时写死：后续可以结合实时数据，进行更新

    # 省和直辖市
    province_distribution = {'湖北': 11756, '北京': 80, '香港': 55, '广东': 49, '甘肃': 38, '台湾': 32, '四川': 25, '上海': 25, '黑龙江': 22, '浙江': 15, '山东': 12, '陕西': 11, '辽宁': 11, '广西': 7, '重庆': 4, '宁夏': 3, '内蒙古': 3, '河南': 2, '河北': 2, '云南': 2, '海南': 2, '江苏': 1, '贵州': 1, '天津': 1, '吉林': 1, '湖南': 0, '安徽': 0, '江西': 0, '福建': 0, '山西': 0, '新疆': 0, '青海': 0, '澳门': 0, '西藏': 0}
    province = list(province_distribution.keys())
    values = list(province_distribution.values())

    # province_distribution = {}
    # with open('data/province.csv', 'r', encoding="UTF-8") as f:
    #     next(f)
    #     dataLine = f.readline().strip("")
    #     while dataLine != "":
    #         tmpList = dataLine.split(",")
    #         province_distribution[tmpList[1]] = int(tmpList[2])
    #         dataLine = f.readline().strip("\n")
    #     f.close()

    # province = list(province_distribution.keys())
    # values = list(province_distribution.values())

    c = (
        Map()
        .add("确诊人数", [list(z) for z in zip(province,values)], "china")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情地图"),
            visualmap_opts=opts.VisualMapOpts(max_= 100),)
        )
    return c


# 02. 疫情新增趋势图
def conf_new_base() -> Line:
    # 静态数据
    # df = pd.read_excel("data/linedata.xlsx",
    #                     usecols=[1],
    #                     names=None)  # 读取项目名称列,不要列名
    # df_li = df.values.tolist()
    # dataY1 = []
    # dataY2 = []
    # dataX = []
    # for s_li in df_li:
    #     dataY1.append(s_li[0])
    #     dataY2.append(s_li[0])
    #     dataX.append(s_li[0])
    # print(result)

    dataY1 = [77, 259, 769, 1737, 2590, 3887, 3399, 2478, 5090, 2048, 394, 648, 406, 427, 125, 143, 40, 15]
    dataY2 = [27, 680, 3806, 4148, 4562, 3971, 4214, 3536, 2450, 1563, 1277, 882, 439, 248, 129, 102, 60, 33]
    dataX = ['2020.01.21', '2020.01.24', '2020.01.27', '2020.01.30', '2020.02.02', '2020.02.05',
             '2020.02.08', '2020.02.11', '2020.02.14', '2020.02.17', '2020.02.20', '2020.02.23',
             '2020.02.26', '2020.02.29', '2020.03.03', '2020.03.06', '2020.03.09', '2020.03.11']
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(dataX)
        .add_yaxis("新增确诊", dataY1, is_smooth=True)
        .add_yaxis("新增疑似", dataY2, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情新增确诊/疑似趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


# 03. 全国现存确诊/疑似趋势图
def conf_total_base() -> Line:
    # 静态数据
    dataY1 = [291, 440, 571, 830, 1287, 1975, 2744, 4515, 5974, 7711, 9692, 11791, 14380, 17205, 20438, 24324]
    dataY2 = [54, 37, 393, 1072, 1965, 2684, 5794, 6973, 9239, 12167, 15238, 17988, 19544, 21558,23214, 23260]

    dataX = ['2020.01.21', '2020.01.24', '2020.01.27', '2020.01.30', '2020.02.02', '2020.02.05',
             '2020.02.08', '2020.02.11', '2020.02.14', '2020.02.17', '2020.02.20', '2020.02.23',
             '2020.02.26', '2020.02.29', '2020.03.03', '2020.03.06', '2020.03.09', '2020.03.11']
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(dataX)
        .add_yaxis("现存确诊", dataY1, is_smooth=True)
        .add_yaxis("现存疑似", dataY2, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情现存确诊/疑似趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


# 04. 全国累计死亡/治愈趋势图
def dead_total_base() -> Line:
    # 静态数据
    dataY1 = [0, 25, 80, 170, 304, 490, 722, 1016, 1380, 1770, 2118, 2442, 2715, 2835, 2943, 3042, 3119, 3169]
    dataY2 = [0, 34, 51, 124, 328, 892, 2050, 3996, 6723, 10844, 16155, 22888, 29745, 39002, 47204, 53726, 58600, 62793]

    dataX = ['2020.01.21', '2020.01.24', '2020.01.27', '2020.01.30', '2020.02.02', '2020.02.05',
             '2020.02.08', '2020.02.11', '2020.02.14', '2020.02.17', '2020.02.20', '2020.02.23',
             '2020.02.26', '2020.02.29', '2020.03.03', '2020.03.06', '2020.03.09', '2020.03.11']
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(dataX)
        .add_yaxis("累计死亡", dataY1, is_smooth=True)
        .add_yaxis("累计治愈", dataY2, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情累计死亡/治愈趋势图"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


# 05. 全国各省市数据明细
def table_base():
    table = Table()

    headers = ["地区", "现有确诊", "累计死亡", "累计治愈"]

    rows = [
        ["湖北", 13522, 414, 397],
        ["浙江", 829, 0, 60],
        ["广东", 813, 0, 24],
        ["河南", 675, 2, 20],
        ["湖南", 593, 0, 29],
        ["安徽", 480, 0, 20],
        ["江西", 476, 2, 19],
        ["重庆", 344, 2, 9]
    ]
    table.add(headers, rows).set_global_opts(
        title_opts=ComponentTitleOpts(title="Table", subtitle="副标题")
    )
    # table.render("table_base.html")
    return rows

# 全国疫情概览
# def card_base():
#     table = Table()
#
#     headers = ["现存确诊", "现有疑似", "累计死亡", "累计治愈"]
#
#     rows = [
#         [34253, 13522, 414, 397],
#     ]
#     table.add(headers, rows).set_global_opts(
#         title_opts=ComponentTitleOpts(title="Table", subtitle="副标题")
#     )
#     # table.render("table_base.html")
#     return rows



# 路由配置

# @app.route("/")
# def index():
#     content = card_base()
#     return render_template("index.html", content=content)

@app.route("/")
def index():
    content = table_base()
    return render_template("index.html", content=content)


@app.route("/mapChart")
def get_map_chart():
    c = map_base()
    return c.dump_options_with_quotes()


@app.route("/confChart")
def get_conf_chart():
    c = conf_new_base()
    return c.dump_options_with_quotes()


@app.route("/confTotalChart")
def get_conf_total_chart():
    c = conf_total_base()
    return c.dump_options_with_quotes()


@app.route("/deadTotalChart")
def get_dead_total_chart():
    c = dead_total_base()
    return c.dump_options_with_quotes()


# 主函数
if __name__ == "__main__":
    app.run()
