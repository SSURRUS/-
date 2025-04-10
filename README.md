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
    .values.tolist()
