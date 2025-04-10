import numpy as np
import pandas as pd
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import datetime

data_haed = pd.read_excel(r"E:/data analyze/春节档-电影票房表现概览.xlsx")
data_haed.head(1)

data_haed["首映票房"] = data_haed["首映票房"].apply(lambda x: round(x/100000000, 2))
data_haed["首周票房"] = data_haed["首周票房"].apply(lambda x: round(x/100000000, 2))
data_haed["首周末票房"] = data_haed["首周末票房"].apply(lambda x: round(x/100000000, 2))

data_haed = data_haed.rename(columns={"首映票房": "首映票房/亿", "首周票房": "首周票房/亿", "首周末票房": "首周末票房/亿"})

data_haed.info()

data_haed = data_haed.drop(labels=["EntMovieID","DBOMovieID","EFMTMovieID","GenreMainID"],axis=1)

colums = list(data_haed)
print(colums)

headers = colums
rows_all = data_haed[colums].apply(lambda x: list(x), axis=1).values.tolist()

table_all = Table()
attributes = {"class": "fl-table", "style": "margin: 0 auto"}  # 居中显示
table_all.add(headers, rows_all, attributes)
table_all.set_global_opts(
    title_opts=ComponentTitleOpts(title=f"春节档-电影详情数据概览", subtitle="（上下左右移动表格）")
)
table_all.render_notebook()

data_movie_time = pd.read_excel(r"E:/data analyze/春节档-电影票房三十日时段详情.xls")

data_movie_time["当前票房/万"] = data_movie_time["当前票房/万"].apply(lambda x: round(x / 10000000, 2))
data_movie_time["当前场次"] = data_movie_time["当前场次"].apply(lambda x: round(x / 10000, 2))
data_movie_time["当前人次/万"] = data_movie_time["当前人次/万"].apply(lambda x: round(x / 1000000, 2))

data_movie_time = data_movie_time.rename(
    columns={"当前票房/万": "当前票房/千万", "当前场次": "当前场次/万", "当前人次/万": "当前人次/百万"})
data_movie_time = data_movie_time[data_movie_time['日期'] <= '2022-02-07']
data_movie_time.head(2)

data_movie_time['电影'].value_counts()

movie_chang = data_movie_time[data_movie_time["电影"] == "长津湖之水门桥"]

line = Line(
    init_opts=opts.InitOpts(
        theme='light',
        width='1000px',
        height='600px')
)

line.add_xaxis(
    movie_chang["日期"].tolist()
)

colums = ["当前票房/千万", "当前人次/百万", "当前场次/万"]
for i in range(3):
    line.add_yaxis(
        colums[i],
        movie_chang[colums[i]],
        is_symbol_show=False,
        is_smooth=True,
        #is_selected=True,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
        z=100,
        linestyle_opts={
            "normal": {
                "shadowColor": 'rgba(0, 0, 0, .5)',
                "shadowBlur": 0,
                "shadowOffsetY": 1,
                "shadowOffsetX": 1,
            },
        },
    )

line.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        boundary_gap=False,
        axislabel_opts=opts.LabelOpts(margin=30, color="black"),
        axistick_opts=opts.AxisTickOpts(is_show=False), ),
    yaxis_opts=opts.AxisOpts(
        name='',
        axisline_opts=opts.AxisLineOpts(is_show=True),
        axistick_opts=opts.AxisTickOpts(is_show=False),
        splitline_opts=opts.SplitLineOpts(
            is_show=True,
            linestyle_opts=opts.LineStyleOpts(color='#483D8B'))
    ),
    tooltip_opts=opts.TooltipOpts(
        is_show=True, trigger='axis', axis_pointer_type='cross'),
    title_opts=opts.TitleOpts(title="长津湖上映后一周电影票房表现",  # 标题
                              title_textstyle_opts=opts.TextStyleOpts(font_size=18),  # 主标题字体大小
                              subtitle="2022-02-01~2022-02-07",  # 次坐标轴
                              pos_left='center'),  # 标题位置
    legend_opts=opts.LegendOpts(
        is_show=True,
        pos_top=45,
        orient="horizontal"
    ),  # 不显示图例

    graphic_opts=[
        opts.GraphicGroup(
            graphic_item=opts.GraphicItem(id_='1', left="center", top="center", z=-1),
            children=[
                opts.GraphicImage(graphic_item=opts.GraphicItem(id_="logo",
                                                                left='center',
                                                                z=-1),
                                  graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                                      # 设置背景图片
                                      # image="https://img2.baidu.com/it/u=3979355417,3562690433&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=388",
                                      width=1000,
                                      height=600,
                                      opacity=0.5, )
                                  )
            ]
        )
    ]
)

line.set_series_opts(

    markarea_opts=opts.MarkAreaOpts(
        is_silent=True,
        label_opts=opts.LabelOpts(position='bottom', color='#000000'),
        itemstyle_opts=opts.ItemStyleOpts(color='#1E90FF', opacity=0.2),
        data=[
            opts.MarkAreaItem(name="正式上映\n春节档", x=("2022-02-01", "2022-02-02")),
            # opts.MarkAreaItem(name="高峰期", x=("2021-10-05", "2021-10-07")),
            # opts.MarkAreaItem(name="第三周\n小高峰", x=("2021-10-15", "2021-10-17")),
        ]
    ),
)
line.set_colors(colors=['#80FFA5', '#00DDFF', '#FF0087'])
line.render_notebook()

# 读入数据
data = pd.read_excel(r"E:/data analyze/春节档-票房详情.xlsx")
data.head(5)

def tranform_data(x):
    x = round(x / 10000, 2)
    return x

data['票房/(万)'] = data['票房'].apply(lambda x: tranform_data(x))

data['票房/(万)'] = data['票房'].apply(lambda x: tranform_data(x))
data_7 = data[data["日期"] >= "2022-02-01"]

bar = (
    Bar(init_opts=opts.InitOpts(
        theme='light',
        width='980px',
        height='500px'
    ))  # 设置图表大小
        .add_xaxis(xaxis_data=data_7['日期'].tolist())  # x轴
        .add_yaxis(
        series_name="场次",  # 柱形图系列名称
        y_axis=data_7['场次'].tolist(),  # 数据
        label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
        itemstyle_opts=opts.AreaStyleOpts(
            opacity=0.8,
            color=JsCode("""
                            new echarts.graphic.LinearGradient(
                            0, 0, 0, 1,
                            [{offset: 0, color: 'rgba(30,144,255)'},
                             {offset: 1, color: 'rgba(30,144,255,0.5)'}],
                              false)
                            """)
        )
    )
        .add_yaxis(
        series_name="人次",  # 柱形图系列名称
        y_axis=data_7['人次'].tolist(),  # 数据
        label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
        itemstyle_opts=opts.AreaStyleOpts(
            opacity=0.8,
            color=JsCode("""
                             new echarts.graphic.LinearGradient(
                                           0, 0, 0, 1,
                                           [{offset: 0, color: '#ed556a'},
                                            {offset: 1, color: '#ee3f4d'}],
                                           false)
                           """)
        )
    )

        .extend_axis(  # 设置次坐标轴
        yaxis=opts.AxisOpts(
            name="",  # 次坐标轴名称
            type_="value",  # 次坐标手类型
            min_=-4000,  # 最小值
            max_=200000,  # 最大值
            is_show=False,  # 是否显示
            axisline_opts=opts.AxisLineOpts(is_show=False,  # y轴线不显示
                                            linestyle_opts=opts.LineStyleOpts(color='#00ca95')),  # 设置线颜色, 字体颜色也变
            axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线不显示
            axislabel_opts=opts.LabelOpts(formatter="{value}"),  # 次坐标轴数据显示格式
        )
    )

        .set_global_opts(title_opts=opts.TitleOpts(title="2022年春节电影票房大盘",  # 标题
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
                                                   subtitle="2022-02-01~2022-02-07",  # 次坐标轴
                                                   pos_left='center'),  # 标题位置
                         legend_opts=opts.LegendOpts(
                             is_show=True,
                             pos_top=50,
                             orient="horizontal"
                         ),  # 不显示图例
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis",
                             axis_pointer_type="shadow"
                         ),  # 提示框
                         xaxis_opts=opts.AxisOpts(name='',
                                                  type_='category',
                                                  axislabel_opts=opts.LabelOpts(rotate=360),
                                                  ),
                         yaxis_opts=opts.AxisOpts(type_="value",  # y轴类型
                                                  is_show=False,
                                                  # max_=5000000,
                                                  name='',  # y轴名称
                                                  name_location='middle',  # y轴名称位置
                                                  name_gap=70,  # y轴名称距离轴线距离
                                                  axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线
                                                  axisline_opts=opts.AxisLineOpts(is_show=True),  # y轴线
                                                  splitline_opts=opts.SplitLineOpts(is_show=True),  # y轴网格线
                                                  axislabel_opts=opts.LabelOpts(formatter="{value}")),  # 轴标签显示方式
                         )
)

line = (
    Line()
        .add_xaxis(xaxis_data=data_7['日期'].tolist())  # x轴
        .add_yaxis(
        series_name="票房/(万)",  # 名称
        yaxis_index=1,  # 次坐标
        is_smooth=True,  # 线条样式  , 是否设置成圆滑曲线
        y_axis=data_7['票房/(万)'].tolist(),
        itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: '#2486b9'
                                    }, {
                                        offset: 1,
                                        color: '#FF00FF'
                                    }], false)""", ),
                "opacity": 0.7,
                "barBorderRadius": [45, 45, 45, 45],
                "shadowColor": 'rgb(0, 160, 221)',
            }},
        linestyle_opts={
            'normal': {
                'width': 4,
                'shadowColor': 'rgba(0, 0, 0, 0.5)',
                'shadowBlur': 5,
                'shadowOffsetY': 10,
                'shadowOffsetX': 10,
                'curve': 0.7,
                'color': '#2486b9'
            }
        },
        label_opts=opts.LabelOpts(is_show=False),  # 显示数据标签
    )
)

bar.overlap(line)  # 图表组合
bar.render_notebook()

data = pd.read_excel(r'E:/data analyze/春节档-电影票房表现概览.xlsx')

data["累计票房"] = data["累计票房"].apply(lambda x: round(x / 10000000, 2))
data["累计场次"] = data["累计场次"].apply(lambda x: round(x / 10000, 2))
data["累计人次"] = data["累计人次"].apply(lambda x: round(x / 1000000, 2))

data = data.rename(columns={"累计票房": "累计票房/千万", "累计场次": "累计场次/万", "累计人次": "累计人次/百万"})
data = data[data['正式上映日期'] == '2022-02-01']
data.head(1)

movies = data['电影'].tolist()
movies

bar_china = (
    Bar(init_opts=opts.InitOpts(width="1200px", height="600px", theme='light'))  # 设置图表大小
        .add_xaxis(xaxis_data=data['电影'].tolist())  # x轴
        .add_yaxis(
        series_name="累计票房/千万",  # 柱形图系列名称
        stack='stack1',
        y_axis=data['累计票房/千万'].tolist(),  # 数据
        label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c} /千万"),  # 显示数据标签
        itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: '#126bae'
                }, {
                    offset: 1,
                    color: '#619ac3'
                }], false)""", ),
                "opacity": 0.8,
                #                 "barBorderRadius": [20, 20, 0, 0],
                'shadowBlur': 4,
                'shadowColor': 'rgba(0, 0, 0, 0.3)',
                'shadowOffsetX': 5,
                'shadowOffsetY': 5,
                'borderColor': 'rgb(220,220,220)',
                'borderWidth': 1
            }}
    )
        .add_yaxis(
        series_name="累计人次/百万",  # 柱形图系列名称
        stack='stack1',
        y_axis=data['累计人次/百万'].tolist(),  # 数据
        label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c} /百万"),  # 显示数据标签
        itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: '#ea7293'
                }, {
                    offset: 1,
                    color: '#ec8aa4'
                }], false)""", ),
                "opacity": 0.8,
                #                 "barBorderRadius": [20, 20, 0, 0],
                'shadowBlur': 4,
                'shadowColor': 'rgba(0, 0, 0, 0.3)',
                'shadowOffsetX': 5,
                'shadowOffsetY': 5,
                'borderColor': 'rgb(220,220,220)',
                'borderWidth': 1
            }}
    )

        .add_yaxis(
        series_name="累计场次/万",  # 柱形图系列名称
        stack='stack1',
        y_axis=data['累计场次/万'].tolist(),  # 数据
        label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c} /万"),  # 显示数据标签
        itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: '#9eccab'
                }, {
                    offset: 1,
                    color: '#a4cab6'
                }], false)""", ),
                "opacity": 0.8,
                #                 "barBorderRadius": [20, 20, 0, 0],
                'shadowBlur': 4,
                'shadowColor': 'rgba(0, 0, 0, 0.3)',
                'shadowOffsetX': 5,
                'shadowOffsetY': 5,
                'borderColor': 'rgb(220,220,220)',
                'borderWidth': 1
            }}
    )

        .reversal_axis()
        # .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="春节档上映电影票房表现概览",  # 标题
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 主标题字体大小
                                                   subtitle="",  # 次坐标轴
                                                   pos_left='center'),  # 标题位置
                         legend_opts=opts.LegendOpts(
                             is_show=True,
                             pos_top=30,
                             orient="horizontal"
                         ),  # 不显示图例
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis",
                             axis_pointer_type="shadow"
                         ),  # 提示框
                         yaxis_opts=opts.AxisOpts(name='',
                                                  type_='category',
                                                  #    axislabel_opts=opts.LabelOpts(rotate=30),
                                                  ),
                         xaxis_opts=opts.AxisOpts(type_="value",  # y轴类型
                                                  #   max_=5000000,
                                                  name='',  # y轴名称
                                                  name_location='middle',  # y轴名称位置
                                                  name_gap=70,  # y轴名称距离轴线距离
                                                  axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线
                                                  axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
                                                  splitline_opts=opts.SplitLineOpts(is_show=True),  # y轴网格线
                                                  axislabel_opts=opts.LabelOpts(formatter="{value}")),  # 轴标签显示方式
                         # datazoom_opts=opts.DataZoomOpts(is_zoom_lock=False,
                         #                                 orient="vertical")
                         )
)
bar_china.render_notebook()

data_move_diyu = pd.read_excel(r'E:/data analyze/春节档-排片地域分布（场次）-top10影片.xlsx')
data_move_diyu.head(5)

data_move_diyu = data_move_diyu.drop(data_move_diyu[(data_move_diyu['电影'] == "CLevel") | (data_move_diyu['电影'] == "CityLevel")].index)
data_move_diyu["电影"] = data_move_diyu["电影"].apply(lambda x: x.split("|")[-1])
data_move_diyu.head(5)

data_move_diyu = data_move_diyu.fillna(0)
data_move_diyu['场次'] = data_move_diyu['场次'].astype(int)

one_city = data_move_diyu[(data_move_diyu['城市'] == '一线城市')]
two_city = data_move_diyu[(data_move_diyu['城市'] == '二线城市')]
three_city = data_move_diyu[(data_move_diyu['城市'] == '三线城市')]
four_city = data_move_diyu[(data_move_diyu['城市'] == '四线城市')]
five_city = data_move_diyu[(data_move_diyu['城市'] == '五线城市')]
one_city.head(5)

one_city_movie = one_city.groupby('电影')['场次'].sum().reset_index().sort_values('场次', ascending=False).reset_index(
            drop=True)[:10]
one_city_movie = one_city_movie.rename(columns = {'场次': '一线城市场次'})
two_city_movie = two_city.groupby('电影')['场次'].sum().reset_index().sort_values('场次', ascending=False).reset_index(
            drop=True)
two_city_movie = two_city_movie.rename(columns = {'场次': '二线城市场次'})
three_city_movie = three_city.groupby('电影')['场次'].sum().reset_index().sort_values('场次', ascending=False).reset_index(
            drop=True)
three_city_movie = three_city_movie.rename(columns = {'场次': '三线城市场次'})
four_city_movie = four_city.groupby('电影')['场次'].sum().reset_index().sort_values('场次', ascending=False).reset_index(
            drop=True)
four_city_movie = four_city_movie.rename(columns = {'场次': '四线城市场次'})
five_city_movie = five_city.groupby('电影')['场次'].sum().reset_index().sort_values('场次', ascending=False).reset_index(
            drop=True)
five_city_movie = five_city_movie.rename(columns = {'场次': '五线城市场次'})

move_top_10 = one_city_movie.merge(two_city_movie, how='left', on='电影').fillna(0)
move_top_10 = move_top_10.merge(three_city_movie, how='left', on='电影').fillna(0)
move_top_10 = move_top_10.merge(four_city_movie, how='left', on='电影').fillna(0)
move_top_10 = move_top_10.merge(five_city_movie, how='left', on='电影').fillna(0)
move_top_10

paipian_top = pd.read_excel(r'E:/data analyze/春节档-排片统计（场次）-top10影片.xlsx')
paipian_top.head(5)

paipian_top.groupby('电影')['场次'].sum()

bar_diyu = (
    Bar(init_opts=opts.InitOpts(width="1200px", height="600px", theme='light')) # 设置图表大小
    .add_xaxis(xaxis_data=move_top_10['电影'].tolist())  # x轴
    .add_yaxis(
        series_name="一线城市",  #柱形图系列名称
        stack='stack1',
        y_axis=move_top_10['一线城市场次'].tolist(), # 数据
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), # 显示数据标签
        itemstyle_opts=opts.ItemStyleOpts(color="#8e97e2",opacity=0.8),     # 柱形图颜色及透明度
        )
    .add_yaxis(
        series_name="二线城市",  #柱形图系列名称
        stack='stack1',
        y_axis=move_top_10['二线城市场次'].tolist(), # 数据
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), # 显示数据标签
        itemstyle_opts=opts.ItemStyleOpts(color="#ed9b9b",opacity=0.8),     # 柱形图颜色及透明度
        )
    .add_yaxis(
        series_name="三线城市",  #柱形图系列名称
        stack='stack1',
        y_axis=move_top_10['三线城市场次'].tolist(), # 数据
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), # 显示数据标签
        itemstyle_opts=opts.ItemStyleOpts(color="#4fc0cc",opacity=0.8),     # 柱形图颜色及透明度
        )
    .add_yaxis(
        series_name="四线城市",  #柱形图系列名称
        stack='stack1',
        y_axis=move_top_10['四线城市场次'].tolist(), # 数据
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), # 显示数据标签
        itemstyle_opts=opts.ItemStyleOpts(color="#f7ce8f",opacity=0.8),     # 柱形图颜色及透明度
        )
    .add_yaxis(
        series_name="五线城市",  #柱形图系列名称
        stack='stack1',
        y_axis=move_top_10['五线城市场次'].tolist(), # 数据
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), # 显示数据标签
        itemstyle_opts=opts.ItemStyleOpts(color="#7fa7c1",opacity=0.8),     # 柱形图颜色及透明度
        )
    .reversal_axis()
    # .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=[
            dict(
                text='春节档 - 排片地域分布（累计场次）',
                left='left',
                textStyle=dict(
                    color='#000',
                    fontSize=20)),
            dict(
                text='春节档 - 排片统计（累计场次）',
                left='60%',
                top='10%',
                textStyle=dict(
                    color='#000',
                    fontSize=16)),
        ],
                    legend_opts=opts.LegendOpts(
                                             is_show=False,),  # 不显示图例
                    tooltip_opts=opts.TooltipOpts(
                                             trigger="axis",
                                             axis_pointer_type="shadow"
                                             ),# 提示框
                    yaxis_opts=opts.AxisOpts(name='',
                                            type_='category',
                                            #    axislabel_opts=opts.LabelOpts(rotate=30),
                                               ),
                     xaxis_opts=opts.AxisOpts(type_="value", # y轴类型
                                            #   max_=5000000,
                                              name='', # y轴名称
                                              name_location='middle', # y轴名称位置
                                              name_gap=70,  # y轴名称距离轴线距离
                                              axistick_opts=opts.AxisTickOpts(is_show=False),   # 刻度线
                                              axisline_opts=opts.AxisLineOpts(is_show=False),   # y轴线
                                              splitline_opts=opts.SplitLineOpts(is_show=True),   # y轴网格线
                                              axislabel_opts=opts.LabelOpts(formatter="{value}")), # 轴标签显示方式
                                               )
)
pie = (Pie(init_opts=opts.InitOpts(theme='light'))
    .add('', [list(z) for z in zip(paipian_top.groupby('电影')['场次'].sum().index.tolist(),
        paipian_top.groupby('电影')['场次'].sum().values.tolist())],radius=['45','100'],center=['70%','40%'])
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}：{c}  {d}%'))
    .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    )
bar_diyu.overlap(pie)
bar_diyu.render_notebook()

t2 = Timeline(init_opts=opts.InitOpts(width="1200px", height="600px", theme='light'))
t2.add_schema(is_auto_play=True, is_loop_play=True, is_timeline_show=False, play_interval=1000)

for d in range(1, 7):  # 指定多个月份

    one_city_movie = data_move_diyu[
        (data_move_diyu['城市'] == '一线城市') & (data_move_diyu['日期'] == f"2022-02-0{d}")]
    two_city_movie = data_move_diyu[
        (data_move_diyu['城市'] == '二线城市') & (data_move_diyu['日期'] == f"2022-02-0{d}")]
    three_city_movi = data_move_diyu[
        (data_move_diyu['城市'] == '三线城市') & (data_move_diyu['日期'] == f"2022-02-0{d}")]
    four_city_movi = data_move_diyu[
        (data_move_diyu['城市'] == '四线城市') & (data_move_diyu['日期'] == f"2022-02-0{d}")]
    five_city_movi = data_move_diyu[
        (data_move_diyu['城市'] == '五线城市') & (data_move_diyu['日期'] == f"2022-02-0{d}")]

    one_city_movie = one_city_movie.rename(columns={'场次': '一线城市场次'})
    two_city_movie = two_city_movie.rename(columns={'场次': '二线城市场次'})
    three_city_movie = three_city_movie.rename(columns={'场次': '三线城市场次'})
    four_city_movie = four_city_movie.rename(columns={'场次': '四线城市场次'})
    five_city_movie = five_city_movie.rename(columns={'场次': '五线城市场次'})

    move_top_10 = one_city_movie.merge(two_city_movie, how='left', on='电影').fillna(0)
    move_top_10 = move_top_10.merge(three_city_movie, how='left', on='电影').fillna(0)
    move_top_10 = move_top_10.merge(four_city_movie, how='left', on='电影').fillna(0)
    move_top_10 = move_top_10.merge(five_city_movie, how='left', on='电影').fillna(0)

    move_top_10 = move_top_10.rename(columns={"日期_x": "日期", "城市_x": "城市"})

    paipian = paipian_top[(paipian_top['日期'] == f"2022-02-0{d}")][:10]

    bar_diyu_pie = (
        Bar(init_opts=opts.InitOpts(width="1200px", height="600px"))  # 设置图表大小
        .add_xaxis(xaxis_data=move_top_10['电影'].tolist())  # x轴
        .add_yaxis(
            series_name="一线城市",  # 柱形图系列名称
            stack='stack1',
            y_axis=move_top_10['一线城市场次'].tolist(),  # 数据
            label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#8e97e2", opacity=0.8),  # 柱形图颜色及透明度
        )
        .add_yaxis(
            series_name="二线城市",  # 柱形图系列名称
            stack='stack1',
            y_axis=move_top_10['二线城市场次'].tolist(),  # 数据
            label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#ed9b9b", opacity=0.8),  # 柱形图颜色及透明度
        )
        .add_yaxis(
            series_name="三线城市",  # 柱形图系列名称
            stack='stack1',
            y_axis=move_top_10['三线城市场次'].tolist(),  # 数据
            label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#4fc0cc", opacity=0.8),  # 柱形图颜色及透明度
        )
        .add_yaxis(
            series_name="四线城市",  # 柱形图系列名称
            stack='stack1',
            y_axis=move_top_10['四线城市场次'].tolist(),  # 数据
            label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#f7ce8f", opacity=0.8),  # 柱形图颜色及透明度
        )
        .add_yaxis(
            series_name="五线城市",  # 柱形图系列名称
            stack='stack1',
            y_axis=move_top_10['五线城市场次'].tolist(),  # 数据
            label_opts=opts.LabelOpts(is_show=False, position='top', formatter="{c}"),  # 显示数据标签
            itemstyle_opts=opts.ItemStyleOpts(color="#7fa7c1", opacity=0.8),  # 柱形图颜色及透明度
        )
        .reversal_axis()
        # .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=[
            dict(
                text=f'2022-02-0{d} - 排片地域分布（场次）- 春节档',
                left='left',
                textStyle=dict(
                    color='#000',
                    fontSize=20)),
            dict(
                text=f'2022-02-0{d} - 排片统计（场次）- 春节档',
                left='60%',
                top='10%',
                textStyle=dict(
                    color='#000',
                    fontSize=16)),
        ],
            legend_opts=opts.LegendOpts(
                is_show=False, ),  # 不显示图例
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="shadow"
            ),  # 提示框
            yaxis_opts=opts.AxisOpts(name='',
                                     type_='category',
                                     #    axislabel_opts=opts.LabelOpts(rotate=30),
                                     ),
            xaxis_opts=opts.AxisOpts(type_="value",  # y轴类型
                                     #   max_=5000000,
                                     name='',  # y轴名称
                                     name_location='middle',  # y轴名称位置
                                     name_gap=70,  # y轴名称距离轴线距离
                                     axistick_opts=opts.AxisTickOpts(is_show=False),  # 刻度线
                                     axisline_opts=opts.AxisLineOpts(is_show=False),  # y轴线
                                     splitline_opts=opts.SplitLineOpts(is_show=True),  # y轴网格线
                                     axislabel_opts=opts.LabelOpts(formatter="{value}")),  # 轴标签显示方式
        )
    )
    pie = (Pie(init_opts=opts.InitOpts(theme='light'))
           .add('', [list(z) for z in zip(paipian['电影'].tolist(),
                                          paipian['场次'].tolist())], radius=['45', '100'], center=['70%', '40%'])
           .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}：{c}  {d}%'))
           .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
           )
    bar_diyu_pie.overlap(pie)
    t2.add(bar_diyu_pie, '{}'.format(d))
t2.render_notebook()

from pyecharts.charts import Page
page = Page(layout=Page.DraggablePageLayout, page_title="大屏展示")

page.add(
   line,bar,bar_china,bar_diyu,t2)
# 先保存到test.html 然后打开，拖拽图片自定义布局， 之后记得点击左上角“save config”对布局文件进行保存。
# 会生成一个chart_config.json的文件，这其中包含了每个图表ID对应的布局位置
page.render('movie analyze.html')

