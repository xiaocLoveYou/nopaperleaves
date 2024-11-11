import datetime
import random

import pandas as pd
from hyperframe.frame import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.dialects.mssql.information_schema import columns

# 1. 读取 Excel 文件到 Pandas DataFrame
file_path = "students.xlsx"  # Excel 文件路径
df = pd.read_excel(file_path)
engine = create_engine("mysql+pymysql://root:123456@localhost/nopaper")

data = pd.read_sql("users",con=engine).query("role == 'normal'")

print(data)

df: pd.DataFrame = pd.DataFrame(data={"user_id": [], "date": [], "status": [], "department_id": [], "resion": []})

print(df)

datelist = [pd.to_datetime(datetime.datetime.now()) - pd.Timedelta(days=x) for x in range(100)]
print(datelist)
# 创建用于存储新行的列表
new_rows = []
options = [0, 1, 2]
probabilities = [0.8, 0.12, 0.08]

# 随机生成一个值

# 遍历原始数据的每一行，并生成日期对应的多行
for row, iterrow in data.iterrows():
    for e in datelist[:50]:  # 仅使用 datelist 的前5天作为示例
        # 将新行数据追加到 new_rows 列表
        new_rows.append({
            "user_id": iterrow["user_id"],
            "date": e,
            "status": str(random.choices(options, probabilities)[0]),
            "department_id": iterrow["department_id"],
            "resion": None
        })
# df["user_id"] = df["user_id"].dtype(int)
df["status"] = df["status"].astype(int)
print(df)
# 使用 pd.concat 一次性添加新行数据
df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

print(df)




# 5. 将数据插入到数据库的 Users 表中
try:
    df.to_sql('attendance', con=engine, if_exists='append', index=False)
    print("数据插入成功")
except Exception as e:
    print("插入失败：", e)
