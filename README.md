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
