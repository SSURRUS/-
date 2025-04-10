第一模块就是将需要的包导进去

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

目的：导入数据处理，可视化和工具所需要的Python库
详细说明：
    numpy(np)：用于数值计算的库，提供数组操作功能，在数据处理中常用于数学运算
    pandas（pd）：数据分析的核心库，用于读取、清洗和处理结构化的数据（如表格）
    collections.Counter：一个计数工具，用于统计可迭代对象的元素出现次数
    pyecharts：一个基于ECharts的Python可视化库，用于生成交互式图表：
      options as opts:提供图表的配置选项，如标题、轴、标签等
      charts：导入所有的图表类型（如Bar、Line、Pie等），通过from  import*方式引入
      commons.utils.jsCode：允许在图表中嵌入Javascript代码，用于自定义样式（如渐变色)
      global.ThemeType:定义图表主题（如light,dark等）
      components.Table:用于创建表格组件
      options.ComponentTitleOpts:配置表格标题的选项
datatime：处理日期时间的库，也可以用于日期的筛选和格式化

第二模块就是对数据进行读取并且进行一个初步的清洗

data_haed = pd.read_excel(r"E:/data analyze/春节档-电影票房表现概览.xlsx")
这边根据你文件的路径地址进行粘贴就可以
data_haed.head(1)

data_haed["首映票房"] = data_haed["首映票房"].apply(lambda x: round(x/100000000, 2))
data_haed["首周票房"] = data_haed["首周票房"].apply(lambda x: round(x/100000000, 2))
data_haed["首周末票房"] = data_haed["首周末票房"].apply(lambda x: round(x/100000000, 2))

data_haed = data_haed.rename(columns={"首映票房": "首映票房/亿", "首周票房": "首周票房/亿", "首周末票房": "首周末票房/亿"})

data_haed.info()

data_haed = data_haed.drop(labels=["EntMovieID","DBOMovieID","EFMTMovieID","GenreMainID"],axis=1)

目的：读取“春节档-电影票房表现概览。xlsx”文件，进行单位转换和列清理
详细说明：
 数据读取：
     pd.read_excel(...):从指定路径读取Excel文件，返回一个DataFrame对象
     data_head.head(1):查看前一行数据，用于初步检查数据结构
 单位转换：
     对“首映票房”、“首周票房”，“首周末票房”三列进行处理：
        apply（lambda x:round(x/100000000,2)）：将原始数据（假设为元）除1亿并保留两位小数，转换为亿元单位
        例如：原始值是123456789，运行后结果为1.23亿
 列重命名：
     rename（columns={...}）:将列名字改为带有“/亿”的新名称，明确单位
 数据信息查看：
     data_head.info():输出DataFrame的基本信息，包括列名、数据类型、非空值数量等，便于检查数据的完整性
 删除无关列：
     drop(labels=[...],axis=1):删除指定的4列（EntMovieID等）


第三模块就是创建电影详情表格

colums=list(data_head)
print(colums)

headers=colums
row_all=data_head[colums].apply(lambda x: list(x),axis=).value.tolist()

table_all=Table()
attributes={"class":"fl-table","style":"margin: auto"}
table_all.add(headers,row_all,attributes)
table_all.set_global_opts(
    title_opts=ComponentTitleOpts(title=f"春节档-电影详情数据概览",subtitle="(上下左右移动表格)")
    )
table_all.render_notebook()

目的：将清洗后的数据生成一个交互式的表格并显示
详细说明：
  获取列名：
    colums=list(data_head):将DataFrame的列名转换为列表
    print(colums):打印列名，便于确认
  数据准备：
    data.head[colums].apply(lambda x:list(x),axis=1):按行将数据转换为列表形式
    .values.tolist()：将结果转为Python原生列表，作为表格的行数据
  创建表格：
    Table():初始化一个表格对象
    attributes：定义HTML属性，class="fl-table"可能用于CSS样式,style="margin:0 auto"使表格居中
    add(headers,row_all，attributes):添加表头（列名）和行数据
  设置全局选项：
    set_global_opts(title_opts=...):设置表格标题和副标题，提示用户可以拖动表格进行查看
  渲染：
    render_notebook():在Jupyter Notebook中渲染交互式表格（需在Notebook环境中运行）

第四模块数据的读取与清洗（电影票房三十日时段详情）

data_movie_time = pd.read_excel(r"E:/data analyze/春节档-电影票房三十日时段详情.xls")

data_movie_time["当前票房/万"]=data_movie_time["当前票房/万"].apply(lambda x:round(x/10000000,2))
data_movie_time["当前场次"]=data_movie_time["当前场次"].apply(lambda x:round(x/10000,2))
data_movie_time["当前人次/万"]=data_movie_time["当前人次/万"].apply(lambda x:round(x/10000000,2))

data_movie_time=data_movie_time.rename(
    columns={"当前票房/万"："当前票房/千万"，"当前场次"："当前场次/万"，"当前人次/万"："当前人次/百万"}）
data_movie_time=data_movie_time[data_movie_time['日期']<='2022-02-07']
data_movie_time.head(2)

data_movie_time['电影'].value_counts()

目的：读取“春节档-电影票房三十日时段详情.xls”，进行单位转换并筛选数据
详细说明：
  数据读取：
    pd.read_excel(...): 读取 Excel 文件
  单位转换：
    "当前票房/万"除以1000万，转换为"千万"单位
    "当前场次"除以1万，单位不变但是数值调整
    "当前人次/万"除以100万，转换为"百万"单位
    使用round(...,2)保留两位小数
  列表重名:
    rename(columns={......}):更新列名以反映新单位
  数据筛选：
    data_movie_time['日期']<='2022-02-07'：筛选出春节档的数据
  初步检查：
    head(2)：查看前2行
    value_counts():统计各电影的出现次数，了解数据分布


第五模块创建折线图（长津湖之水门桥票房表现）

movie_chang=data_movie_time[data_movie_time["电影"]=="长津湖之水门桥"]

line=Line(
        init_opts=opts.InitOpts(
            theme='light',
            width='1000px',
            height='600px')
）

line.add_xaxis(
    movie_chang["日期"].tolist()
)

colums=["当前票房/千万"，"当前场次/万"，"当前人次/百万"]
for i in range(3):
    line.add_yaxis(
        colums[i],
        movie_chang[colums[i]],
        is_symbol_show=False,
        is_smooth=True,
        areastyle_opt=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
        z=100,
        linestyle_opts{
            "normal":{
                  "shadowColor"：'rgba(0,0,0,.5)'，
                  "shadowBlur":0,
                  "shadowOffsetY":1,
                  "shadowOffsetX":1,
                  }
            }
    )
    
line.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        boundary_gap=Flase，
        axislabel_opts=opts.LabelOpts(margin=30,color="black"),
        axisstick_opts=opts.AxisTickOpts(is_show=False),),
    yaxis_opts=opts.AxisOpts(
         name=''.
         axisline_opts=opts.AxisLineOpts(is_show=True)，
         axistick_opts=opts.AxisTickOpts(is_show=False),
         splitline_opts=opts.SplitLineOpts(
             is_show=True,
             linestyle_opts=opts.LineStyleOpts(color='#483D8B'))
   )
   tooltip_opts=opts.TooltipOpts(
       is_show=True,trigger='axis',axis_pionter_type='cross'),
    title_opts=opts.TitleOpts(title="长津湖上映一周电影票房表现",
                              title_textstyle_opts=opts.TextStyleOpts(font_size=18),
                              subtitle"2022-02-01~2022-02-07",
                              pos_left='center'),
    legend_opts=opts.LegendOpts(
        is_show=True,
        post_top=45,
        orient="horizontal"
    ),
    graphic_opts=[
        opts.GraphicGroup(
            graphic_item=opts.GraphicItem(id='1',left="center",top="center",z=-1),
            children=[
                opts.GraphicImage(graphic_item=opts.GraphicItem(id="logo",
                                                                left='center',
                                                                z=-1),
                                  graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                                      opacity=0.5,)
                                      )
                ]
            )
        ]
    )

line.set_series_opts(
    markarea_opts=opts.MarkAreaOpts(
        is_silent=True,
        label_opts=opts.LabelOpts(position='bottom',color='#000000'),
        itemstyle_opts=opts.ItemStyleOpts(color='#1E90FF',opacity=0.2),
        data=[
            opts.MarkAreaItem(name="正式上映\n春节档",x=("2022-02-01","2022-02-02")),
            ]
        ),
    )
    line.set_color(colors=['#80FFA5','00DDFF','#FF0087'])
    line.render_notebook()
    
目的: 为电影“长津湖之水门桥”绘制票房、场次、人次的折线图

详细说明:
  数据筛选：
    筛选出“长津湖之水门桥”的数据。
  初始化折线图：
    Line(init_opts=...):创建折现图，设置主题为light,宽1000px，高600px
  添加X轴
    add_xaxis(...):使用日期作为x轴
  添加多条Y轴数据
    循环添加“当前票房/千万”、“当前场次/万”、“当前人次/百万”三条折线：
      is_smooth=True:平滑曲线
      areastyle_opts:添加半透明区域填充
      linestyle_opts:设置线条阴影效果
  全局配置：
    xaxis_opts:X轴无间隙，标签为黑色
    yaxis_opts:Y轴显示网线格，颜色为深紫色
    tooltip_opts:鼠标悬停显示交叉线提示
    title_opts:设置标题和副标题，居中显示
    legend_opts:图例水平显示，位于顶部
    graphic_opts:添加背景图（代码中图片URL被注释，可自行进行添加）
 系统配置：
   markarea_opts:标志"2022-02-01至02-02"为春节档正式上映区域
   set_color:设置三条线的颜色
 渲染：
   在Notebook中显示
