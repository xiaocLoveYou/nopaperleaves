import pandas as pd
from sqlalchemy import create_engine

# 1. 读取 Excel 文件到 Pandas DataFrame
file_path = "students.xlsx"  # Excel 文件路径
df = pd.read_excel(file_path)

# 2. 重命名 DataFrame 列，匹配数据库字段
df.columns = ['grade', 'class_name', 'username', 'student_id', 'status', 'account', 'password']

# 3. 添加必要的字段：role 和 department_id, class_id
df['role'] = 'normal'               # 假设所有学生默认角色为 'normal'
# df['department_id'] = None          # 系部 ID，可以基于年级或班级进一步获取
# df['class_id'] = None               # 班级 ID，可以基于年级或班级进一步获取

# 将需要插入的列映射到数据库 `Users` 表的字段名
user_data = df.rename(columns={
    'username': 'username',
    'password': 'password',
    'role': 'role',
    'department_id': 'department_id',
    'class_id': 'class_id'
})[['username', 'password', 'role', 'department_id', 'class_id']]

# 4. 创建数据库连接
# 替换以下信息：username，password，hostname，database_name
engine = create_engine("mysql+pymysql://username:password@hostname/database_name")

# 5. 将数据插入到数据库的 Users 表中
try:
    user_data.to_sql('Users', con=engine, if_exists='append', index=False)
    print("数据插入成功")
except Exception as e:
    print("插入失败：", e)
