import datetime
import json
import pandas as pd
import pymysql
from pandas import DataFrame, Series

from utils import get_conn, get_local_date


# 仪表盘班级
def helper1(class_id):

    # 这里直接从数据库获取数据，不需要传入data参数
    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    # date = datetime.datetime.utcnow().date()
    date = get_local_date()
    print("当前日期：", date)

    # 将数据中的日期转换为日期类型，忽略时间部分
    print(data['date'])
    data['date'] = pd.to_datetime(data['date']).dt.strftime("%Y-%m-%d")
    print("数据中的日期列：")
    print(data['date'].head())  # 打印日期列的前几行，检查转换后的日期格式

    # 过滤数据，注意日期匹配
    data = data[(data["date"] == date) & (data["class_id"] == class_id)]
    print(f"过滤后的数据（class_id={class_id}）：")
    print(data)

    if data.empty:
        print(f"没有找到 class_id={class_id} 和当前日期的数据。")
        return {"ren_data": []}

    all_status = ["0", "1", "2", "3", "4"]

    multi_index = pd.MultiIndex.from_product([data["class_id"].unique(), all_status],
                                             names=["class_id", "status"])

    # Grouping data by class_id and status, filling missing status with 0
    ren = data.groupby(["class_id", "status"]).size().reindex(multi_index, fill_value=0).reset_index(name="sum")

    # Replace status codes with descriptions
    ren["status"] = ren["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })

    print("status 替换后的数据：")
    print(ren)
    ren_data = ren.to_dict(orient='records')
    print(ren_data)
    return ren_data

# 仪表盘系部
def helper2(department_id):
    # 这里直接从数据库获取数据，不需要传入data参数
    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    date = get_local_date()

    print("当前日期：", date)

    # 将数据中的日期转换为日期类型，忽略时间部分
    data['date'] = pd.to_datetime(data['date']).dt.to_period("d")
    print("数据中的日期列：")
    print(data['date'].head())  # 打印日期列的前几行，检查转换后的日期格式

    # 过滤数据，注意日期匹配
    data = data[(data["date"] == date) & (data["department_id"] == department_id)]
    print(f"过滤后的数据（class_id={department_id}）：")
    print(data)

    if data.empty:
        print(f"没有找到 class_id={department_id} 和当前日期的数据。")
        return {"ren_data": []}

    all_status = ["0", "1", "2", "3", "4"]

    multi_index = pd.MultiIndex.from_product([data["department_id"].unique(), all_status],
                                             names=["department_id", "status"])

    # Grouping data by class_id and status, filling missing status with 0
    ren = data.groupby(["department_id", "status"]).size().reindex(multi_index, fill_value=0).reset_index(name="sum")

    # Replace status codes with descriptions
    ren["status"] = ren["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })

    print("status 替换后的数据：")
    print(ren)
    ren_data = ren.to_dict(orient='records')
    print(ren_data)
    return ren_data


# 堆叠柱状图班级
def helper3(class_id):

    # 这里直接从数据库获取数据，不需要传入data参数
    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    print(data['date'].head())

    # 过滤数据，注意日期匹配
    data = data[(data["class_id"] == class_id)]
    print(f"过滤后的数据（class_id={class_id}）：")
    print(data)

    if data.empty:
        print(f"没有找到 class_id={class_id} 和当前日期的数据。")
        return {"ren_data": []}
    all_status = ["0", "1", "2", "3", "4"]
    # 按 class_id、status 和 date 进行分组统计
    class_status = pd.MultiIndex.from_product(
        [data["class_id"].unique(), all_status, data["date"].unique()],
        names=["class_id", "status", "date"]
    )
    bzhuangtai = data.groupby(["class_id", "status", "date"]).size().reindex(
        class_status, fill_value=0).reset_index(name="sum")
    bzhuangtai["status"] = bzhuangtai["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })
    print("status 替换后的数据：")
    print(bzhuangtai)
    bzhuangtai_data = bzhuangtai.to_dict(orient='records')
    print(bzhuangtai_data)
    return bzhuangtai_data

def helper4(department_id):

    # 这里直接从数据库获取数据，不需要传入data参数
    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    date = datetime.datetime.utcnow().date()

    print("当前日期：", date)



    # 将数据中的日期转换为日期类型，忽略时间部分
    data['date'] = pd.to_datetime(data['date']).dt.to_period("d")
    print("数据中的日期列：")
    print(data['date'].head())  # 打印日期列的前几行，检查转换后的日期格式

    # 过滤数据，注意日期匹配
    data = data[(data["date"] == date) & (data["department_id"] == department_id)]
    print(f"过滤后的数据（class_id={department_id}）：")
    print(data)

    if data.empty:
        print(f"没有找到 class_id={department_id} 和当前日期的数据。")
        return {"ren_data": []}

    all_status = ["0", "1", "2", "3", "4"]

    multi_index = pd.MultiIndex.from_product([data["department_id"].unique(), all_status],
                                             names=["department_id", "status"])

    # Grouping data by class_id and status, filling missing status with 0
    ren = data.groupby(["department_id", "status"]).size().reindex(multi_index, fill_value=0).reset_index(name="sum")

    # Replace status codes with descriptions
    ren["status"] = ren["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })

    print("status 替换后的数据：")
    print(ren)
    ren_data = ren.to_dict(orient='records')
    print(ren_data)
    return ren_data

## 状态分布雷达图
def helper5():

    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    print(data['date'].head())

    date = datetime.datetime.utcnow().date()
    # print(date)
    # date = "2024-11-11"
    data = data[data["date"] == str(date)]

    all_status = ["0", "1", "2", "3", "4"]

    qzhuangtai = data.groupby(["status"]).size().reindex(all_status, fill_value=0).reset_index(name="sum")

    qzhuangtai["status"] = qzhuangtai["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })
    zong = qzhuangtai["sum"].sum()
    qzhuangtai["sum"] = (qzhuangtai["sum"] / zong * 100).round(2)
    print("status 替换后的数据：")
    print(qzhuangtai)
    qzhuangtai_data = qzhuangtai.to_dict(orient='records')
    print(qzhuangtai_data)

    option = {
        'title': {
            'text': '状态分布雷达图',
            'left': 'center',
            'textStyle': {
                'fontSize': 16
            }
        },
        'tooltip': {},
        'radar': {
            'indicator': [{
                'name': status,
                'max': 85
            } for status in qzhuangtai["status"]],
        },
        'series': [{
            'name': '状态分布',
            'type': 'radar',
            'data': [{
                'value': qzhuangtai["sum"].tolist(),
                'name': '状态分布'
            }]
        }]
    }

    return option

## 状态分布饼图
def helper6():

    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    date = datetime.datetime.utcnow().date()
    date = str(date)
    # date = "2024-11-08"
    print("日期", date)

    data['date'] = pd.to_datetime(data['date']).dt.to_period("d")

    print(data['date'].head())


    data = data[(data["date"] == date)]
    all_status = ["0", "1", "2", "3", "4"]

    multi_index = pd.MultiIndex.from_product([data["class_id"].unique(), all_status],
                                             names=["class_id", "status"])


    ren = data.groupby(["class_id", "status"]).size().reindex(multi_index, fill_value=0).reset_index(name="sum")

    ren["status"] = ren["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })
    print(ren)
    class_id = ren[ren["status"] == "正常报道"]
    print(class_id)
    class_id = class_id.sort_values("sum",ascending=False).head(1).iloc[0][0]
    print("qwqwqweeqeqe\n",class_id)
    ren = ren[ren["class_id"] == class_id]

    print(ren)
    ren_data = ren.to_dict(orient='records')
    print(ren_data)

    option = {
        'title': {
            'text': '状态分布饼图',
            'left': 'center',
            'textStyle': {
                'fontSize': 16
            }
        },
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'right',
            'data': ren['status'].tolist()
        },
        'series': [{
            'name': '状态分布',
            'type': 'pie',
            'radius': ['35%', '60%'],
            'data': {"name": ren["status"].tolist(), "value": ren["sum"].tolist()},
            'emphasis': {
                'itemStyle': {
                    'shadowBlur': 10,
                    'shadowOffsetX': 0,
                    'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }
    return option

## 状态分布饼图 最小
def helper7():

    data: DataFrame = pd.read_sql("select * from attendance", get_conn())

    # date = datetime.datetime.utcnow().date()
    date = "2024-11-08"
    print("日期", date)




    data['date'] = pd.to_datetime(data['date']).dt.to_period("d")

    print(data['date'].head())


    data = data[(data["date"] == date)]
    all_status = ["0", "1", "2", "3", "4"]

    multi_index = pd.MultiIndex.from_product([data["class_id"].unique(), all_status],
                                             names=["class_id", "status"])


    ren = data.groupby(["class_id", "status"]).size().reindex(multi_index, fill_value=0).reset_index(name="sum")

    ren["status"] = ren["status"].replace({
        '0': '正常报道', '1': '病假', '2': '事假', '3': '病假未审批', '4': '事假未审批'
    })
    print(ren)
    class_id = ren[ren["status"] == "正常报道"]
    print(class_id)
    class_id = class_id.sort_values("sum",ascending=True).head(1).iloc[0][0]
    print("qwqwqweeqeqe\n",class_id)
    ren = ren[ren["class_id"] == class_id]

    print(ren)
    ren_data = ren.to_dict(orient='records')
    print(ren_data)

    option = {
        'title': {
            'text': '状态分布饼图',
            'left': 'center',
            'textStyle': {
                'fontSize': 16
            }
        },
        'tooltip': {
            'trigger': 'item',
            'formatter': '{a} <br/>{b}: {c} ({d}%)'
        },
        'legend': {
            'orient': 'vertical',
            'left': 'right',
            'data': ren['status'].tolist()
        },
        'series': [{
            'name': '状态分布',
            'type': 'pie',
            'radius': ['35%', '60%'],
            'data': {"name": ren["status"].tolist(), "value": ren["sum"].tolist()},
            'emphasis': {
                'itemStyle': {
                    'shadowBlur': 10,
                    'shadowOffsetX': 0,
                    'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }
    return option
