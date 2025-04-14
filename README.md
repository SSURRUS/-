第一模块就是将需要的包导进去<br>

import numpy as np <br>
import pandas as pd <br>
from collections import Counter <br>
from pyecharts import options as opts <br>
from pyecharts.charts import * <br>
from pyecharts.commons.utils import JsCode <br>
from pyecharts.globals import ThemeType <br>
from pyecharts.components import Table <br>
from pyecharts.options import ComponentTitleOpts <br>
import datetime <br>

目的：导入数据处理，可视化和工具所需要的Python库 <br>
详细说明：<br>
    numpy(np)：用于数值计算的库，提供数组操作功能，在数据处理中常用于数学运算 <br>
    pandas（pd）：数据分析的核心库，用于读取、清洗和处理结构化的数据（如表格）<br>
    collections.Counter：一个计数工具，用于统计可迭代对象的元素出现次数 <br>
    pyecharts：一个基于ECharts的Python可视化库，用于生成交互式图表：<br>
    options as opts:提供图表的配置选项，如标题、轴、标签等 <br>
    charts：导入所有的图表类型（如Bar、Line、Pie等），通过from  import*方式引入 <br>
    commons.utils.jsCode：允许在图表中嵌入Javascript代码，用于自定义样式（如渐变色) <br>
    global.ThemeType:定义图表主题（如light,dark等） <br>
    components.Table:用于创建表格组件 <br>
    options.ComponentTitleOpts:配置表格标题的选项 <br>
    datatime：处理日期时间的库，也可以用于日期的筛选和格式化 <br>

##第二模块就是对数据进行读取并且进行一个初步的清洗 <br>

data_haed = pd.read_excel(r"E:/data analyze/春节档-电影票房表现概览.xlsx") <br>
这边根据你文件的路径地址进行粘贴就可以 <br>
data_haed.head(1) <br>

data_haed["首映票房"] = data_haed["首映票房"].apply(lambda x: round(x/100000000, 2)) <br>
data_haed["首周票房"] = data_haed["首周票房"].apply(lambda x: round(x/100000000, 2)) <br>
data_haed["首周末票房"] = data_haed["首周末票房"].apply(lambda x: round(x/100000000, 2)) <br>

data_haed = data_haed.rename(columns={"首映票房": "首映票房/亿", "首周票房": "首周票房/亿", "首周末票房": "首周末票房/亿"}) <br>

data_haed.info() <br>

data_haed = data_haed.drop(labels=["EntMovieID","DBOMovieID","EFMTMovieID","GenreMainID"],axis=1) <br>

目的：读取“春节档-电影票房表现概览。xlsx”文件，进行单位转换和列清理 <br>
详细说明： <br>
 数据读取： <br>
     pd.read_excel(...):从指定路径读取Excel文件，返回一个DataFrame对象 <br>
     data_head.head(1):查看前一行数据，用于初步检查数据结构 <br>
 单位转换： <br>
 对“首映票房”、“首周票房”，“首周末票房”三列进行处理： <br>
        apply（lambda x:round(x/100000000,2)）：将原始数据（假设为元）除1亿并保留两位小数，转换为亿元单位 <br>
        例如：原始值是123456789，运行后结果为1.23亿 <br>
 列重命名： <br>
     rename（columns={...}）:将列名字改为带有“/亿”的新名称，明确单位 <br>
 数据信息查看： <br>
     data_head.info():输出DataFrame的基本信息，包括列名、数据类型、非空值数量等，便于检查数据的完整性 <br>
 删除无关列： <br>
     drop(labels=[...],axis=1):删除指定的4列（EntMovieID等） <br>

运行截图： <br>
这段是在程序当中直接生成的效果图，需要在开发软件的运行框里面查看 <br>
![d060044b72be28b87cfa532e157103c](https://github.com/user-attachments/assets/6427952f-4f00-4786-88fa-2085abf8ece6)

第三模块就是创建电影详情表格 <br>

colums=list(data_head) <br>
print(colums) <br>

headers=colums <br>
row_all=data_head[colums].apply(lambda x: list(x),axis=).value.tolist() <br>

table_all=Table() <br>
attributes={"class":"fl-table","style":"margin: auto"} <br>
table_all.add(headers,row_all,attributes) <br>
table_all.set_global_opts( <br>
    title_opts=ComponentTitleOpts(title=f"春节档-电影详情数据概览",subtitle="(上下左右移动表格)") <br>
    ) <br>
table_all.render_notebook() <br>

目的：将清洗后的数据生成一个交互式的表格并显示 <br>
详细说明： <br>
  获取列名： <br>
    colums=list(data_head):将DataFrame的列名转换为列表 <br>
    print(colums):打印列名，便于确认 <br>
  数据准备： <br>
    data.head[colums].apply(lambda x:list(x),axis=1):按行将数据转换为列表形式 <br>
    .values.tolist()：将结果转为Python原生列表，作为表格的行数据 <br>
  创建表格： <br>
    Table():初始化一个表格对象 <br>
    attributes：定义HTML属性，class="fl-table"可能用于CSS样式,style="margin:0 auto"使表格居中 <br>
    add(headers,row_all，attributes):添加表头（列名）和行数据 <br>
  设置全局选项： <br>
    set_global_opts(title_opts=...):设置表格标题和副标题，提示用户可以拖动表格进行查看 <br>
  渲染： <br>
    render_notebook():在Jupyter Notebook中渲染交互式表格（需在Notebook环境中运行） <br>

第四模块数据的读取与清洗（电影票房三十日时段详情） <br>

data_movie_time = pd.read_excel(r"E:/data analyze/春节档-电影票房三十日时段详情.xls") <br>

data_movie_time["当前票房/万"]=data_movie_time["当前票房/万"].apply(lambda x:round(x/10000000,2)) <br>
data_movie_time["当前场次"]=data_movie_time["当前场次"].apply(lambda x:round(x/10000,2)) <br>
data_movie_time["当前人次/万"]=data_movie_time["当前人次/万"].apply(lambda x:round(x/10000000,2)) <br>

data_movie_time=data_movie_time.rename( <br>
    columns={"当前票房/万"："当前票房/千万"，"当前场次"："当前场次/万"，"当前人次/万"："当前人次/百万"}）<br>
data_movie_time=data_movie_time[data_movie_time['日期']<='2022-02-07'] <br>
data_movie_time.head(2) <br>

data_movie_time['电影'].value_counts() <br>

目的：读取“春节档-电影票房三十日时段详情.xls”，进行单位转换并筛选数据 <br>
详细说明： <br>
  数据读取： <br>
    pd.read_excel(...): 读取 Excel 文件 <br>
  单位转换： <br>
    "当前票房/万"除以1000万，转换为"千万"单位 <br>
    "当前场次"除以1万，单位不变但是数值调整 <br>
    "当前人次/万"除以100万，转换为"百万"单位 <br>
    使用round(...,2)保留两位小数 <br>
  列表重名: <br>
    rename(columns={......}):更新列名以反映新单位 <br>
  数据筛选： <br>
    data_movie_time['日期']<='2022-02-07'：筛选出春节档的数据 <br>
  初步检查： <br>
    head(2)：查看前2行 <br>
    value_counts():统计各电影的出现次数，了解数据分布 <br>


第五模块创建折线图（长津湖之水门桥票房表现） <br>

movie_chang=data_movie_time[data_movie_time["电影"]=="长津湖之水门桥"] <br>

line=Line( <br>
        init_opts=opts.InitOpts( <br>
            theme='light', <br>
            width='1000px', <br>
            height='600px') <br>
） <br>

line.add_xaxis( <br>
    movie_chang["日期"].tolist() <br>
) <br>

colums=["当前票房/千万"，"当前场次/万"，"当前人次/百万"] <br>
for i in range(3): <br>
    line.add_yaxis( <br>
        colums[i], <br>
        movie_chang[colums[i]], <br>
        is_symbol_show=False, <br>
        is_smooth=True, <br>
        areastyle_opt=opts.AreaStyleOpts(opacity=0.5), <br>
        label_opts=opts.LabelOpts(is_show=False), <br>
        z=100, <br>
        linestyle_opts{ <br>
            "normal":{ <br>
                  "shadowColor"：'rgba(0,0,0,.5)'， <br>
                  "shadowBlur":0, <br>
                  "shadowOffsetY":1, <br>
                  "shadowOffsetX":1, <br>
                  } <br>
            } <br>
    ) <br>
    
line.set_global_opts( <br>
    xaxis_opts=opts.AxisOpts( <br>
        boundary_gap=Flase， <br>
        axislabel_opts=opts.LabelOpts(margin=30,color="black"), <br>
        axisstick_opts=opts.AxisTickOpts(is_show=False),), <br>
    yaxis_opts=opts.AxisOpts( <br>
         name=''. <br>
         axisline_opts=opts.AxisLineOpts(is_show=True)， <br>
         axistick_opts=opts.AxisTickOpts(is_show=False), <br>
         splitline_opts=opts.SplitLineOpts( <br>
             is_show=True, <br>
             linestyle_opts=opts.LineStyleOpts(color='#483D8B')) <br>
   ) <br>
   tooltip_opts=opts.TooltipOpts( <br>
       is_show=True,trigger='axis',axis_pionter_type='cross'), <br>
    title_opts=opts.TitleOpts(title="长津湖上映一周电影票房表现", <br>
                              title_textstyle_opts=opts.TextStyleOpts(font_size=18), <br>
                              subtitle"2022-02-01~2022-02-07", <br>
                              pos_left='center'), <br>
    legend_opts=opts.LegendOpts( <br>
        is_show=True, <br>
        post_top=45, <br>
        orient="horizontal" <br>
    ),<br>
    graphic_opts=[ <br>
        opts.GraphicGroup( <br>
            graphic_item=opts.GraphicItem(id='1',left="center",top="center",z=-1), <br>
            children=[ <br>
                opts.GraphicImage(graphic_item=opts.GraphicItem(id="logo", <br>
                                                                left='center', <br>
                                                                z=-1), <br>
                                  graphic_imagestyle_opts=opts.GraphicImageStyleOpts( <br>
                                      opacity=0.5,) <br>
                                      ) <br>
                ] <br>
            ) <br>
        ] <br>
    ) <br>
    

line.set_series_opts( <br>
    markarea_opts=opts.MarkAreaOpts( <br>
        is_silent=True, <br>
        label_opts=opts.LabelOpts(position='bottom',color='#000000'), <br>
        itemstyle_opts=opts.ItemStyleOpts(color='#1E90FF',opacity=0.2), <br>
        data=[ <br>
            opts.MarkAreaItem(name="正式上映\n春节档",x=("2022-02-01","2022-02-02")), <br>
            ] <br>
        ), <br>
    ) <br>
    line.set_color(colors=['#80FFA5','00DDFF','#FF0087']) <br>
    line.render_notebook() <br>
    
目的: 为电影“长津湖之水门桥”绘制票房、场次、人次的折线图 <br>

详细说明: <br>
  数据筛选： <br>
    筛选出“长津湖之水门桥”的数据 <br>
  初始化折线图： <br>
    Line(init_opts=...):创建折现图，设置主题为light,宽1000px，高600px <br>
  添加X轴 <br>
    add_xaxis(...):使用日期作为x轴 <br>
  添加多条Y轴数据 <br>
    循环添加“当前票房/千万”、“当前场次/万”、“当前人次/百万”三条折线： <br>
      is_smooth=True:平滑曲线 <br>
      areastyle_opts:添加半透明区域填充 <br>
      linestyle_opts:设置线条阴影效果 <br>
  全局配置： <br>
    xaxis_opts:X轴无间隙，标签为黑色 <br>
    yaxis_opts:Y轴显示网线格，颜色为深紫色 <br>
    tooltip_opts:鼠标悬停显示交叉线提示 <br>
    title_opts:设置标题和副标题，居中显示 <br>
    legend_opts:图例水平显示，位于顶部 <br>
    graphic_opts:添加背景图（代码中图片URL被注释，可自行进行添加） <br>
 系统配置： <br>
   markarea_opts:标志"2022-02-01至02-02"为春节档正式上映区域 <br>
   set_color:设置三条线的颜色 <br>
 渲染： <br>
   在Notebook中显示 <br>
运行截图：<br>
![53d30a5bf1d2c63fb06ef1d617deb76](https://github.com/user-attachments/assets/6161ee7b-61dc-4b9e-8c6a-b89aa6b050dd)


第六模块是柱状图与折线图叠加 <br>

data = pd.read_excel(r"E:/data analyze/春节档-票房详情.xlsx") <br>
data.head(5) <br>

def tranform_data(x): <br>
    x=round(x/10000,2) <br>
    return x <br>

data['票房/（万）']=data['票房'].apply(lambda x:tranform_data(x)) <br>
data_7=data[data["日期"]>="2022-02-01"] <br>

bar=( <br>
    Bar(init_opts=opts.InitOpts(theme='light',width='980px',height='500px')) <br>
        .add_xaxis(xaxis_data=data_7['日期'].tolist()) <br>
        .add_yaxis( <br>
        series_name="场次", <br>
        y_axis=data_7['场次'].tolist(), <br>
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), <br>
        itemstyle_opts=opts.AreaStyleOpts(opacity=0.8,color=JsCode("...")) <br>
    )<br>
        .add_yaxis( <br>
        series_name="人次", <br>
        y_axis=data_7['人次'].tolist(), <br>
        label_opts=opts.LabelOpts(is_show=False,position='top',formatter="{c}"), <br>
        itemstyle_opts=opt.AreaStyleOpts(opacity=0.8,color=JsCode("...")) <br>
    ) <br>
        .extend_axis(yaxis=opts.AxisOpts(name="",type="value",min_=-4000,max_=200000,is_show=False)) <br>
        .set_global_opts(...) <br>
)<br>

line=( <br>
    Line() <br>
         .add_xaxis(xaxis_data=data_7['日期'].tolist()) <br>
         .add_yaxis( <br>
         series_name="票房/（万）", <br>
         yaxis_index=1, <br>
         is_smooth=True, <br>
         y_axis=data_7['票房/（万）'].tolist(), <br>
         itemstyle_opts={"normal":{...}}, <br>
         linestyle_opts={"normal":{...}} <br>
    )<br>
)<br>

bar.overlap(line) <br>
bar.render_notebook() <br>

目的: 显示春节档 7 天（2022-02-01 起）的场次、人次（柱状图）和票房（折线图）。 <br>
详细说明: <br>
  数据处理: <br>
    读取“春节档-票房详情.xlsx”，将票房转换为万元单位。筛选 2022-02-01 后的数据。<br>
  柱状图: <br>
    X 轴为日期，添加“场次”和“人次”两组柱状图，使用渐变色。添加次坐标轴（隐藏），为折线图准备。 <br>
  折线图: <br>
    添加“票房/万”折线，使用次坐标轴，设置渐变色和阴影。 <br>
  叠加: <br>
    bar.overlap(line): 将折线图叠加在柱状图上。 <br>
  渲染: <br>
    显示组合图表。 <br>



第七模块是堆叠柱状图 <br>

data = pd.read_excel(r'E:/data analyze/春节档-电影票房表现概览.xlsx') <br>
data["累计票房"]=data["累计票房"].apply(lambda x:round(x/10000000,2)) <br>
data["累计场次"]=data["累计场次"].apply(lambda x:round(x/10000,2)) <br>
data["累计人次"]=data["累计人次"].apply(lambda x:round(x/1000000,2)) <br>
data=data.rename(columns={"累计票房":"累计票房/千万","累计场次"："累计场次/万"，"累计人次"："累计人次/百万"}) <br>
data=data[data['正式上映日期']=='2022-02-01'] <br>

bar_china=( <br>
    Bar(init_opts=opts.InitOpts(width="1200px",height="600px,theme='light')) <br>
        .add_xaxis(xaxis_data=data['电影'].tolist()) <br>
        .add_yaxis(series_name="累计票房/千万",stack='stack1',y_axis=data['累计票房/千万'].tolist(),...) <br>
        .add_yaxis(series_name="累计票房/百万",stack='stack1',y_axis=data['累计票房/百万'].tolist(),...) <br>
        .add_yaxis(series_name="累计票房/万",stack='stack1',y_axis=data['累计票房/万'].tolist(),...) <br>
        .reversal_axis() <br>
        .set_global_opts(...) <br>
)<br>
bar_china.render_notebook() <br>

目的:  <br>
  显示 2022-02-01 上映电影的累计票房、人次、场次堆叠柱状图。 <br>
详细说明: <br>
  数据处理: <br>
    单位转换并筛选上映日期为 2022-02-01 的电影。 <br>
  柱状图: <br>
    X 轴为电影名，Y 轴为三组堆叠数据，使用渐变色和阴影。 <br>
    reversal_axis(): 翻转坐标轴，横向显示。 <br>
  渲染: <br>
    显示堆叠柱状图。 <br>
运行截图： <br>
![31cb437124aeae08ab2522ed01d66de](https://github.com/user-attachments/assets/f04a3fc2-b4b1-4738-9713-2f7869afed37)



第八模块地域分布堆叠柱状图与饼图叠加 <br>

data_move_diyu = pd.read_excel(r'E:/data analyze/春节档-排片地域分布（场次）-top10影片.xlsx') <br>
data_move_diyu=data_move_diyu.drop(data_move_diyu[(data_move_diyu['电影']=="Clevel")|(data_move_diyu['电影']=="CityLevel")].index) <br>
data_move_diyu['电影']=data_move_diyu['电影'].apply(lambda x:x.split("|")[-1]) <br>
data_move_diyu=data_move_diyu.fillna(0) <br>
data_move_diyu['场次']=data_move_diyu['场次'].astype(int) <br>

one_city=data_move_diyu[(data_move_diyu['城市']=='一线城市'）] <br>

move_top_10=one_city_movie.merge(two_city_movie, how='left', on='电影').fillna(0) <br>

paipian_top=pd.read_excel(r'E:/data analyze/春节档-排片统计（场次）-top10影片.xlsx') <br>

bar_diyu=( <br>
    Bar(...) <br>
        .add_xaxis(...) <br>
        .add_yaxis(series_name="一线城市",stack='stack1',...) <br>
        .reversal_axis() <br>
        .set_global_opts(...) <br>
)  <br>
pie=(Pie(...).add(...)) <br>
bar_diyu.overlap(pie) <br>
bar_diyu.render_notebook() <br>
 
目的: <br> 
  显示 Top 10 电影在不同城市级别的排片分布（柱状图）与总排片占比（饼图）。 <br>
详细说明: <br>
  数据处理: <br>
    清洗数据，去除无关行，提取电影名，合并各城市级别数据。 <br>
  柱状图: <br>
    堆叠显示各城市级别场次。 <br>
  饼图: <br>
    显示总排片占比。 <br>
  叠加: <br>
    将饼图叠加在柱状图右侧。 <br>
运行截图：<br>
![567449b5b15c920f9c5805bc4f6edc9](https://github.com/user-attachments/assets/41ded739-c6c8-4bc8-9f2d-8cc26a852c80)


第九个模块时间动态图 <br>

t2=TimeLine(...) <br>
for d in range(1,7): <br>
    bar_diyu_pie=(Bar(...).add_yaxis(...)) <br>
    pie=(Pie(...).add(...)) <br>
    bar_diyu_pie.overlap(pie) <br>
    t2.add(bar_diyu_pie,'{}'.format(d)) <br>
t2.render_notebook() <br>

目的: <br>
  创建 2022-02-01 至 02-06 的动态地域分布图。<br>
详细说明: <br>
  时间线: <br>
    Timeline: 创建时间线组件，自动播放。 <br>
  每日图表: <br>
    循环生成每日柱状图和饼图组合。 <br>
  渲染: <br>
    显示动态图表。 <br>
运行截图：<br>
  因图片无法展示动态效果，还请自己跑一下代码看看时间线变换 <br>
![b3c8cea4048a96d4d8f4fb89bc3a858](https://github.com/user-attachments/assets/c5801ae7-409f-40c2-94c9-538bceb614e2)



第十模块大屏展示 <br>

from pyecharts.charts import Page <br>
#前面声明忘记加了 写在这边了 写在代码的开头会稍微好点 <br>
page=Page(layout=Page.DraggablePageLayout,page_title"大屏展示") <br>
page.add(line,bar,bar_china,bar_diyu,t2) <br>
page.render('movie analyze.html') <br>

目的: <br>
  将所有图表整合到一个可拖拽布局的 HTML 页面。 <br>
详细说明: <br>
  Page: 创建页面，支持拖拽布局。 <br>
  add(...): 添加所有图表。 <br>
  render(...): 输出 HTML 文件，用户可调整布局并保存配置。 <br>


总结：通过读取多个 Excel 文件，分析春节档电影数据，生成折线图、柱状图、饼图等可视化内容，最终整合为一个大屏展示页面。<br>
每个模块专注于特定数据处理或图表类型，逻辑清晰，适合数据分析和可视化展示需求。<br>
运行时需确保文件路径正确且环境支持 Notebook 或 HTML 输出。本段自述中的代码为自敲，因为这里尚且没有运行环境故无法测试，其中语法可能会有一些因为单词拼写的错误望能理解。<br>
代码源文件也已经上传可直接运行，本段自述仅用于加强自身对知识的理解也方便观看者。<br>
